from setuptools import setup, find_packages

setup(
    name="pylon-desktop",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "PySide6",
    ],
    entry_points={
        "console_scripts": [
            "my-web-browser=my_web_browser.browser:run_browser",
        ],
    },
    author="aesthetics-of-record",
    author_email="aaaapple123@naver.com",
    description="desktop application for pylon",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aesthetics-of-record/pylon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)