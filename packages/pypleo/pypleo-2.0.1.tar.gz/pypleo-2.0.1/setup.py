from setuptools import setup, find_packages

setup(
    name='pypleo',
    version='2.0.1',
    packages=['pypleo'],
    include_package_data=True,
    description="API client for legacy Pleo API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['requests']
)
