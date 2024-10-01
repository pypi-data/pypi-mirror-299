from setuptools import setup, find_packages

setup(
    name='jady',
    version='0.1.0',
    description='Uma breve descrição do pacote',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Douglasbm040/jady',
    author='Opythonista',
    author_email='douglasbm040@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[],
)
