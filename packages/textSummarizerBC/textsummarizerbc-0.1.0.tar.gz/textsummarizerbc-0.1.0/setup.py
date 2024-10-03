# setup.py

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="textSummarizerBC",                  
    version="0.1.0",                        
    author="Chandra Mouli B",                     
    author_email="mouli9@example.com",  
    description="A text processing library using Hugging Face Transformers",
    long_description=long_description,      # Description from README.md
    long_description_content_type="text/markdown",  # README content type
    url="https://github.com/moulibc/textSummarizer",  # Your project URL
    packages=find_packages(),               
    classifiers=[                           
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                
    install_requires=[                      
        "transformers>=4.0.0",
        "torch",
    ],
)
