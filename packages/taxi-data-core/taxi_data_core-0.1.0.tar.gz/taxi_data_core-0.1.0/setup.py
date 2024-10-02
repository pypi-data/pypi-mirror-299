from setuptools import setup, find_packages

setup(
    name="taxi_data_core",  # Replace with your package name
    version="0.1.0",  # Replace with your package version
    author="Wayne Bennett",
    author_email="wayne.bennett@live.com",
    description="Core modules for taxi_data funcitonality.",
    long_description=open("README.md").read(),  # Make sure you have a README.md file
    long_description_content_type="text/markdown",  # If you use Markdown for README
    url="https://github.com/WayneBennett666/taxi-data-core",  # Replace with your project URL
    packages=find_packages(where='src'),
    package_dir={"": "src"},  # Root ('') of the packages is under 'src'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Replace with your license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",  # Replace with the minimum Python version required
    install_requires=[
        "selenium",
        "pydantic",
        "beautifulsoup4",
        "google-auth",
        "google-auth-oauthlib",
        "google-api-python-client",
        "xero-python",
        "pandas"
        # Add more dependencies as needed
    ],
)