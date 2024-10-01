
from setuptools import setup
from setuptools.command.install import install
import sys

class crash_on_install(install):
    def run(self):
        sys.stderr.write("The package '{name}' is reserved for dragonfruit.ai\n")
        sys.exit(1)

setup(
    name='df-self-checkout',
    version='0.0.0',
    description="The package '{name}' is reserved for dragonfruit.ai",
    author='dragonfruit.ai',
    author_email='support@dragonfruit.ai',
    url='https://dragonfruit.ai',
    cmdclass={'install': crash_on_install},
    install_requires=[],
)
