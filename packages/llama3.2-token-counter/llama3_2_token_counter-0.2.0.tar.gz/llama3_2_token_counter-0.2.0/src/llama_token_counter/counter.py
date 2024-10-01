import asyncio
import logging
from typing import Union, List, Optional
from pathlib import Path
from .custom_tokenizer import CustomTokenizer

logger = logging.getLogger(__name__)

class LlamaTokenCounter:
    def __init__(self, tokenizer_dir: Path):
        self.tokenizer_dir = tokenizer_dir
        self.tokenizer = CustomTokenizer(tokenizer_dir)

    def tokenize(self, text: str) -> List[int]:
        return self.tokenizer.encode(text)

    def get_max_tokens(self) -> int:
        return 131072  # Set the correct maximum token limit

    def count_tokens_sync(self, text: Union[str, List[str]], batch_size: Optional[int] = None) -> int:
        if isinstance(text, str):
            return len(self.tokenize(text))
        elif isinstance(text, list):
            if batch_size:
                total_tokens = 0
                for i in range(0, len(text), batch_size):
                    batch = text[i:i+batch_size]
                    total_tokens += sum(len(self.tokenize(t)) for t in batch)
                return total_tokens
            else:
                return sum(len(self.tokenize(t)) for t in text)
        else:
            raise ValueError("Input must be a string or a list of strings")