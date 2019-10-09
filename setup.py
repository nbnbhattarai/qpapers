from setuptools import setup, find_packages
import qpapers

setup(
    name='qpapers',
    version=str(qpapers.__VERSION__),
    packages=find_packages(),
    description='Find research papers across varios providers',
    long_description='''qpapers is a script to search paper across various publishers.''',
    url='https://blog.nabinbhattarai.com/qpapers/',
    author='Nabin Bhattarai',
    author_email='nbn.bhattarai99@gmail.com',
    license="MIT",
    install_requires=['beautifulsoup4', 'requests', 'PyYAML'],
    entry_points={
        'console_scripts': ['qpapers=qpapers.main:main'],
    },
    package_data={
        '': ['config.yml', ],
    }
)
