RQUGE🤗: Reference-Free Metric for Evaluating Question Generation by Answering the Question
=================
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-red.svg)](#python)
[![arxiv](https://img.shields.io/badge/arXiv-2211.01482-b31b1b.svg)](https://arxiv.org/abs/2211.01482)
[![PyPI version bert-score](https://badge.fury.io/py/rquge.svg)](https://pypi.python.org/pypi/rquge/)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) 

<p align="center">
  <img src="meta.jpeg" width="500"/>
</p>

We propose RQUGE, a **R**eference-free **QU**estion **G**eneration **E**valuation metric that can compute the quality of the candidate question without requiring the access to the reference question. Given the corresponding context and answer span, our metric calculates the acceptability score by applying a general question-answering module, followed by a span scorer. You can find more detail in [the paper](https://arxiv.org/abs/2211.01482) (ACL2023).

<p align="center">
  <img src="main_model.jpg" width="700"/>
</p>


Contents
---------------

- [Huggingface Evaluate🤗](#hf_evaluate)
- [Installation](#install)
- [Calculation](#calculation)
- [Citation](#citation)

<a name="hf_evaluate"/>  

HuggingFace Evaluation 🤗
--------------  

RQUGE score is available on [Huggingface Evaluate](https://huggingface.co/docs/evaluate/index). It can be used as:

```
from evaluate import load
rqugescore = load("alirezamsh/rquge")
generated_questions = ["how is the weather?"]
contexts = ["the weather is sunny"]
answers = ["sunny"]
results = rqugescore.compute(generated_questions=generated_questions, contexts=contexts, answers=answers)
print(results["mean_score"])
>>> [5.05]
```

The demo and further details are also available on [here](https://huggingface.co/spaces/alirezamsh/rquge). (```device``` argument can be used to run RQUGE on GPU/CPU. Default is CPU)

<a name="install"/>  

Installation
--------------  

You should have the following packages:

- transformers
- pytorch
- sentencepiece

Install from pypi with pip by
```
pip install rquge
```
Install latest unstable version from the master branch on Github by:
```
pip install git+https://github.com/alirezamshi/RQUGE
```
Install it from the source by:
```
git clone https://github.com/alirezamshi/RQUGE
cd RQUGE
pip install .
```

Note: you need to download the pre-trained model for the span scorer module (available on [Huggingface](https://huggingface.co/alirezamsh/quip-512-mocha)🤗 ```alirezamsh/quip-512-mocha```):
```
wget https://storage.googleapis.com/sfr-qafacteval-research/quip-512-mocha.tar.gz
tar -xzvf quip-512-mocha.tar.gz
rm quip-512-mocha.tar.gz
```

<a name="calculation"/>  

RQUGE Calculation
-------------- 

#### Python Function
The RQUGE class is provided in ```rquge_score/scorer.py```. We also provide a python function in ```rquge_score_cli/scorer_cli.py``` to use different features of RQUGE metric.

#### Command Line Interface (CLI)
We provide a command line interface (CLI) of RQUGE, you can use it as follows:
```
rquge --input_type #MODE --sp_scorer_path #PATH_TO_SPAN_SCORER --qa_model_path #PATH_TO_QA_MODEL --context #CONTEXT_FILE --question #QUESTION --answer #ANSWER --output_path #OUTPUT

#MODE: The type of input (sample or offline). In the sample mode, "--context", "--question", and "--answer" commands contain string, while in offline mode, they contain path to files including contexts, corresponding questions and answers
#PATH_TO_SPAN_SCORER: path to the local checkpoint of span scorer model or "alirezamsh/quip-512-mocha"
#PATH_TO_QA_MODEL: name of QA model on Huggingface or local path 
#CONTEXT_FILE: a text file containing one context per line (directly in the input in "sample" mode)
#QUESTION_FILE: a text file containing one question per line (directly in the input in "sample" mode)
#ANSWER_FILE: a text file containing one answer per line (directly in the input in "sample" mode)
#OUTPUT: local path for saving RQUGE scores for each (context,question,answer) pair
```

Here is a sample score computation for the interactive mode

```
rquge --input_type sample --sp_scorer_path ckpt/quip-512-mocha --qa_model_path 'allenai/unifiedqa-v2-t5-large-1363200' --context "the weather is sunny" --question "how is the weather?" --answer sunny
```

**Note:** the rquge score is between 1 to 5.

<a name="citation"/>  

Citation
-------------

<a name="citations"/>  

If you use this code for your research, please cite the following work:
```
@misc{mohammadshahi2022rquge,
    title={RQUGE: Reference-Free Metric for Evaluating Question Generation by Answering the Question},
    author={Alireza Mohammadshahi and Thomas Scialom and Majid Yazdani and Pouya Yanki and Angela Fan and James Henderson and Marzieh Saeidi},
    year={2022},
    eprint={2211.01482},
    archivePrefix={arXiv},
    primaryClass={cs.CL}
}
```
Have a question not listed here? Open [a GitHub Issue](https://github.com/alirezamshi/RQUGE/issues) or 
send us an [email](alireza.mohammadshahi@idiap.ch).
