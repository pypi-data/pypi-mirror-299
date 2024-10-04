from setuptools import setup, find_packages

setup(
    name='beautifull_terminal',
    version='0.1',
    packages=find_packages(),
    description='Automatically beautify your terminal output with colors.',
    author='starcrusher2025',
    url='https://github.com/StarGames2025/beautifull_terminal',
    install_requires=[],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

#python setup.py sdist bdist_wheel
#twine upload dist/*