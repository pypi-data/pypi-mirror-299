from setuptools import setup, find_packages 

setup(

    name='htask',
    description="This project helps to solve basics problems where you stuck every time because these are basic tasks and we forget it everytime then when suddenly asked by someone or during collage projects.This tool covers every basics problems such as fibnacci series , complex patterns, reverse string, find  duplicate values and more. ",   
    version='1.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    author='Ankush Kumar Rajput (Mr.Horbio)',
    url='https://github.com/MrHorbio/',
    youtube="https://www.youtube.com/@Mr-Horbio",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify Python versions
)
