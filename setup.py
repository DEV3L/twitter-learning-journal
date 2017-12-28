from setuptools import setup, find_packages

setup(
    name='twitter-learning-journal',
    packages=find_packages(),
    version='0.1',
    description='Qualify learnings of a Twitter account as a learning journal.',
    author='Justin Beall',
    author_email='jus.beall@gmail.com',
    url='https://github.com/DEV3L/twitter-learning-journal',
    download_url='https://github.com/DEV3L/twitter-learning-journal/tarball/0.1',
    keywords=['dev3l', 'tweepy', 'learning', ],
    install_requires=[
        'beautifulsoup4',
        'sqlalchemy',
        'tweepy',
        'pytest',
        'bandit',
        'coveralls',
        'coverage',
        'pylint',
        'tox'
    ],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
