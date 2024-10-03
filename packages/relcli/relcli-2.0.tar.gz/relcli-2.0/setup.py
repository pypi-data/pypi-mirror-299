from setuptools import setup, find_packages

setup(
    name='relcli',
    version='2.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3',
        'click',
        'pyperclip',
        'rich',
        'prompt_toolkit',
        'setuptools>=40.8.0',
    ],
    entry_points='''
        [console_scripts]
        dash=dashcli.dashcli:dashcli
        #clicommand=folderName.fileName:mainFunctionName
    ''',
    author='Siddharth Rao',
    author_email='isiddharthrao@gmail.com',
    description='A custom CLI tool for Relatient users to manage the AWS ECS clusters and connecting to PostgreSQL databases',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/isiddharthrao',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)
