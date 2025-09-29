import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    base_dir: str = os.getcwd()
    models_folder: str = "nlp_models"
    model_name: str = "rubert_tiny2_250925"
    model_dir: str = os.path.join(base_dir, models_folder, model_name)
    tokenizer_name: str = "rubert_tiny2_ft_250925_tokenizer"
    tokenizer_dir: str = os.path.join(base_dir, models_folder, tokenizer_name)
    use_cuda: bool = False
    env: str = "development"
    log_level: str = "DEBUg"

    lbls_in_dataset: list = [
        'O',
        'B-BRAND',
        'B-PERCENT',
        'B-TYPE',
        'B-VOLUME',
        'I-BRAND',
        'I-PERCENT',
        'I-TYPE',
        'I-VOLUME']
    label2id: dict = {v:i for i, v in enumerate(lbls_in_dataset)}
    id2label: dict = {i:v for i, v in enumerate(lbls_in_dataset)}

    class Config:
        env_file = ".env"

settings = Settings()
# print(settings.model_dir)