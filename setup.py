from setuptools import setup, find_packages

setup(
    name='blo',
    version='0.1',
    license='BSD-3-clause',
    author='Yann Savuir',
    author_email='savuir@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blo = blo.blog:main',
        ],
    },
    package_data={'': ['blo/default.json']},
    include_package_data=True,
    url='https://github.com/savuir/blo',  # use the URL to the github repo
    download_url='https://github.com/savuir/blo/tarball/0.1',  # I'll explain this in a second
    keywords=['blogging', 'blog', 'static blog generator'],  # arbitrary keywords
)