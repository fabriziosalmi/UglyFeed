from setuptools import setup, find_packages

# Reading the long description from the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='uglypy',  # The package name on PyPI
    version='0.0.27',  # Initial version, update manually for major changes
    author='Fabrizio Salmi',
    author_email='fabrizio.salmi@gmail.com',  # Replace with your email
    description='A Python package for aggregating and processing RSS feeds with LLM-enhanced content rewriting.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fabriziosalmi/UglyFeed',  # Correct key for homepage
    project_urls={
        "Bug Tracker": "https://github.com/fabriziosalmi/UglyFeed/issues",
        "Documentation": "https://github.com/fabriziosalmi/UglyFeed/blob/main/docs",
        "Source Code": "https://github.com/fabriziosalmi/UglyFeed",
    },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Ensure compatibility with Python 3.7 and above
    install_requires=[
        'beautifulsoup4==4.12.3',
        'EbookLib==0.18',
        'feedgen==1.0.0',
        'feedparser==6.0.11',
        'jiwer==3.0.4',
        'joblib==1.4.0',
        'langdetect==1.0.9',
        'lexical_diversity==0.1.1',
        'nltk==3.8.1',
        'numpy==1.24.4',
        'openai==1.30.5',
        'pandas==2.2.2',
        'psutil==5.9.8',
        'PyYAML==6.0.1',
        'requests==2.32.3',
        'scikit_learn==1.4.2',
        'sentence_transformers==2.7.0',
        'spacy==3.7.0',
        'textblob==0.18.0.post0',
        'textstat==0.7.3',
        'tqdm==4.66.3',
        'typer==0.9.0',
        'streamlit',  # No specific version required, latest will be installed
        'schedule',
    ],
    entry_points={
        'console_scripts': [
            'uglypy=uglypy.cli:main',
        ],
    },
    license='AGPL-3.0',  # Specify the license type
)
