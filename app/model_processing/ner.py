from config import settings
from pydantic_models.models import Entities

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForTokenClassification
import re

class Predictor:
    def __init__(self, tokenizer, model):
        self.tokenizer = tokenizer
        self.model = model

    def predict_all_entities(self, text: str, debug: bool = False) -> Entities:

        self.model.eval()
        if settings.use_cuda:
            device="cuda"
        else:
            device="cpu"

        words = []
        spans = []
        for match in re.finditer(r"\S+", text):
            words.append(match.group())
            spans.append(match.span())

        enc = self.tokenizer(
            words,
            is_split_into_words=True,
            return_tensors="pt",
            truncation=True
        )

        input_ids = enc["input_ids"].to(device)
        attention_mask = enc["attention_mask"].to(device)
        word_ids = enc.word_ids(batch_index=0)

        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
            logits = outputs.logits[0]               # (seq_len, num_labels)
            probs = F.softmax(logits, dim=-1)        # (seq_len, num_labels)

        results = []
        prev_word_idx = None
        for token_idx, word_idx in enumerate(word_ids):
            if debug:
                print(token_idx, word_idx, logits[token_idx])
            if word_idx is None:
                prev_word_idx = None
                continue

            # определяем по первому токену
            if word_idx != prev_word_idx:
                label_id = int(torch.argmax(logits[token_idx]).cpu().numpy())
                label = settings.id2label[label_id]

                start_idx, end_idx = spans[word_idx]
                results.append((start_idx, end_idx, label))

            prev_word_idx = word_idx

        return results
