from setuptools import setup, find_packages

__version__ = '0.0.0'

setup(
    name="laobot",
    version=__version__,
    install_requires=[
        'praw', 'bump2version', 'celery', 'redis', 'sqlalchemy', 'click', 'click-log',
        'python-pidfile'
        ],
    author='Bill Normandin',
    author_email='bill@pokeybill.us',
    url='https://pokeybots.com/laobot.html',
    packages=find_packages(),
    license='MIT',
    entry_points={'console_scripts': ['laobot=laobot.cli:cli']}
)
