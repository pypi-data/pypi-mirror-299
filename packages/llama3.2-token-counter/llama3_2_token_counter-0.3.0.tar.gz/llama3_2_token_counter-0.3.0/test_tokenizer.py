from pathlib import Path
from sentencepiece import SentencePieceProcessor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

root_dir = Path(__file__).parent
tokenizer_file = root_dir / "src" / "llama_token_counter" / "tokenizer" / "tokenizer.model"

logger.info(f"Tokenizer file path: {tokenizer_file}")
tokenizer = SentencePieceProcessor(model_file=str(tokenizer_file))
logger.info("Tokenizer loaded successfully")

text = "Hello, world!"
tokens = tokenizer.encode(text)
logger.info(f"Tokens for '{text}': {tokens}")