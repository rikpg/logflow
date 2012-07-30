from setuptools import setup, find_packages

version = __import__('logflow').__version__

setup(
    name='logflow',
    version=version,
    author='Riccardo Poggi',
    author_email='rik.poggi@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/rikpg/logflow',
    license='BSD licence',
    description='Logging framework for Python.',
    long_description=open('README.md').read(),
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Logging',
    ),
    setup_requires=['nose'],
    tests_require=(
        'mock',
    ),
)
