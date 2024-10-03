from setuptools import setup, find_packages

setup(
    name="Publicis.AI.Transformer.Spreadsheet",
    version="1.0.0",
    packages=find_packages(),
    license="MIT",
    entry_points={
        'console_scripts': [
            'my_start=Main.AI.Transformer.Spreadsheet',  ## Project Entry-point e.g. 'my_start=<your Main.py filename>:<Main function name>'
        ],
    },
    author="RAGHU",
    author_email="RAGHU.SINGH@PUBLICISRESOURCES.COM",
    description="An AI-based Conversion Tool, an R&D project",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Python Software Foundation License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
    ],
    python_requires='>=3.6',
)
