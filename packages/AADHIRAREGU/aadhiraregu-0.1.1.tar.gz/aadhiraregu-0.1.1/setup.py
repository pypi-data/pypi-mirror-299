from setuptools import setup, find_packages

setup(
    name='AADHIRAREGU',  # Package name
    version='0.1.1',           # Package version
    description='A brief description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # If README is in Markdown
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/your_package',  # Project URL
    packages=find_packages(),  # Automatically find packages
    install_requires=[         # Dependencies
        # e.g. 'numpy', 'pandas'
    ],
    classifiers=[              # Metadata for PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',   # Python version requirements
)
