from setuptools import setup, find_packages

version = "0.1.7"

setup(
    name='django_daisy',
    version='0.1.7',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # Add dependencies here
    description='A modern django dashboard built with daisyui',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hypy13/django-daisy',
    author='Hossein Yaghoubi',
    author_email='hossein.yaghoubi13@gmail.com',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
