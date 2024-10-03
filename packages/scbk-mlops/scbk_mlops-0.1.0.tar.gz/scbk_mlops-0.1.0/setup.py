from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename) as f:
        return f.read().splitlines()

setup(
    name='scbk_mlops',
    version='0.1.0',
    author='Jong Hwa Lee, Jin Young Kim', 
    author_email='jonghwa.jh.lee@sc.com, jinyoung.jy.kim@sc.com',
    description='Local version of MLOps intended for limited capabilities (no DB connection) under network segregation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/scbk-datascience/scbk-mlops',
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=parse_requirements('requirements.txt'), # Issue 생기면 바꾸기
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
