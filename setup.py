from setuptools import setup, find_packages
import qpapers

setup(
    name='qpapers',
    version=str(qpapers.__VERSION__),
    packages=find_packages(),
    description='qpapers: find research papers across varios providers',
    long_description='''qpapers is a script to search paper across various publishers.''',
    url='https://blog.nabinbhattarai.com/qpapers/',
    license="MIT",
    install_requires=['beautifulsoup4', 'requests'],
    entry_points={
        'console_scripts': ['qpapers=qpapers.main:main'],
    }
)
