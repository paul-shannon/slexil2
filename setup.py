import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

exec(open("src/slexil/version.py").read())

setuptools.setup(
    name='slexil_package',
    version = __version__,	
    author='Paul Shannon',
    author_email='paul.thurmond.shannon@gmail.com',
    description='Software Linking ELAN XML to Illuminated Language',
    keywords='slexil, ELAN, IJAL',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/paul-shannon/slexil2',
    install_requires=[
		'formatting',
		'numpy',
		'pandas',
		'xmlschema',
		'pyyaml',
		'yattag'],
    project_urls={
        'Documentation': 'https://github.com/paul-shannon/slexil2',
        'Bug Reports':
        'https://github.com/paul-shannon/slexil2/issues',
        'Source Code': 'https://github.com/paul-shannon/slexil2'
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        "License :: OSI Approved :: GPL License",
        "Operating System :: OS Independent",
    ]
)

