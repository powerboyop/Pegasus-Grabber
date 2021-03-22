import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='EL1T3',
    version='0.1.9',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='EL1T3 GR4BB3R Module',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/Its-Vichy/EL1T3',
    install_requires=[
            'requests',
            'discord_webhook'
    ],
    author='Its_Vichy',
    author_email='Its_Vichy@protonmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)