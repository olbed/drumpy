from setuptools import setup

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='drumpy',
    packages=['drumpy'],
    version='0.0.20',
    author='olbed',
    description='Play drums on your keyboard',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/olbed/drumpy',
    include_package_data=True,
    install_requires=[
        'pygame>=1.9.6,<2',
        'PyYAML>=5.3.1,<6',
    ],
    entry_points={
        'console_scripts': [
            'drumpy = drumpy.main:run',
        ],
    },
)
