from setuptools import setup

setup(
    name='named_decorator',
    description="""
    Utility to name wrappers based on their callees, dynamically. This makes it
    easy to trace calls in large codebases with heavily used decorators.
    """,
    url='TODO',
    version='0.0.1',
    author='Yelp Performance Team',
    author_email='team-perf@yelp.com',
    platforms='all',
    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    install_requires=['six'],
    py_modules=['named_decorator'],
    options={
        'bdist_wheel': {
            'universal': 1,
        }
    },
)
