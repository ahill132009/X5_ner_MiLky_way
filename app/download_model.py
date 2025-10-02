import yaml
from transformers import AutoModel, AutoTokenizer
import os

# Load config
with open('./env.yaml') as f:
    config = yaml.safe_load(f)

model_id = config['model_dir']
safe_name = model_id.replace('/', '__')
save_path = '/code/nlp_models/' + safe_name

# Ensure directory exists
os.makedirs(save_path, exist_ok=True)

print('Downloading model:', model_id)
model = AutoModel.from_pretrained(model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id)

model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)

print('✅ Model and tokenizer saved to', save_path)