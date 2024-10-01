from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Telegram client in your favorite app: Terminal!'

# Setting up
setup(
    name="telecli",
    version=VERSION,
    author="ilpy",
    author_email="<ilpy@proton.me>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["pyrogram"]
)