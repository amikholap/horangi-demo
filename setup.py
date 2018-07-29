from setuptools import find_packages, setup

setup(
    name='horangi-demo',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'cassandra-driver==3.14.0',
        'Django==2.0.7',
        'djangorestframework==3.8.2',
        'uWSGI==2.0.17.1',
    ],
)
