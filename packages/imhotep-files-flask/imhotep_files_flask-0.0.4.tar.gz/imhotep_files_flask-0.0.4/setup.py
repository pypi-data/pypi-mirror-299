from setuptools import setup, find_packages
 
classifiers = [
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='imhotep_files_flask',
  version='0.0.4',
  description='A Flask library for secure file uploads and deletions',
  long_description=open('README.md').read(),
  url='https://github.com/Imhotep-Tech/imhotep_files_flask',  
  author="Karim Bassem",
  author_email="imhoteptech@outlook.com",
  license='MIT', 
  classifiers=classifiers,
  keywords='files_flask', 
  packages=find_packages(),
  install_requires=['werkzeug'],
  long_description_content_type="text/markdown"
)