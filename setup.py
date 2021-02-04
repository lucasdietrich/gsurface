import setuptools

with open("readme.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

setuptools.setup(
    name='gsurface',
    description='Simulate a surface-guided point mass motion according to the Newton 2nd Law Approach',
    version='0.0.1',
    author='Lucas DIETRICH',
    author_email='pro@ldietrich.fr',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Adecy/gsurface',
    packages=setuptools.find_packages(),
    license='GNU General Public License v3 (GPLv3)',
    python_requires='>= 3.8',
)
