from setuptools import setup, find_packages

setup(
    name='scikits_learns',
    version='0.1.0',  # Increment version number
    packages=find_packages(),
    install_requires=[
        'openai>=0.27.0',
    ],
    author='Shaheer Zaman',
    author_email='shaheerzk@gmail.com',
    description='Random forest query enhancer using AI techniques',
    url='https://github.com/shaheerzk01/random_forest.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
