from setuptools import setup, find_packages

setup(
    name='pyexcreporter',
    version='0.1',
    packages= find_packages(),
    include_package_data=True,
    install_requires=[
        
    ],
    extra_require={
        'dev': [
            'twine>=3.4.1',
            'wheel>=0.37.1',
        ],
        
    },
    description='An exception reporter utility.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mohamed Zaki',
    author_email='zaki.x86@gmail.com',
    url='https://github.com/zaki-x86/pyexcreporter.git',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    license=open('LICENSE').read(),
    zip_safe=False,
)
