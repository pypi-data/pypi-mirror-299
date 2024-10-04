from setuptools import setup, find_packages
import os

version_folder = os.path.dirname(os.path.join(os.path.abspath(__file__)))

with open(os.path.join(version_folder, 'verl/version/version')) as f:
    __version__ = f.read().strip()

# TODO: add version info to requirements
install_requires = [
    'tensordict>=0.3.0,<0.3.1',
    'transformers',
    'codetiming',
    'pybind11',
    'hydra-core',
    'numpy',
    'pytest',
    'yapf',
    "dill",
    "accelerate"
]

install_optional = [
    'vllm==0.5.4',
    'liger-kernel'
]

extras_require = {
    'demo': ['hydra-core', 'transformers', ''],
    'single-controller': ['ray', 'kubernetes'],
    'single-controller-ray': ['ray'],
}

setup(
    name='verl',
    version=__version__,
    package_dir={'': '.'},
    packages=find_packages(where='.'),
    url='https://github.com/volcengine/verl',
    license='Apache 2.0',
    author='Bytedance - Seed - MLSys',
    author_email='zhangchi.usc1992@bytedance.com, gmsheng@connect.hku.hk',
    description='VeRL: Volcano Engine Reinforcement Learning for LLM',
    install_requires=install_requires,
    extras_require=extras_require,
    package_data={'': ['version/*']},
    include_package_data=True,
)
