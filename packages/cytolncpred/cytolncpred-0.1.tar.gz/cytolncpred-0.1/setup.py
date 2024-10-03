from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='cytolncpred',
    version='0.1',
    description='A computational method to predict the probability of lncRNA localizing to cytoplasm',
    author='Gajendra P.S. Raghava',
    author_email='raghava@iiitd.ac.in',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE',),
    url='https://github.com/raghavagps/cytolncpred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'cytolncpred.nfeature':['*'],
    'cytolncpred.models':['*']},
    entry_points={ 'console_scripts' : ['cytolncpred = cytolncpred.python_scripts.cytolncpred:main']},
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[
        'numpy==2.1.1', 'pandas==2.2.3', 'scikit-learn==1.5.2', 'argparse', 'xgboost==2.1.1'  # Add any Python dependencies here
    ]
)
