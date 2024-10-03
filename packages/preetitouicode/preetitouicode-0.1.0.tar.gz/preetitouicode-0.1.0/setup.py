from setuptools import setup, find_packages

setup(
    name='preetitouicode',  # The name of your package
    version='0.1.0',  # Version number
    packages=find_packages(),
    description='A Python package to convert Preeti encoded text to Unicode.',
    author='Bimarsha Mishra',
    author_email='bimarsha.mishra@gmail.com',
    url='https://github.com/bimarsha123/preetitounicode',  # URL to the project repository
    install_requires=[],  # Any dependencies (if any)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)