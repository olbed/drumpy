import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drumpy",
    version="0.0.4",
    description="Play drums on your keyboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/olbed/drumpy",
    packages=setuptools.find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'drumpy = drumpy.main:run',
        ],
    },
)
