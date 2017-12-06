from setuptools import setup

setup(
    name='named_decorator',
    description="""
    Utility to name wrappers based on their callees, dynamically. This makes it
    easy to trace calls in large codebases with heavily used decorators.
    """,
    url='https://github.com/Yelp/named_decorator',
    version='0.1.4',
    author='Yelp Performance Team',
    author_email='no-reply+use_github_issues@yelp.com',
    platforms='all',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    py_modules=['named_decorator'],
    options={
        'bdist_wheel': {
            'universal': 1,
        }
    },
)
