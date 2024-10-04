# VeRL: Volcano Engine Reinforcement Learning for LLM
Current status: under heavy development

## Installation
As development mode
```bash
pip3 install -e . --user
```


pypi repo: TODO

### Dependencies
Lightweight dependencies are in setup.py and will be installed during installation of verl. Other dependencies include
```bash
# flash attention 2
pip3 install flash-attn --no-build-isolation
# megatron
bvc clone aml/mlsys/megatron;
cd megatron;
pip3 install -e . --user
# apex
pip3 install -v --disable-pip-version-check --no-cache-dir --no-build-isolation \
         --config-settings "--build-option=--cpp_ext" --config-settings "--build-option=--cuda_ext" \
         git+https://github.com/NVIDIA/apex

```


## Contribution
### Code formatting
We use yapf (Google style) to enforce strict code formatting when reviewing MRs. To reformat you code locally, make sure you installed `yapf`
```bash
pip3 install yapf
```
Then, make sure you are at top level of verl repo and run
```bash
yapf -ir -vv --style ./.style.yapf verl tests single_controller examples
```