from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="GhReviewer",
    version="0.1.0",
    description="A tool for systematically reviewing GitHub repositories",
    author="Jon Cavallie Mester",
    author_email="jonmester3@gmail.com",
    packages=find_packages(),
    py_modules=["github_review_app"],
    install_requires=required,
    entry_points={
        'console_scripts': [
            'ghreview=github_review_app:main',
        ],
    },
)
