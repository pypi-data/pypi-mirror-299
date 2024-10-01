from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name="NumTextAlchemy",  # Your package name
    version="0.1.1",  # Version of your package
    author="Srinath Gudi",  # Your name
    author_email="srinathngudi11@gmail.com",  # Your email
    description="NumTextAlchemy is a Python library designed to convert extremely large numbers into their text representations and back to their numerical form.",  # Short description
    long_description=long_description,  # Long description from README.md
    long_description_content_type="text/markdown",
    url="https://github.com/Srinath-N-Gudi/NumTextAlchemy",  # GitHub or project URL
    packages=[
        'NumTextAlchemy'
    ],  # Automatically find packages in your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    license='MIT',
    python_requires=">=3.0",  # Python version requirement
    include_package_data=True,  # Include files listed in MANIFEST.in
)
