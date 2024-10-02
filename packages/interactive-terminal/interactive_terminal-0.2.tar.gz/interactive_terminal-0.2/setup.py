from setuptools import setup, find_packages
import os

setup(
    name='interactive_terminal',                      # Name of the package
    version='0.2',                                   # Initial version of the package
    packages=find_packages(),                         # Automatically find and list all packages
    install_requires=['colorama'],                    # Dependencies required for your package
    description='An interactive terminal question and answer module.',  # Short description
    author='Aiden Metcalfe',                          # Your name
    author_email='avaartshop@outlook.com',           # Your email
    long_description=open(os.path.join('docs', 'README.md'), 'r').read(),  # Read the contents of README.md
    long_description_content_type='text/markdown',   # Specify the format of the long description
    classifiers=[                                     # Classifiers to help users find your package
        'Development Status :: 3 - Alpha',           # Current development status
        'Intended Audience :: Developers',            # Target audience
        'License :: OSI Approved :: MIT License',     # License type
        'Programming Language :: Python :: 3',        # Compatible Python versions
    ],
)