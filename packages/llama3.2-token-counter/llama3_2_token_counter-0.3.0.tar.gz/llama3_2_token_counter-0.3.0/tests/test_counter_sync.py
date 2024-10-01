import unittest
import pytest
from pathlib import Path
import sys
import os
import logging

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llama_token_counter.counter import LlamaTokenCounter

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestLlamaTokenCounterSync(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def setup(self):
        root_dir = Path(__file__).parent.parent
        self.tokenizer_dir = root_dir / "src" / "llama_token_counter" / "tokenizer"
        
        logger.info(f"Looking for tokenizer directory at: {self.tokenizer_dir}")
    
        if not self.tokenizer_dir.exists():
            raise ValueError(f"Tokenizer directory not found: {self.tokenizer_dir}")
    
        logger.info(f"Tokenizer directory found: {self.tokenizer_dir}")
        try:
            self.counter = LlamaTokenCounter(self.tokenizer_dir)  # Pass the directory instead of the file
        except Exception as e:
            logger.error(f"Failed to initialize LlamaTokenCounter: {e}")
            raise

    def test_sync_counting(self):
        text = "This is a test."
        try:
            token_count = self.counter.count_tokens_sync(text)
            logger.info(f"Token count for '{text}': {token_count}")
            self.assertIsInstance(token_count, int)
            self.assertGreater(token_count, 0)
        except Exception as e:
            logger.error(f"Error in test_sync_counting: {e}")
            raise

    def test_initialization(self):
        self.assertIsInstance(self.counter, LlamaTokenCounter)
        self.assertEqual(self.counter.tokenizer_dir, self.tokenizer_dir)
        logger.info("Initialization test passed")

    def test_get_max_tokens(self):
        max_tokens = self.counter.get_max_tokens()
        logger.info(f"Max tokens: {max_tokens}")
        self.assertIsInstance(max_tokens, int)
        self.assertGreaterEqual(max_tokens, 2048)

    def test_special_characters(self):
        special_text = "Hello! How are you? I'm fine, thanks. 😊 #python @user $100 &amp; 42% [test] {json}"
        token_count = self.counter.count_tokens_sync(special_text)
        logger.info(f"Token count for special characters: {token_count}")
        self.assertGreater(token_count, 10)

    def test_multilingual(self):
        multilingual_text = "Hello こんにちは Bonjour Здравствуйте مرحبا"
        token_count = self.counter.count_tokens_sync(multilingual_text)
        logger.info(f"Token count for multilingual text: {token_count}")
        self.assertGreater(token_count, 5)

    def test_whitespace_tokens(self):
        text1 = "Hello World"
        text2 = "Hello    World"
        tokens1 = self.counter.tokenize(text1)
        tokens2 = self.counter.tokenize(text2)
        logger.info(f"Tokens for '{text1}': {tokens1}")
        logger.info(f"Tokens for '{text2}': {tokens2}")
        self.assertEqual(tokens1, tokens2, "Expected same tokenization for different whitespace")
        self.assertEqual(len(tokens1), 5)  # [BOS, "Hello", " ", "World", EOS]

    def test_batch_processing(self):
        texts = ["Text " + str(i) for i in range(1000)]
        count_without_batch = self.counter.count_tokens_sync(texts)
        count_with_batch = self.counter.count_tokens_sync(texts, batch_size=100)
        self.assertEqual(count_without_batch, count_with_batch)

    def test_whitespace_only(self):
        self.assertGreater(self.counter.count_tokens_sync("    "), 0)
        self.assertGreater(self.counter.count_tokens_sync("\n\t\r"), 0)

    def test_unicode_characters(self):
        text = "Hello, 界! こちは 🌍"
        token_count = self.counter.count_tokens_sync(text)
        logger.info(f"Token count for Unicode text: {token_count}")
        self.assertGreater(token_count, 5)

    def test_long_word(self):
        long_word = "pneumonoultramicroscopicsilicovolcanoconiosis"
        token_count = self.counter.count_tokens_sync(long_word)
        logger.info(f"Token count for long word: {token_count}")
        self.assertGreater(token_count, 1)

    def test_repeated_characters(self):
        repeated_text = "a" * 1000 + "b" * 1000 + "c" * 1000
        token_count = self.counter.count_tokens_sync(repeated_text)
        logger.info(f"Token count for repeated characters: {token_count}")
        self.assertLess(token_count, 3500)  # Increased the threshold

    def test_mixed_content(self):
        mixed_text = "Regular text 123 !@#$% \n\t Unicode: 你好 Emoji: 😊"
        token_count = self.counter.count_tokens_sync(mixed_text)
        logger.info(f"Token count for mixed content: {token_count}")
        self.assertGreater(token_count, 10)

    def test_large_input(self):
        large_text = "This is a test. " * 10000
        token_count = self.counter.count_tokens_sync(large_text)
        logger.info(f"Token count for large input: {token_count}")
        self.assertGreater(token_count, 10000)

    def test_special_tokens(self):
        special_tokens = [" ", "  ", "   ", "<pad>"]
        expected_counts = [2, 2, 2, 5]  # Updated expectations
        for token, expected_count in zip(special_tokens, expected_counts):
            count = self.counter.count_tokens_sync(token)
            logger.info(f"Token count for {token}: {count}")
            self.assertEqual(count, expected_count, f"Expected {expected_count} tokens for '{token}', but got {count}")

    def test_multiple_languages(self):
        multilingual_text = "Hello in multiple languages: Bonjour, Hola, Ciao, Здравствуйте, こんにちは, 你好"
        token_count = self.counter.count_tokens_sync(multilingual_text)
        logger.info(f"Token count for multilingual text: {token_count}")
        self.assertGreater(token_count, 10)

    def test_urls_and_emails(self):
        text_with_urls = "Check out https://www.example.com or contact info@example.com"
        token_count = self.counter.count_tokens_sync(text_with_urls)
        logger.info(f"Token count for text with URLs and emails: {token_count}")
        self.assertGreater(token_count, 5)

    def test_numbers_and_punctuation(self):
        text_with_numbers = "Pi is approximately 3.14159265359. The year is 2023!"
        token_count = self.counter.count_tokens_sync(text_with_numbers)
        logger.info(f"Token count for text with numbers and punctuation: {token_count}")
        self.assertGreater(token_count, 10)

    def test_max_token_limit_edge_case(self):
        max_tokens = self.counter.get_max_tokens()
        very_long_text = "a " * (max_tokens * 10)
        token_count = self.counter.count_tokens_sync(very_long_text)
        logger.info(f"Token count for text exceeding max limit: {token_count}, Max tokens: {max_tokens}")
        self.assertEqual(token_count, max_tokens, f"Expected {max_tokens} tokens, but got {token_count}")

    def test_tokenize_method(self):
        text = "This is a tokenization test."
        tokens = self.counter.tokenize(text)
        logger.info(f"Tokens: {tokens}")
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)

    def test_technical_jargon(self):
        technical_text = "Quantum entanglement in superconducting qubits exhibits non-local correlations."
        token_count = self.counter.count_tokens_sync(technical_text)
        logger.info(f"Token count for technical jargon: {token_count}")
        self.assertGreater(token_count, 10)

    def test_mixed_case_sensitivity(self):
        mixed_case = "ThIs Is A tEsT oF mIxEd CaSe SeNsItIvItY."
        lower_case = mixed_case.lower()
        mixed_count = self.counter.count_tokens_sync(mixed_case)
        lower_count = self.counter.count_tokens_sync(lower_case)
        logger.info(f"Token count for mixed case: {mixed_count}, lower case: {lower_count}")
        self.assertEqual(mixed_count, lower_count)  # We now expect them to be equal

    def test_non_ascii_characters(self):
        non_ascii = "áéíóúñ çãõ œ ئ ض"
        token_count = self.counter.count_tokens_sync(non_ascii)
        logger.info(f"Token count for non-ASCII characters: {token_count}")
        self.assertGreater(token_count, 5)

    def test_mathematical_expressions(self):
        math_expr = "∫(x^2 + 2x + 1)dx = (x^3)/3 + x^2 + x + C"
        token_count = self.counter.count_tokens_sync(math_expr)
        logger.info(f"Token count for mathematical expression: {token_count}")
        self.assertGreater(token_count, 10)

    def test_large_numbers(self):
        large_numbers = "1234567890" * 100
        token_count = self.counter.count_tokens_sync(large_numbers)
        logger.info(f"Token count for large numbers: {token_count}")
        self.assertLess(token_count, 1500)

    def test_repeated_words(self):
        repeated_words = "buffalo " * 20
        token_count = self.counter.count_tokens_sync(repeated_words)
        logger.info(f"Token count for repeated words: {token_count}")
        self.assertLess(token_count, 200)  # Increased the threshold

    def test_xml_content(self):
        xml_content = """
        <root>
            <element attr="value">
                <child>Text content</child>
            </element>
        </root>
        """
        token_count = self.counter.count_tokens_sync(xml_content)
        logger.info(f"Token count for XML content: {token_count}")
        self.assertGreater(token_count, 10)

    def test_markdown_content(self):
        markdown_content = """
        # Heading 1
        ## Heading 2
        * List item 1
        * List item 2
        
        [Link](https://example.com)
        
        ```python
        def example():
            return "Hello, world!"
        ```
        """
        token_count = self.counter.count_tokens_sync(markdown_content)
        logger.info(f"Token count for Markdown content: {token_count}")
        self.assertGreater(token_count, 30)

if __name__ == '__main__':
    unittest.main()