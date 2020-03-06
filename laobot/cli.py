import click
import click_log
import logging
import pidfile

from . import __version__ as app_version
from .server import send_server_message, get_server
from .utils import constants, json_log
from .utils.celery import get_app_info, ping


logger = logging.getLogger('laobot')
click_log.basic_config(logger)


@click.Group
@click.version_option(version=app_version)
@click_log.simple_verbosity_option(logger)
def cli():
    """ Command-line interface to LAOBot """


@cli.command()
@click.argument('message', nargs=-1)
def send(message):
    """ Send a raw command to the LAOBotServer (if it is running) """
    status = send_server_message("status")
    click.secho(f'Server status: {status}', fg='green' if status == 'OK' else 'red')
    if status == 'OK':
        click.echo(send_server_message(' '.join(message)))


@cli.command()
def shutdown():
    click.secho(send_server_message('shutdown'), fg='yellow')


@cli.command()
def get_worker_stats():
    json_log(get_app_info())


@cli.command()
@click.option('-p', '--poll', type=float, default=0.5)
def start(poll):
    try:
        if ping() is None:
            click.secho(f'No celery workers detected, is celery running?', fg='red')
            raise click.Abort()
        else:
            json_log(get_app_info())

        with get_server() as server:
            server.serve_forever(poll_interval=poll)

    except pidfile.AlreadyRunningError:
        click.secho(f'Server already running (PIDFile={constants.PIDFILE})', fg='red')
        raise click.Abort()


if __name__ == '__main__':
    cli(prog_name='laobot')
