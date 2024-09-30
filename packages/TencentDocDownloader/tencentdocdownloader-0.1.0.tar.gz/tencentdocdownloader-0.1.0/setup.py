from setuptools import setup, find_packages

setup(
    name='TencentDocDownloader',
    version='0.1.0',
    author='ChronoWalker',
    author_email='terrenceliao@hotmail.com',
    description='A tool to download Tencent documents, currently supports Excel documents.',
    long_description=open('README.md', encoding='utf-8').read(),  # Specify encoding
    long_description_content_type='text/markdown',
    url='https://github.com/kuloPo/TencentDocDownload',
    packages=find_packages(),
    install_requires=[
        'requests',
        'openpyxl',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)