from setuptools import setup, find_packages

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except:
        pass

setup(
    name ='NLT',
    version ='1.0',
    description = 'Upload your projects to Github without leaving the terminal',
    author = 'Dibya Ranjan Jena',
    author_email = 'dibyajena917@gmail.com',

    long_description=readme(),  
    long_description_content_type='text/markdown',
    
    packages = find_packages(),
    include_package_data = True,
    install_requires=[
        'requests',
        'click',
        'colorama',
        'windows-curses;platform_system=="Windows"',
        'pick',
        'cryptography',
        'prettytable',
        'gitpython'
    ],
    entry_points='''
        [console_scripts]
        nlt=nlt_gb:cli
        
    ''',
)