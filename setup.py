from setuptools import setup, find_packages

setup(
    name ='NLT',
    version ='1.0',
    description = 'Upload your projects to Github without leaving the terminal',
    author = 'Dibya Ranjan Jena',
    author_email = 'dibyajena917@gmail.com',
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
        'requests',
        'click',
        'colorama'
    ],
    entry_points='''
        [console_scripts]
        nlt=nlt_gb:cli
        
    ''',
)