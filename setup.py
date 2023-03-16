from setuptools import setup

setup(
    name='named_decorator',
    description="""
    Utility to name wrappers based on their callees, dynamically. This makes it
    easy to trace calls in large codebases with heavily used decorators.
    """,
    url='https://github.com/Yelp/named_decorator',
    version='0.2.0',
    author='Yelp Performance Team',
    author_email='no-reply+use_github_issues@yelp.com',
    python_requires='>=3.8',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    py_modules=['named_decorator'],
)
