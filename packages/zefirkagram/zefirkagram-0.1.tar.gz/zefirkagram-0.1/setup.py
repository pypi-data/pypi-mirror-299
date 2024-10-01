from setuptools import setup

setup(
    name='zefirkagram',
    version='0.1',
    package_dir={'zefirkagram': 'src'},
    packages=['zefirkagram'],
    install_requires=[
        'requests',
    ],
    description='A simple Telegram bot to send messages and pictures to a Telegram channel',
    author='Resonaura',
    author_email='resonaura@gmail.com',
    url='https://github.com/resonaura/zefirkagram',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
