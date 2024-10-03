from setuptools import setup, find_packages

setup(
    name='trust_sign',
    version='0.1',
    packages=find_packages(),
    description='A library for data tokenization and detokenization',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Mouhawos/Trust-Sign',
    author='Spidercrypt',
    author_email='spidercrypt.dev@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'Flask', 'requests', 'jsonify'
    ],
)
