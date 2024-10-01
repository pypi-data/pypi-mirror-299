import pathlib
from setuptools import setup, find_packages

location = pathlib.Path(__file__).parent
README = (location / "README.md").read_text()

setup(
    name="gaugedetect",
    version="0.0.2",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/pannawatr/gaugedetect",
    author="",
    author_email="",
    license="the8thfloor",
    packages=find_packages(),
    install_requires=["requests", "supabase", "numpy", "pillow", "pillow-heif", "python-dotenv"]
)