from setuptools import setup, find_packages

setup(
    name='benchmanage',
    version='0.1.0',
    author='wolone',
    author_email='71954466@qq.com',
    description='Bench管理大师',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wolono/benchmanage',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask',
        'Flask-Login',
        'paramiko',
        'Flask-WTF',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    entry_points={
        'console_scripts': [
            'benchmanage=benchmanage.app:main',
        ],
    },
)