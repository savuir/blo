from setuptools import setup, find_packages


setup(
    name='blo',
    version='0.6',
    license='BSD-3-clause',
    author='Sajjad Shahcheraghian',
    author_email='shgninc@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'blo = blo.blog:main',
        ],
    },
    install_requires=['jinja2', 'markdown', 'PyRSS2Gen'],
    package_data={'': ['blo/default.json', 'blo/draft_templates.json',]},
    include_package_data=True,
    url='https://github.com/shgninc/blo',  # use the URL to the github repo
    download_url='https://github.com/savuir/blo/tarball/0.1',  # I'll explain this in a second
    keywords=['blogging', 'blog', 'static blog generator'],  # arbitrary keywords
)
