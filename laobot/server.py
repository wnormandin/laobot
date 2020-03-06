import logging
import socket
import socketserver
import time
import sys
import pidfile

from laobot import __version__
from laobot.utils import constants, json_log
from laobot.utils.celery import get_app_info, ping


logger = logging.getLogger(__name__)
timers = {}
SHUTTING_DOWN = False


class LAOMessageHandler(socketserver.StreamRequestHandler):
    """ Handler for LAOBot server messages """

    def handle(self):
        self.current_command = self.rfile.readline().decode().strip()
        response = ''
        if self.current_command:
            if self.current_command.lower() == 'status':
                logger.debug('Status: OK')
                response = 'OK'
            elif self.current_command.lower() == 'shutdown':
                logger.warning('Received shutdown command')
                global SHUTTING_DOWN
                SHUTTING_DOWN = True
                response = 'Shutting down'
            else:
                logger.info(f'Received command: {self.current_command}')
                response = f'Received {len(self.current_command)} characters'
        else:
            response = 'Must provide a command'
        self.wfile.write(bytes(response, 'utf-8'))


class LAOBotServer(socketserver.TCPServer):
    """ LAOBot server, dispatches periodic tasks, handles requests """

    def serve_forever(self, poll_interval=0.5):
        logger.info(f'LAOBot Server: v{__version__}')
        with pidfile.PIDFile(constants.PIDFILE):
            super().serve_forever(poll_interval=poll_interval)

    def service_actions(self):
        from laobot.utils.celery import run_test, run_job

        if SHUTTING_DOWN:
            self.shutdown()
            sys.exit(0)

        if id(self) not in timers:
            timers[id(self)] = time.time()

        if time.time() - timers[id(self)] > constants.ACTION_WAIT_TIME:
            logger.debug('Running default task')
            # Do default work
            run_job.delay('television')
            timers[id(self)] = time.time()


def send_server_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((constants.SERVER_HOST, constants.SERVER_PORT))
        sock.sendall(bytes(f'{message}\n', 'utf-8'))
        return str(sock.recv(1024), 'utf-8')


def get_server(msg_handler=LAOMessageHandler):
    return LAOBotServer((constants.SERVER_HOST, constants.SERVER_PORT), msg_handler)


if __name__ == '__main__':
    try:
        if ping() is None:
            logger.error(f'No celery workers detected, is celery running?')
        else:
            json_log(get_app_info())

        with get_server() as server:
            server.serve_forever()
    except pidfile.AlreadyRunningError:
        print(f'Server already running (PIDFILE={constants.PIDFILE})')
