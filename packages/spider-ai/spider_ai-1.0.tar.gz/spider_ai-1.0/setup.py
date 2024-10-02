from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='spider-ai',
  version='1.0',
  description='lib python for AI',
  author='spiderXR',
  license='MIT', 
  classifiers=classifiers,
  keywords='spider-ai', 
  packages=find_packages(),
  install_requires=[''] 
)
