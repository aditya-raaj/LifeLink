from setuptools import find_packages,setup
from typing import List
HYPHEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
        THIS FUNCTION WILL RETURN THE LIST OF REQUIREMENTS
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        [req.replace("\n","") for req in requirements]
        if HYPHEN_E_DOT in requirements:
             requirements.remove(HYPHEN_E_DOT)
        return requirements

setup(
    name='LifeLink',
    version='0.0.1',
    author='Aditya',
    author_email='rajaditya0024@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)