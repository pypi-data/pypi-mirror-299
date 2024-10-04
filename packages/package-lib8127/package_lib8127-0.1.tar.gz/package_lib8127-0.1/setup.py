# my_package/setup.py
from setuptools import setup, find_packages

setup(
    name='package_lib8127',
    version='0.1',
    packages=find_packages(),
    description='A package that runs custom code on import.',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/my_package',  # Укажите URL вашего репозитория
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
