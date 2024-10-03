from setuptools import setup, find_namespace_packages


setup(
    name='classic-thread-pool-executor',
    version='1.0.0',
    description='',
    packages=find_namespace_packages('sources'),
    package_dir={'': 'sources'},
    extras_require={
        'dev': [
            'pytest~=8.3.2',
        ]
    }
)
