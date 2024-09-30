from setuptools import setup, find_packages


setup(
  name='solverpack',
  version='0.0.1',
  author='mikhail_rozhkov',
  description='Package solver.',
  packages=find_packages(),
  install_requires=['pandas==2.2.2',
                    'sqlalchemy==2.0.35',
                    'psycopg2==2.9.9'],
)