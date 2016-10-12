from setuptools import setup


setup(
    name = 'rankingscompare',
    version = '0.1.0',
    description = 'Rank correlation and similarity statistics',
    long_description = open('README.md').read(),
    url = 'https://github.com/jakesherman/rankingscompare',
    author = 'Jake Sherman',
    author_email = 'jake@jakesherman.com',
    install_requires = [
        'numpy',
    ],
    zip_safe = False)
