from setuptools import setup, find_packages

setup(
    name='cancer_package',  # Your package name
    version='0.1',
    packages=find_packages(),
    install_requires=[
        # List dependencies from your notebook here, for example:
        'pandas', 
        'numpy', 
        'matplotlib', 
        'scikit-learn'
    ],
    author='Mearn',
    author_email='mearn4240@gmail.com',
    description='A package for cancer-related analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/sanjeevi/cancer_package',  # GitHub or project homepage
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
