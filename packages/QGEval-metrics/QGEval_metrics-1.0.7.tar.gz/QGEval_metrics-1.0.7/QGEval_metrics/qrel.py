import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/QRelScore')
from evalpackage.qrelscore import QRelScore

def corpus_qrel(preds, contexts, device='cuda',_mlm_model='model/bert-base-cased',_clm_model='model/gpt2'):
    assert len(contexts) == len(preds)
    mlm_model = _mlm_model
    clm_model = _clm_model
    scorer = QRelScore(mlm_model=mlm_model,
                   clm_model=clm_model,
                   batch_size=16,
                   nthreads=4,
                   device=device)
    scores = scorer.compute_score_flatten(contexts, preds)
    return scores
