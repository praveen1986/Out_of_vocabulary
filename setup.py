from setuptools import setup, find_packages

setup(name='OOV',
      version='0.1',
      description='Out of vocabulary',
      author='Praveen Kulkarni',
      author_email='praveen.anil.kulkarni@gmail.com',
      packages=find_packages(),
      install_requires=[
        'numpy>=1.14.0',
        'scipy>=1.1.0',
        'gensim>=3.3.0'
      ]
     )