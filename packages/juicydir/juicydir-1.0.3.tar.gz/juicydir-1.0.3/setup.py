from setuptools import setup, find_packages, Command
import os
import shutil

class CleanCommand(Command):
    """Custom clean command to remove build artifacts."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Remove build artifacts from the previous build."""
        print("Cleaning up old build artifacts...")
        folders_to_clean = ['build', 'dist', 'juicydir.egg-info']
        for folder in folders_to_clean:
            if os.path.exists(folder):
                print(f"Removing {folder}")
                shutil.rmtree(folder)

setup(
    name='juicydir',
    version='1.0.3',
    description='Juicy Dir - Recursive File & Content Scanner',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Griffin Skaff',
    author_email='griffts@comcast.net',
    url='https://github.com/TraxionRPh/juicydir',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'juicydir=juicydir.juicydir:main',
        ],
    },
    install_requires=[
        'PyYAML',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    cmdclass={
        'clean': CleanCommand,
    }
)