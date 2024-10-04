from setuptools import setup, find_packages

setup(
    name="twistor",  # Package name
    version="0.1.0",  # Initial release version
    description="A language or a package used to make discord bots..... :)",
    long_description=open('README.md').read(),  # You can add a README.md
    long_description_content_type='text/markdown',
    url="https://github.com/Siddhartha41210-git/Twistor",  # Link to your project’s homepage or repository
    author="Siddhartha41210",
    author_email="cooldevsiddhartha41210@gmail.com",
    license="MIT",  # Or your chosen license
    packages=find_packages(),  # Automatically find the twistor package
    install_requires=[  # Dependencies required for your package
        'discord.py>=2.0.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
