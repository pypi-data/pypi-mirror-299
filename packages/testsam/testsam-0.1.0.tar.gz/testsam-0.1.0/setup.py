from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    description = fh.read()

setup(
    name='testsam',
    version='0.1.0',
    author='Simron Senapati',
    author_email='simronsenapati@gmail.com',
    description='A extended vacuum library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mylib',
    packages=find_packages(),
    install_requires=[],
    # classifiers=[
    #     'Programming Language :: Python :: 3',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
    python_requires='>=3.6',
)
