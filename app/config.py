from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import cached_property
import os
import torch

class Settings(BaseSettings):
    """Application settings with Docker and environment variable support."""
    
    # Base paths - can be overridden via environment variables
    base_dir: Path = Path.cwd()
    models_folder: str = "prod_models"
    
    # Model configuration
    model_name: str = "distilrubert_optuna_ft_09344"
    tokenizer_name: str = "distilrubert_optuna_ft_09344"
    
    # Runtime settings
    use_cuda: bool = True if torch.cuda.is_available() else False
    env: str = "development"
    log_level: str = "DEBUG"
    
    # NER labels - class variable (doesn't need to be configurable)
    LABELS: list[str] = [
        'O',
        'B-BRAND',
        'B-PERCENT',
        'B-TYPE',
        'B-VOLUME',
        'I-BRAND',
        'I-PERCENT',
        'I-TYPE',
        'I-VOLUME'
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Computed properties using cached_property for efficiency
    @cached_property
    def model_dir(self) -> Path:
        """Full path to model directory."""
        if os.path.exists(self.base_dir / self.models_folder / self.model_name):
            return self.base_dir / self.models_folder / self.model_name
        else:
            return self.model_name

    @cached_property
    def tokenizer_dir(self) -> Path:
        """Full path to tokenizer directory."""
        print(self.base_dir / self.models_folder / self.tokenizer_name)
        if os.path.exists(self.base_dir / self.models_folder / self.tokenizer_name):
            return self.base_dir / self.models_folder / self.tokenizer_name
        else:
            return self.model_name
    
    @cached_property
    def label2id(self) -> dict[str, int]:
        """Mapping from label to ID."""
        return {label: idx for idx, label in enumerate(self.LABELS)}
    
    @cached_property
    def id2label(self) -> dict[int, str]:
        """Mapping from ID to label."""
        return {idx: label for idx, label in enumerate(self.LABELS)}
    
    # def validate_paths(self) -> None:
    #     """Validate that required directories exist."""
    #     if not self.model_dir.exists():
    #         raise FileNotFoundError(f"Model directory not found: {self.model_dir}")
    #     if not self.tokenizer_dir.exists():
    #         raise FileNotFoundError(f"Tokenizer directory not found: {self.tokenizer_dir}")
    
    def __repr__(self) -> str:
        return (
            f"Settings(env={self.env}, model_dir={self.model_dir}, "
            f"use_cuda={self.use_cuda})"
        )


# Singleton instance
settings = Settings()
print(settings)