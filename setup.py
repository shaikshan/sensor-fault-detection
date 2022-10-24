from setuptools import find_packages,setup
from typing import List

REQUIREMENTS_FILE_NAME = 'requirements.txt'

def get_requirements_list()->List[str]:
    """
    This function will return list of requirements
    """
    with open(REQUIREMENTS_FILE_NAME) as requirements_file:
        return requirements_file.readlines().remove("-e .")
        
setup(

    name= "sensor",
    version="0.0.3",
    author="roshan",
    author_email="shaikroshan1997@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements_list()
)
