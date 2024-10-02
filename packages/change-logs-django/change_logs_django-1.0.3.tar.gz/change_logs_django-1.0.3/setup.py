from setuptools import setup, find_packages

setup(
    name='change-logs-django',
    version='1.0.3',
    packages=find_packages(exclude=["demo*", "demoapp*"]),
    include_package_data=True,
    install_requires=[
        'django>=3.2',
    ],
    description='A Django app for managing release notes/ change logs for your project.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/OmerBhatti/change-logs-django',
    author='Omer Bhatti',
    author_email='omerbhatti340@gmail.com',
    license='MIT',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
