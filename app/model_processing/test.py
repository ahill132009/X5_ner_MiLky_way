# from transformers import AutoTokenizer

# path = "/home/mikhail/Documents/Хакатоны/X5_ner_MiLky_way/app/nlp_models/rubert_tiny2_ft_250925_tokenizer"

# # Test 1: Can we load tokenizer from local dir?
# try:
#     tok = AutoTokenizer.from_pretrained(path, use_fast=True)
#     print("✅ Local tokenizer loaded!")
# except Exception as e:
#     print("❌ Local tokenizer failed:", e)

# # Test 2: Can we load from base model?
# try:
#     tok2 = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2", use_fast=True)
#     print("✅ Base tokenizer loaded!")
# except Exception as e:
#     print("❌ Base tokenizer failed:", e)

# tok2.save_pretrained(path)