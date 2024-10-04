from setuptools import setup, find_packages

setup(
    name='correlation_insight',
    version='0.1.0',
    description='Un package Python pour analyser la corrélation, incluant des tests de normalité, de linéarité, et des visualisations pour évaluer les relations entre variables.',
    author='CHABI ADJOBO AYEDESSO',
    author_email='aurelus.chabi@gmail.com',
    url='https://github.com/chabiadjobo/correlation_insight',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'statsmodels',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
)
