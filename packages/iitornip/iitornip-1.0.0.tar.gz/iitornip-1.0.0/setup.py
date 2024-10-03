from setuptools import setup

with open('README.md') as file:
    long_description = file.read()

setup(
    name='iitornip',
    version='1.0.0',
    packages=['iitornip'],
    url='https://github.com/vkvbit/iitornip',
    download_url='https://github.com/vkvbit/iitornip',
    license='MIT',
    author='Vaibhav Kumar',
    author_email='myselfv@hotmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['iitornip', 'onion', 'tor', 'tor nodes', 'tor exit nodes'],    
    entry_points={
        'console_scripts': [
            'iitornip = iitornip.__main__:cli'
         ]
    },
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Security',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'requests',
        'argparse',
        'os',
        'sys'
    ],
)