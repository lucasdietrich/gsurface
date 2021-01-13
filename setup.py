from setuptools import setup

setup(
    name='gsurface',
    description='Simulate surface guided mass points',
    version='0.0.1',
    packages=['gsurface', 'gsurface.forces', 'gsurface.plotter', 'gsurface.surface'],
    url='ldietrich.fr/gsurface',
    license='GPLv3',
    author='Lucas DIETRICH',
    author_email='pro@ldietrich.fr',
    python_requires='>= 3.8'
)
