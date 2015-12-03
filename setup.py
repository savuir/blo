from setuptools import setup, find_packages

setup(
    name='blo',
    version='0.1',
    license='BSD-3-clause',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blo = blo.blog:main',
        ],
    },
    package_data={'': ['blo/default.json']},
    include_package_data=True,
)