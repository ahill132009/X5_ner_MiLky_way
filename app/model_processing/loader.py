from transformers import pipeline
from typing import Optional
from config import settings
from transformers import AutoTokenizer, AutoModelForTokenClassification


class Model:
    def __init__(self, model_path, tokenizer_path):
        self.model_path = model_path
        self.tokenizer_path = tokenizer_path
        if settings.use_cuda:
            self.device="cuda"
        else:
            self.device="cpu"

    def init_model(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path, 
                                                             use_fast=True, 
                                                             add_prefix_space=True)
        self.model = AutoModelForTokenClassification.from_pretrained(self.model_path).to(self.device)
        return self.tokenizer, self.model
