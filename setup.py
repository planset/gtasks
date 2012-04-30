from setuptools import setup, find_packages

setup(
    name='gtasks',
    version='0.1',
    description='google tasks ui',
    author='Daisuke Igarashi',
    author_email='planset@gmail.com',
    url='htp://lowlevellife.com',
    license='BSD',
    scripts=['bin/gtasks'],
    install_requires=[
        "google-api-python-client",
        ],
    packages=find_packages(),
)


