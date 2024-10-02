# setup.py

from setuptools import setup, find_packages

setup(
    name="whiteduck",
    version="0.1.1",
    author="Andre Ratzenberger",
    author_email="andre.ratzenberger@whiteduck.com",
    description="A tool to scaffold projects with Whiteduck's recommended tech stack",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/whiteduck",  # Replace with your repository URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",  # Include if you're using click
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "whiteduck=whiteduck.cli:cli",  # Use 'cli' if using click
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
