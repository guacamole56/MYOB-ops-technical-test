from setuptools import setup

from myob_ops_technical_test.config import VERSION

version = VERSION

setup(
    name='MYOB-Ops-Technical-Test',
    version=version,
    packages=['myob_ops_technical_test'],
    include_package_data=True,
    install_requires=[
        'flask >= 0.12',
    ],
)
