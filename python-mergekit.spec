Name:		python-mergekit
Version:	0.1.4
Release:	1
Summary:	Toolkit for merging pre-trained large language models
License:	LGPL-3.0-only
Group:		Development/Python
URL:		https://github.com/arcee-ai/mergekit
Source0:	https://files.pythonhosted.org/packages/source/m/mergekit/mergekit-%{version}.tar.gz
BuildArch:	noarch
BuildSystem:	python
BuildRequires:	python
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(setuptools)

# Runtime: cooker pins in pyproject are tighter than needed.
# Require what we actually ship; leave datasets unused-at-import optional.
Requires:	python%{pyver}dist(torch)
Requires:	python%{pyver}dist(transformers)
Requires:	python%{pyver}dist(tokenizers)
Requires:	python%{pyver}dist(huggingface-hub)
Requires:	python%{pyver}dist(peft)
Requires:	python%{pyver}dist(safetensors)
Requires:	python%{pyver}dist(accelerate)
Requires:	python%{pyver}dist(pydantic)
Requires:	python%{pyver}dist(immutables)
Requires:	python%{pyver}dist(click)
Requires:	python%{pyver}dist(tqdm)
Requires:	python%{pyver}dist(protobuf)
Requires:	python%{pyver}dist(typing-extensions)
Requires:	python%{pyver}dist(pyyaml)
Recommends:	python%{pyver}dist(sentencepiece)
Recommends:	python%{pyver}dist(scipy)
Requires:	python%{pyver}dist(datasets)

# Generator copies exact pins (click==8.2.1, tqdm==4.67.1, pydantic~=2.10,
# safetensors~=0.5, accelerate~=1.6) that reject cooker versions.
%global __requires_exclude ^python[0-9.]+dist\\((click|tqdm|pydantic|safetensors|accelerate|immutables)\\)

%description
mergekit merges Hugging Face / PyTorch language models (linear, SLERP,
TIES, DARE, task arithmetic, …) and can extract a LoRA adapter from
the difference between a fine-tune and its base:

  mergekit-yaml config.yml ./out
  mergekit-extract-lora --model finetune --base base ./lora-out

GGUF merge of an existing adapter is llama-export-lora (llama-cpp-examples).

%prep -a
python - <<'PY'
from pathlib import Path
p = Path("pyproject.toml")
t = p.read_text()
for a, b in [
    ('"tqdm==4.67.1"', '"tqdm>=4.67.1"'),
    ('"click==8.2.1"', '"click>=8.2.1"'),
    ('"safetensors~=0.5.2"', '"safetensors>=0.5.2"'),
    ('"accelerate~=1.6.0"', '"accelerate>=1.6.0"'),
    ('"pydantic~=2.10.6"', '"pydantic>=2.10.6"'),
    ('"immutables==0.21"', '"immutables>=0.21"'),
]:
    t = t.replace(a, b)
p.write_text(t)
print("patched mergekit pyproject.toml")
PY

%files
%doc README.md
%license LICENSE
%{_bindir}/mergekit-yaml
%{_bindir}/mergekit-legacy
%{_bindir}/mergekit-layershuffle
%{_bindir}/mergekit-moe
%{_bindir}/mergekit-tokensurgeon
%{_bindir}/mergekit-extract-lora
%{_bindir}/mergekit-evolve
%{_bindir}/mergekit-pytorch
%{_bindir}/mergekit-multi
%{_bindir}/bakllama
%{py_sitedir}/mergekit
%{py_sitedir}/mergekit-*.*-info
