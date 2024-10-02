from setuptools import setup

setup(
    name="gather_taxi_data",  # Replace with your package name
    version="0.1.0",  # Replace with your package version
    author="Wayne Bennett",
    author_email="wayne.bennett@live.com",
    description="Export data from web portals and save to database.",
    long_description=open("README.md").read(),  # Make sure you have a README.md file
    long_description_content_type="text/markdown",  # If you use Markdown for README
    url="https://github.com/WayneBennett666/gather-taxi-data",  # Replace with your project URL
    package_dir={"": "src"},  # Root ('') of the packages is under 'src'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Replace with the minimum Python version required
    install_requires=[
        "taxi_data_core",
        "selenium",
        "pydantic",
        "beautifulsoup4"
        # Add more dependencies as needed
    ],
    entry_points={
        "console_scripts": [
            "gather-taxi-data=gather_taxi_data.gather_all_data:main",  # Replace with your CLI commands if needed
        ],
    },
)