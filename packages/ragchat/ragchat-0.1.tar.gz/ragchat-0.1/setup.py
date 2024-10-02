# from setuptools import find_packages, setup

# # Read requirements from requirements.txt
# with open('requirements.txt') as f:
#     requirements = f.read().splitlines()


# setup(
#     name='ragchat',
#     packages=find_packages(include=['ragchat']),
#     version='0.1.0',
#     description='This is the Retrieval Augmented Generation library.',
#     author='Me',
#     install_requires=requirements,
#     setup_requires=['pytest-runner'],
#     tests_require=['pytest==4.4.1'],
#     test_suite='tests',
# )


# setup.py
from setuptools import setup, find_packages

setup(
    name="ragchat",  # name of your package
    version="0.1",  # initial version
    packages=find_packages(),  # automatically find packages in your directory
    install_requires=[  # list dependencies from requirements.txt
        line.strip() for line in open("requirements.txt").readlines()
    ],
    description="A Retrieval-Augmented Generation chat library",
    long_description=open("README.md").read(),  # add description from README
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ragchat",  # replace with your GitHub URL
    author="team",
    author_email="your.email@example.com",
    classifiers=[  # additional metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',  # specify the Python version
)
