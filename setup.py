from setuptools import setup, find_packages

long_description = ""
with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='font2img',
    version='2.1',
    packages=find_packages(),
    description="Drawing glyph in font file (woff, tff ..) ",
    long_description = long_description,
    long_description_content_type='text/markdown',
    author='coderfly,magicalbomb',
    author_email='coderflying@163.com,3379747207@qq.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules = ["font2img"],
    python_requires = '>=3.5',
    install_requires=['pillow', 'fonttools', 'reportlab'],
)