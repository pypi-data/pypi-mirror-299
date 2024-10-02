from setuptools import setup, find_packages

setup(
    name='mehdi_test',
    version='0.1.5',
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Mehdi Hamzeluie',
    author_email='mehdihamze73@gmail.com',
    url='https://github.com/Hamzeluie/your_project',
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
        'numpy',
        'pandas',
        # ...
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    python_requires='>=3.6',
)
