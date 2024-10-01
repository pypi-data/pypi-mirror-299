import json
from typing import List, Dict, Any
from pathlib import Path
import logging
from functools import lru_cache

class CustomTokenizer:
    def __init__(self, tokenizer_dir: Path):
        self.tokenizer_dir = Path(tokenizer_dir)
        self.config = self._load_json(self.tokenizer_dir / "tokenizer_config.json")
        self.tokenizer_data = self._load_json(self.tokenizer_dir / "tokenizer.json")
        
        self.vocab = {word.lower(): i for i, word in enumerate(self.tokenizer_data['model']['vocab'])}
        self.merges = dict(enumerate(self.tokenizer_data['model'].get('merges', [])))
        self.added_tokens = self._load_added_tokens()
        
        self.unk_token = self.config.get('unk_token', '<unk>')
        self.bos_token = self.config.get('bos_token', '<s>')
        self.eos_token = self.config.get('eos_token', '</s>')
        self.whitespace_token = ' '
        
        self.unk_token_id = self.vocab.get(self.unk_token, len(self.vocab))
        self.bos_token_id = self.vocab.get(self.bos_token, len(self.vocab) + 1)
        self.eos_token_id = self.vocab.get(self.eos_token, len(self.vocab) + 2)
        self.whitespace_token_id = self.vocab.get(self.whitespace_token, len(self.vocab))
        
        logging.info("CustomTokenizer initialization complete")
        self._tokenize_word_cached = lru_cache(maxsize=10000)(self._tokenize_word)
        self._id_to_token = {i: token for token, i in self.vocab.items()}
        self._special_tokens = {self.bos_token, self.eos_token, self.unk_token, self.whitespace_token}

    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        logging.info(f"Loading JSON file: {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logging.info(f"JSON file loaded successfully: {file_path}")
        return data

    def _load_added_tokens(self) -> Dict[str, int]:
        added_tokens = {}
        for token_id, token_info in self.config.get('added_tokens_decoder', {}).items():
            added_tokens[token_info['content']] = int(token_id)
        return added_tokens

    @lru_cache(maxsize=10000)
    def encode(self, text: str, add_special_tokens: bool = True) -> List[int]:
        if not text:
            return [self.bos_token_id, self.eos_token_id] if add_special_tokens else []
        tokens = []
        for word in text.split():
            tokens.extend(self._tokenize_word(word.lower()))
            tokens.append(self.whitespace_token_id)
        if tokens and tokens[-1] == self.whitespace_token_id:
            tokens.pop()  # Remove trailing whitespace token
        if add_special_tokens:
            tokens = [self.bos_token_id] + tokens + [self.eos_token_id]
        return tokens[:self.model_max_length]  # Truncate to max_length

    def _tokenize_word(self, word: str) -> List[int]:
        if word in self.added_tokens:
            return [self.added_tokens[word]]

        if word in self.vocab:
            return [self.vocab[word]]

        tokens = []
        while word:
            found = False
            for i in range(len(word), 0, -1):
                subword = word[:i]
                if subword in self.vocab:
                    tokens.append(self.vocab[subword])
                    word = word[i:]
                    found = True
                    break
            if not found:
                tokens.append(self.unk_token_id)
                word = word[1:]  # Skip one character for unknown tokens

        return tokens

    def tokenize(self, text: str) -> List[int]:
        tokens = []
        for char in text:
            if char.isspace():
                if not tokens or tokens[-1] != self.whitespace_token_id:
                    tokens.append(self.whitespace_token_id)
            else:
                tokens.extend(self._tokenize_word(char.lower()))
        return tokens

    def batch_encode_plus(self, batch: List[str], add_special_tokens: bool = True, 
                          truncation: bool = False, max_length: int = None, 
                          padding: bool = False) -> Dict[str, List[List[int]]]:
        batch_tokens = self.encode_batch(batch, add_special_tokens)
        
        if truncation and max_length:
            batch_tokens = [tokens[:max_length] for tokens in batch_tokens]
        
        if padding:
            max_len = max(len(tokens) for tokens in batch_tokens)
            batch_tokens = [tokens + [self.unk_token_id] * (max_len - len(tokens)) for tokens in batch_tokens]
        
        return {'input_ids': batch_tokens}

    def encode_batch(self, batch: List[str], add_special_tokens: bool = True) -> List[List[int]]:
        return [self.encode(text, add_special_tokens) for text in batch]

    def decode(self, tokens: List[int]) -> str:
        decoded = []
        for token in tokens:
            if token in self._id_to_token:
                word = self._id_to_token[token]
                if word not in self._special_tokens:
                    decoded.append(word)
            else:
                decoded.append(self.unk_token)  # Handle unknown tokens
        return ''.join(decoded).strip()  # Join without spaces and strip

    def vocab_size(self) -> int:
        return len(self.vocab)

    @property
    def model_max_length(self) -> int:
        return self.config.get('model_max_length', 2048)  # Default to 2048 if not specified