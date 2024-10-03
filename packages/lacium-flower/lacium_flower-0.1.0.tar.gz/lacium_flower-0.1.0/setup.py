from setuptools import setup, find_packages

setup(
    name='lacium-flower',
    version='0.1.0',
    description='Biblioteca de similaridade fonológica e semântica',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/usuario/lacium-flower',
    author='Geraldo Gomes',
    author_email='ggc4@cin.ufpe.br',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'nltk',
        'torch',
        'transformers',
        'scikit-learn',
        'python-Levenshtein',
        'pyphen'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
