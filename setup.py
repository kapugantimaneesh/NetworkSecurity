from setuptools import setup,find_packages
from typing import List

def find_requirements()->List[str]:
    try:
        requirements=[] 
        with open('requirements.txt','r') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                if requirement and requirement !='-e .':
                    requirements.append(requirement)

        
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirements


setup(
    name="NetworkSecurityProject",
    author="Maneesh",
    version="0.0.1",
    packages=find_packages(),
    install_requires=find_requirements()
)

