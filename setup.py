from setuptools import setup

setup(
    name="configure-repositories",
    version="0.2.0",
    description="A command line interface to configure repositories of the Serlo organization",
    py_modules=["configure-repositories"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: CC0 1.0 Universal",
    ],
    install_requires=[
        "click",
    ],
    entry_points="""
        [console_scripts]
        configure_repositories=configure_repositories:cli
    """,
)
