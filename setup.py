from setuptools import setup
setup(
    name = 'ytdl',
    version = '0.1.0',
    packages = ['ytdl'],
    entry_points = {
        'console_scripts': [
            'ytdl = ytdl.__main__:main'
        ]
    })