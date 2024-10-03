from setuptools import setup, find_packages

setup(
    name='localcloudforge',
    version='0.2.0',
    author='João Vitor de Faria',
    author_email='joao.faria@profusion.mobi',
    description='A tool for developing and testing AWS service integrations locally.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/joaovitorgit/LocalCloudForge',
    packages=find_packages(),
    install_requires=[
        'boto3>=1.34.123',
        'localstack-client>=2.6'
    ],
    classifiers=[],
    python_requires='>=3.11.4',
)
