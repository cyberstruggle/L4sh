import io
from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with io.open(path.join(pwd, 'README.md'), encoding='utf-8') as readme:
    desc = readme.read()
with io.open(path.join(pwd, 'requirements.txt'), encoding='utf-8') as requirements:
    required = requirements.read().splitlines()

setup(
    name='l4sh',
    description='A python tool for Log4Shell RCE Exploit - fully independent exploit does not require any 3rd party binaries.',
    long_description=desc,
    long_description_content_type='text/markdown',
    author='cyberstruggle',
    url='https://github.com/cyberstruggle/L4sh',
    download_url='https://github.com/cyberstruggle/L4sh',
    packages=['l4sh'],
    package_data={'l4sh': ['db/*', 'utils/*']},
    classifiers=[
        'Topic :: Security',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    entry_points={
        'console_scripts': [
            'l4sh = l4sh.main:main'
        ]
    },
    install_requires = required,
    keywords=['log4j', 'log4shell']
)