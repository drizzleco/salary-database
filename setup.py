from setuptools import find_packages
from setuptools import setup

setup(
    name="backend",
    version="1.0.0",
    maintainer="Drizzle",
    description="Salary Database Backend",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
