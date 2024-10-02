from setuptools import setup, find_packages
import os
from setuptools.command.install import install
from subprocess import call

class PostInstallCommand(install):
    """Post-installation for downloading the model"""
    def run(self):
        # Run the standard install
        install.run(self)

        # Download the model after installation
        print("Running post-install tasks: Downloading model...")

        # Create a directory for the model if it doesn't exist
        model_dir = os.path.join(os.getcwd(), 'bourguiba', 'model')
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        # Ensure model is downloaded using the ModelDownloader
        # Replace with the correct command to download your model
        call(["python", "-m", "bourguiba.model_downloader"])

setup(
    name='bourguiba',
    version='3.1.3',  # Update version number
    packages=find_packages(),
    install_requires=[
        'transformers',
        'torch',
    ],
    entry_points={
        'console_scripts': [
            'bourguiba=bourguiba.bourguiba:main',
        ],
    },
    cmdclass={
        'install': PostInstallCommand,
    },
    author='Si Moahmed Aziz Bahloul, Wo Chrikou Il Mangouli Mahdi Magroun',
    description='Shell command generator using LLaMA model',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AzizBahloul/PromptToCommand',  # Your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
