import os.path as osp
from distutils.core import setup
from setuptools import find_packages

#def get_requirements(filename='requirements.txt'):
#    here = osp.dirname(osp.realpath(__file__))
#    with open(osp.join(here, filename), 'r') as f:
#        requires = [line.replace('\n', '') for line in f.readlines()]
#    return requires

setup(
  name = 'eereid',         
  packages = find_packages(),
  version = '0.1.1',      
  license='apache-2.0',        
  description = 'Python module providing tools for training and evaluating re-identification models.',   
  author = 'Simon Klüttermann, Jérôme Rutinowski',                   
  author_email = 'Simon.Kluettermann@cs.tu-dortmund.de',      
  url = 'https://github.com/psorus/eereid',   
  download_url = 'https://github.com/psorus/eereid/archive/v_01.tar.gz',    
  keywords = ['Re-ID','Reidentification','Contrastive Learning','Metric Learning','Machine Learning','ML'],   
  install_requires=[],#get_requirements(),
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)

          #'tensorflow==2.11.*',
          #'numpy',
          #'scikit-learn',
          #'tqdm',
