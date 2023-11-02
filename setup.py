"""setup.py"""
import sys
import unittest
from setuptools import setup, find_packages, Command

# Define a custom test command
class TestCommand(Command):
    """
    Custom test command to run unit tests using unittest.

    This command allows running unit tests for the package using 'python setup.py test'.
    """

    user_options = []

    def initialize_options(self):
        """
        Initialize options for the custom test command.
        """

    def finalize_options(self):
        """
        Finalize options for the custom test command.
        """


    def run(self):
        """
        Run unit tests using unittest and exit with appropriate status code.
        """
        test_suite = unittest.TestLoader().discover('tests')
        result = unittest.TextTestRunner(verbosity=2).run(test_suite)
        if not result.wasSuccessful():
            sys.exit(1)

setup(
    name='entanglement-visualizer',
    version='0.1.0',
    description='A quantum entanglement visualizer',
    long_description='A Python package for visualizing quantum entanglement.',
    author='Minjong Kim',
    author_email='tlemsl@dgist.ac.kr',
    url='https://github.com/tlemsl/Entanglement_visualizer',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'numpy',
        # Add any other dependencies your project requires here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    cmdclass={'test': TestCommand},
)
