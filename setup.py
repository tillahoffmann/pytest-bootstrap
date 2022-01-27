from setuptools import find_packages, setup


setup(
    name='pytest-bootstrap',
    packages=find_packages(),
    version='0.1.0',
    install_requires=[
        'numpy',
    ],
    extras_require={
        'tests': [
            'flake8',
            'pytest',
            'pytest-cov',
            'scipy',
        ],
        'docs': [
            'matplotlib',
            'sphinx',
        ]
    },
    classifiers=[
        'Framework :: Pytest',
    ],
)
