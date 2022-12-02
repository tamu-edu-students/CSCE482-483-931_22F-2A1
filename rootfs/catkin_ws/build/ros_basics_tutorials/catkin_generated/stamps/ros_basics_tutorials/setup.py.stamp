

from catkin_pkg.python_setup import generate_distutils_setup
# fetch values from package.xml
from setuptools import find_packages, setup, Command
REQUIRES_PYTHON = '>=3.6.0'

setup(
    version='0.0.0',
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=["ros_essentials_cpp", "ros_msg", "ros ","*.tests", "*.tests.*", "tests.*"]),
    package_dir={'': 'src'}
)

