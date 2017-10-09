from setuptools import setup, find_packages

# Global variables
version = '0.1.0'
requires = [
    'requests',
    'arrow'
]

setup(
    name='pagerduty_v2',
    version=version,
    description='Python library to make integration with the PagerDuty v2 API easier.',
    long_description=open('README.rst', 'r').read(),
    author="Aaron Johnson",
    author_email="acjohnson@pcdomain.com",
    url="https://github.com/acjohnson/python-pagerduty_v2",
    packages=find_packages(),
    install_requires=requires
)
