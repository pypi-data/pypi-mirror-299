import json
import functools
from typing import List, Union, Dict, Any, Optional, Coroutine
from pathlib import Path
import logging
import asyncio
from transformers import PreTrainedTokenizerFast

def require_tokenizer(func):
    """
    @brief Decorator to check if tokenizer is initialized before calling a method.
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.tokenizer is None:
            raise ValueError("Tokenizer is not properly initialized")
        return func(self, *args, **kwargs)
    return wrapper

class LlamaTokenCounter:
    """
    @brief A class for counting tokens in text using the Llama tokenizer.
    
    @details This class provides methods to count tokens and tokenize strings or lists of strings,
    with support for both synchronous and asynchronous operations. It handles large inputs
    efficiently using the tokenizer's batch processing capabilities and caching.
    """

    def __init__(self, tokenizer_dir: Union[str, Path] = None):
        """
        @brief Initialize the LlamaTokenCounter.
        
        @param tokenizer_dir: Path to the directory containing tokenizer files.
        If None, uses the default path.
        @throws ValueError: If required files are missing or cannot be loaded.
        """
        if tokenizer_dir is None:
            tokenizer_dir = Path(__file__).parent / "tokenizer"
        
        self.tokenizer_dir: Path = Path(tokenizer_dir)
        if not self.tokenizer_dir.exists():
            raise ValueError(f"Tokenizer directory not found: {self.tokenizer_dir}")
        
        required_files = [
            "tokenizer.json",
            "tokenizer_config.json",
        ]

        for file in required_files:
            if not (self.tokenizer_dir / file).exists():
                raise ValueError(f"Required file not found: {file}")
        
        try:
            self.config: Dict[str, Any] = self._load_json(self.tokenizer_dir / "tokenizer_config.json")
        except ValueError as e:
            raise ValueError(f"Failed to load tokenizer config: {e}")
        
        self._tokenizer: Optional[PreTrainedTokenizerFast] = None
        self.model_max_length: int = self.config.get("model_max_length", 2048)
        self._token_cache: Dict[str, List[int]] = {}

    @property
    def tokenizer(self) -> PreTrainedTokenizerFast:
        """
        @brief Lazy load the tokenizer.
        
        @return: The initialized tokenizer.
        @throws ValueError: If the tokenizer fails to load.
        """
        if self._tokenizer is None:
            try:
                self._tokenizer = PreTrainedTokenizerFast(
                    tokenizer_file=str(self.tokenizer_dir / "tokenizer.json"),
                    config=self.config,
                    clean_up_tokenization_spaces=True  # Add this line
                )
            except Exception as e:
                logging.error(f"Failed to load tokenizer. Error: {e}", exc_info=True)
                raise ValueError("Failed to initialize tokenizer") from e
        return self._tokenizer

    def _load_json(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        @brief Load a JSON file.
        
        @param file_path: Path to the JSON file.
        @return: Parsed JSON content as a dictionary.
        @throws ValueError: If the file is not found or cannot be parsed.
        """
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading JSON file {file_path}: {e}")

    @require_tokenizer
    def count_tokens(self, text: Union[str, List[str]], async_mode: bool = False, batch_size: int = 1000) -> Union[int, Coroutine[None, None, int]]:
        """
        Count tokens in the given text or list of texts.
        
        @param text: A string or list of strings to tokenize.
        @param async_mode: If True, returns a coroutine for asynchronous execution.
        @param batch_size: The number of texts to process in a single batch when dealing with large lists.
        @return: The total number of tokens, or a coroutine if async_mode is True.
        @raises ValueError: If the input is invalid.
        """
        if async_mode:
            return self._count_tokens_async(text, batch_size)
        else:
            return self._count_tokens_impl(text, batch_size)

    async def _count_tokens_async(self, text: Union[str, List[str]], batch_size: int) -> int:
        return await asyncio.to_thread(self._count_tokens_impl, text, batch_size)

    def _count_tokens_impl(self, text: Union[str, List[str]], batch_size: int) -> int:
        """
        Internal method to implement token counting logic.
        
        @param text: A string or list of strings to tokenize.
        @param batch_size: The number of texts to process in a single batch.
        @return: The total number of tokens.
        @raises ValueError: If the input is invalid.
        """
        if isinstance(text, str):
            return min(len(self.tokenize(text)), self.model_max_length)
        elif isinstance(text, list):
            if not all(isinstance(t, str) for t in text):
                raise ValueError("All elements in the list must be strings")
            if not text:  # Handle empty list
                return 0
            
            total_tokens = 0
            for i in range(0, len(text), batch_size):
                batch = text[i:i+batch_size]
                encoded = self.tokenizer.batch_encode_plus(
                    batch, 
                    add_special_tokens=False, 
                    truncation=True, 
                    max_length=self.model_max_length,
                    padding=False,
                    return_attention_mask=False,
                    return_token_type_ids=False,
                )
                total_tokens += sum(len(ids) for ids in encoded['input_ids'])
            
            return min(total_tokens, self.model_max_length)
        else:
            raise ValueError("Input must be a string or a list of strings")

    def get_max_tokens(self) -> int:
        """
        @brief Get the maximum number of tokens supported by the model.
        
        @return: The maximum number of tokens.
        """
        return self.model_max_length

    @require_tokenizer
    def tokenize(self, text: str) -> List[int]:
        """
        @brief Tokenize the given text.
        
        @param text: The string to tokenize.
        @return: A list of token IDs.
        """
        if text in self._token_cache:
            return self._token_cache[text]
        
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        
        # Cache the result if it's not too long
        if len(text) <= 1000:  # Adjust this threshold as needed
            self._token_cache[text] = tokens
        
        return tokens

    @require_tokenizer
    async def tokenize_async(self, text: str) -> List[int]:
        """
        @brief Asynchronously tokenize the given text.
        
        @param text: The string to tokenize.
        @return: A list of token IDs.
        """
        return await asyncio.to_thread(self.tokenize, text)