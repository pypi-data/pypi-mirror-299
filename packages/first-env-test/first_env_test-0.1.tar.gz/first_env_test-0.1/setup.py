from setuptools import setup, find_packages, Command  
from setuptools.command.install import install  
import os  

class PostInstallCommand(install):  
    """Post-installation for installation mode."""  
    def run(self):  
        install.run(self)
        print("Post-installation script is running...")  
        print("Environment Variables:")  
        for key, value in os.environ.items():  
            print(f"{key}: {value}")  

setup(  
    name='first_env_test',  
    version='0.1',  
    packages=find_packages(),  
    author='Your Name',  
    author_email='your_email@example.com',  
    description='A package that prints environment variables during installation',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.6',  
    cmdclass={  
        'install': PostInstallCommand,  
    },  
)