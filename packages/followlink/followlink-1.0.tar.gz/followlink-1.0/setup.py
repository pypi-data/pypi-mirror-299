from setuptools import setup, find_packages

setup(
    name='followlink',
    version='1.0',
    description='A tool to follow URL redirects and analyze response codes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/malwarekid/followlink',
    author='Nitin Sharma',
    author_email='nitinsharmahd123@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'requests',
        'colorama',
    ],
    entry_points={
        'console_scripts': [
            'followlink=FollowLink.followlink:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
