import unittest
from pathlib import Path
import sys
import os
import logging
import asyncio

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.counter import LlamaTokenCounter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestLlamaTokenCounter(unittest.TestCase):
    def setUp(self):
        self.tokenizer_dir = Path(__file__).parent / "tokenizer"
        if not self.tokenizer_dir.exists():
            raise ValueError(f"Tokenizer directory not found: {self.tokenizer_dir}")
        self.counter = LlamaTokenCounter(self.tokenizer_dir)
        logger.info(f"Set up LlamaTokenCounter with tokenizer directory: {self.tokenizer_dir}")

    def test_initialization(self):
        self.assertIsInstance(self.counter, LlamaTokenCounter)
        self.assertEqual(self.counter.tokenizer_dir, self.tokenizer_dir)
        logger.info("Initialization test passed")

    def test_count_tokens_string(self):
        text = "Hello, world!"
        token_count = self.counter.count_tokens(text)
        logger.info(f"Token count for '{text}': {token_count}")
        self.assertGreater(token_count, 0, f"Expected more than 0 tokens, got {token_count}")

    def test_count_tokens_list(self):
        texts = ["Hello", "world", "!"]
        token_count = self.counter.count_tokens(texts)
        logger.info(f"Token count for {texts}: {token_count}")
        self.assertGreater(token_count, 0, f"Expected more than 0 tokens, got {token_count}")

    def test_count_tokens_invalid_input(self):
        with self.assertRaises(ValueError):
            self.counter.count_tokens(123)
        with self.assertRaises(ValueError):
            self.counter.count_tokens([1, 2, 3])
        with self.assertRaises(ValueError):
            self.counter.count_tokens(["valid", 123, "invalid"])
        logger.info("Invalid input test passed")

    def test_get_max_tokens(self):
        max_tokens = self.counter.get_max_tokens()
        logger.info(f"Max tokens: {max_tokens}")
        self.assertIsInstance(max_tokens, int)
        self.assertGreaterEqual(max_tokens, 2048)

    def test_long_text(self):
        long_text = "This is a very long text that goes on and on. " * 100
        token_count = self.counter.count_tokens(long_text)
        logger.info(f"Token count for long text: {token_count}")
        self.assertGreater(token_count, 500, f"Expected more than 500 tokens for long text, got {token_count}")

    def test_special_characters(self):
        special_text = "Hello! How are you? I'm fine, thanks. 😊 #python @user $100 &amp; 42% [test] {json}"
        token_count = self.counter.count_tokens(special_text)
        logger.info(f"Token count for special characters: {token_count}")
        self.assertGreater(token_count, 10, f"Expected more than 10 tokens for special characters, got {token_count}")

    def test_multilingual(self):
        multilingual_text = "Hello こんにちは Bonjour Здравствуйте مرحبا"
        token_count = self.counter.count_tokens(multilingual_text)
        logger.info(f"Token count for multilingual text: {token_count}")
        self.assertGreater(token_count, 5, f"Expected more than 5 tokens for multilingual text, got {token_count}")

    def test_code_snippet(self):
        code_snippet = """
        def hello_world():
            print("Hello, World!")
            for i in range(10):
                print(f"Count: {i}")
        """
        token_count = self.counter.count_tokens(code_snippet)
        logger.info(f"Token count for code snippet: {token_count}")
        self.assertGreater(token_count, 20, f"Expected more than 20 tokens for code snippet, got {token_count}")

    def test_max_length(self):
        very_long_text = "a" * 1000000  # 1 million characters
        token_count = self.counter.count_tokens(very_long_text)
        max_tokens = self.counter.get_max_tokens()
        logger.info(f"Token count for very long text: {token_count}, Max tokens: {max_tokens}")
        self.assertLessEqual(token_count, max_tokens, f"Token count {token_count} exceeds max tokens {max_tokens}")

    def test_consistency(self):
        text = "This is a test of consistency."
        count1 = self.counter.count_tokens(text)
        count2 = self.counter.count_tokens(text)
        logger.info(f"Consistency test: First count: {count1}, Second count: {count2}")
        self.assertEqual(count1, count2, "Tokenization should be consistent for the same input")

    def test_whitespace_handling(self):
        text1 = "Hello World"
        text2 = "Hello    World"
        count1 = self.counter.count_tokens(text1)
        count2 = self.counter.count_tokens(text2)
        logger.info(f"Whitespace handling: '{text1}' count: {count1}, '{text2}' count: {count2}")
        self.assertGreaterEqual(count2, count1, "Multiple whitespaces should result in equal or more tokens")

    def test_whitespace_tokens(self):
        text1 = "Hello World"
        text2 = "Hello    World"
        tokens1 = self.counter.tokenize(text1)
        tokens2 = self.counter.tokenize(text2)
        logger.info(f"Tokens for '{text1}': {tokens1}")
        logger.info(f"Tokens for '{text2}': {tokens2}")
        self.assertNotEqual(tokens1, tokens2, "Different whitespace should result in different tokenization")

    def test_large_list_of_strings(self):
        large_list = ["Hello", "World"] * 1000  # 2000 items
        token_count = self.counter.count_tokens(large_list)
        logger.info(f"Token count for large list of strings: {token_count}")
        self.assertGreater(token_count, 1000, f"Expected more than 1000 tokens for large list, got {token_count}")

    def test_empty_input(self):
        self.assertEqual(self.counter.count_tokens(""), 0)
        self.assertEqual(self.counter.count_tokens([]), 0)

    def test_whitespace_only(self):
        self.assertGreater(self.counter.count_tokens("    "), 0)
        self.assertGreater(self.counter.count_tokens("\n\t\r"), 0)

    def test_unicode_characters(self):
        text = "Hello, 世界! こんにちは 🌍"
        token_count = self.counter.count_tokens(text)
        logger.info(f"Token count for Unicode text: {token_count}")
        self.assertGreater(token_count, 5)

    def test_long_word(self):
        long_word = "pneumonoultramicroscopicsilicovolcanoconiosis"
        token_count = self.counter.count_tokens(long_word)
        logger.info(f"Token count for long word: {token_count}")
        self.assertGreater(token_count, 1)

    def test_repeated_characters(self):
        repeated_text = "a" * 1000 + "b" * 1000 + "c" * 1000
        token_count = self.counter.count_tokens(repeated_text)
        logger.info(f"Token count for repeated characters: {token_count}")
        self.assertLess(token_count, 3000)

    def test_mixed_content(self):
        mixed_text = "Regular text 123 !@#$% \n\t Unicode: 你好 Emoji: 😊"
        token_count = self.counter.count_tokens(mixed_text)
        logger.info(f"Token count for mixed content: {token_count}")
        self.assertGreater(token_count, 10)

    def test_large_input(self):
        large_text = "This is a test. " * 10000
        token_count = self.counter.count_tokens(large_text)
        logger.info(f"Token count for large input: {token_count}")
        self.assertGreater(token_count, 10000)

    def test_special_tokens(self):
        special_tokens = [" ", "  ", "   ", "<pad>"]
        expected_counts = [1, 1, 1, 3]  # Updated expected count for <pad>
        for token, expected_count in zip(special_tokens, expected_counts):
            count = self.counter.count_tokens(token)
            logger.info(f"Token count for {token}: {count}")
            self.assertEqual(count, expected_count, f"Expected {expected_count} for '{token}', got {count}")

    def test_code_snippets(self):
        code_snippet = """
        def fibonacci(n):
            if n <= 1:
                return n
            else:
                return fibonacci(n-1) + fibonacci(n-2)
        
        print(fibonacci(10))
        """
        token_count = self.counter.count_tokens(code_snippet)
        logger.info(f"Token count for code snippet: {token_count}")
        self.assertGreater(token_count, 20)

    def test_multiple_languages(self):
        multilingual_text = "Hello in multiple languages: Bonjour, Hola, Ciao, Здравствуйте, こんにちは, 你好"
        token_count = self.counter.count_tokens(multilingual_text)
        logger.info(f"Token count for multilingual text: {token_count}")
        self.assertGreater(token_count, 10)

    def test_urls_and_emails(self):
        text_with_urls = "Check out https://www.example.com or contact info@example.com"
        token_count = self.counter.count_tokens(text_with_urls)
        logger.info(f"Token count for text with URLs and emails: {token_count}")
        self.assertGreater(token_count, 5)

    def test_numbers_and_punctuation(self):
        text_with_numbers = "Pi is approximately 3.14159265359. The year is 2023!"
        token_count = self.counter.count_tokens(text_with_numbers)
        logger.info(f"Token count for text with numbers and punctuation: {token_count}")
        self.assertGreater(token_count, 10)

    def test_consistency(self):
        text = "This is a test of tokenization consistency."
        count1 = self.counter.count_tokens(text)
        count2 = self.counter.count_tokens(text)
        self.assertEqual(count1, count2)

    def test_batch_processing(self):
        texts = ["Hello", "World", "This is a test", "Multiple strings in a list"]
        token_count = self.counter.count_tokens(texts)
        logger.info(f"Token count for batch processing: {token_count}")
        self.assertGreater(token_count, 10)

    def test_max_token_limit(self):
        very_long_text = "a" * 1000000  # 1 million characters
        token_count = self.counter.count_tokens(very_long_text)
        max_tokens = self.counter.get_max_tokens()
        logger.info(f"Token count for very long text: {token_count}, Max tokens: {max_tokens}")
        self.assertLessEqual(token_count, max_tokens)

    async def test_async_counting(self):
        text = "This is an async test."
        sync_count = self.counter.count_tokens(text)
        async_count = await self.counter.count_tokens(text, async_mode=True)
        self.assertEqual(sync_count, async_count)

    async def test_async_batch_processing(self):
        texts = ["Async", "Batch", "Processing", "Test"]
        sync_count = self.counter.count_tokens(texts)
        async_count = await self.counter.count_tokens(texts, async_mode=True)
        self.assertEqual(sync_count, async_count)

    def test_tokenize_method(self):
        text = "This is a tokenization test."
        tokens = self.counter.tokenize(text)
        logger.info(f"Tokens: {tokens}")
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)

    async def test_async_tokenize_method(self):
        text = "This is an async tokenization test."
        sync_tokens = self.counter.tokenize(text)
        async_tokens = await self.counter.tokenize_async(text)
        self.assertEqual(sync_tokens, async_tokens)

    def test_error_handling(self):
        with self.assertRaises(ValueError):
            self.counter.count_tokens(123)
        with self.assertRaises(ValueError):
            self.counter.count_tokens([1, 2, 3])
        with self.assertRaises(ValueError):
            self.counter.count_tokens(None)

    def test_very_long_sentence(self):
        long_sentence = "This is a very long sentence with many words " * 1000
        token_count = self.counter.count_tokens(long_sentence)
        logger.info(f"Token count for very long sentence: {token_count}")
        self.assertGreater(token_count, 5000)

    def test_technical_jargon(self):
        technical_text = "Quantum entanglement in superconducting qubits exhibits non-local correlations."
        token_count = self.counter.count_tokens(technical_text)
        logger.info(f"Token count for technical jargon: {token_count}")
        self.assertGreater(token_count, 10)

    def test_mixed_case_sensitivity(self):
        mixed_case = "ThIs Is A tEsT oF mIxEd CaSe SeNsItIvItY."
        lower_case = mixed_case.lower()
        mixed_count = self.counter.count_tokens(mixed_case)
        lower_count = self.counter.count_tokens(lower_case)
        logger.info(f"Token count for mixed case: {mixed_count}, lower case: {lower_count}")
        self.assertNotEqual(mixed_count, lower_count)

    def test_non_ascii_characters(self):
        non_ascii = "áéíóúñ çãõ ßœ ئ ض"
        token_count = self.counter.count_tokens(non_ascii)
        logger.info(f"Token count for non-ASCII characters: {token_count}")
        self.assertGreater(token_count, 5)

    def test_mathematical_expressions(self):
        math_expr = "∫(x^2 + 2x + 1)dx = (x^3)/3 + x^2 + x + C"
        token_count = self.counter.count_tokens(math_expr)
        logger.info(f"Token count for mathematical expression: {token_count}")
        self.assertGreater(token_count, 10)

    def test_large_numbers(self):
        large_numbers = "1234567890" * 100
        token_count = self.counter.count_tokens(large_numbers)
        logger.info(f"Token count for large numbers: {token_count}")
        self.assertLess(token_count, 1000)  # Expecting some compression

    def test_repeated_words(self):
        repeated_words = "buffalo " * 20
        token_count = self.counter.count_tokens(repeated_words)
        logger.info(f"Token count for repeated words: {token_count}")
        self.assertLess(token_count, 40)  # Expecting some compression

    def test_xml_content(self):
        xml_content = """
        <root>
            <element attr="value">
                <child>Text content</child>
            </element>
        </root>
        """
        token_count = self.counter.count_tokens(xml_content)
        logger.info(f"Token count for XML content: {token_count}")
        self.assertGreater(token_count, 10)

    def test_json_content(self):
        json_content = """
        {
            "key1": "value1",
            "key2": 42,
            "key3": [1, 2, 3],
            "key4": {"nested": "object"}
        }
        """
        token_count = self.counter.count_tokens(json_content)
        logger.info(f"Token count for JSON content: {token_count}")
        self.assertGreater(token_count, 15)

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
        token_count = self.counter.count_tokens(markdown_content)
        logger.info(f"Token count for Markdown content: {token_count}")
        self.assertGreater(token_count, 30)

    def test_edge_case_characters(self):
        edge_cases = "".join(chr(i) for i in range(32, 127)) + "".join(chr(i) for i in range(160, 256))
        token_count = self.counter.count_tokens(edge_cases)
        logger.info(f"Token count for edge case characters: {token_count}")
        self.assertGreater(token_count, 50)

    def test_consistency_across_calls(self):
        text = "This is a test of tokenization consistency across multiple calls."
        counts = [self.counter.count_tokens(text) for _ in range(100)]
        logger.info(f"Token counts across 100 calls: {counts[:5]}...")
        self.assertEqual(len(set(counts)), 1, "Token counts should be consistent across calls")

    def test_large_batch_processing(self):
        large_batch = ["Text " + str(i) for i in range(10000)]
        token_count = self.counter.count_tokens(large_batch)
        logger.info(f"Token count for large batch: {token_count}")
        self.assertGreater(token_count, 10000)

    async def test_async_large_batch_processing(self):
        large_batch = ["Hello world"] * 10000
        token_count = await self.counter.count_tokens(large_batch, async_mode=True)
        self.assertEqual(token_count, 20000)  # Assuming "Hello world" is 2 tokens

    def test_tokenization_reversibility(self):
        original_text = "This is a test of tokenization reversibility."
        tokens = self.counter.tokenize(original_text)
        reconstructed_text = self.counter.tokenizer.decode(tokens)
        logger.info(f"Original: {original_text}")
        logger.info(f"Reconstructed: {reconstructed_text}")
        self.assertEqual(original_text, reconstructed_text.strip())  # Added strip() to remove potential leading/trailing spaces

    def test_max_token_limit_edge_case(self):
        max_tokens = self.counter.get_max_tokens()
        very_long_text = "a" * (max_tokens * 10)  # Try to exceed max tokens by a large margin
        token_count = self.counter.count_tokens(very_long_text)
        logger.info(f"Token count for text exceeding max limit: {token_count}, Max tokens: {max_tokens}")
        self.assertLessEqual(token_count, max_tokens)
        self.assertGreater(token_count, max_tokens * 0.9)  # Ensure we're close to the max limit

    def test_unified_count_tokens(self):
        text = "This is a test."
        sync_count = self.counter.count_tokens(text)
        async_count = asyncio.run(self.counter.count_tokens(text, async_mode=True))
        self.assertEqual(sync_count, async_count)

    def test_batch_processing(self):
        texts = ["Text " + str(i) for i in range(1000)]
        count_without_batch = self.counter.count_tokens(texts)
        count_with_batch = self.counter.count_tokens(texts, batch_size=100)
        self.assertEqual(count_without_batch, count_with_batch)

    async def test_async_batch_processing(self):
        texts = ["Text " + str(i) for i in range(1000)]
        count_sync = self.counter.count_tokens(texts, batch_size=100)
        count_async = await self.counter.count_tokens(texts, async_mode=True, batch_size=100)
        self.assertEqual(count_sync, count_async)

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            self.counter.count_tokens(123)
        with self.assertRaises(ValueError):
            self.counter.count_tokens([1, 2, 3])

    def test_async_operations(self):
        asyncio.run(self.run_async_tests())

    async def run_async_tests(self):
        await self.test_async_counting()
        await self.test_async_batch_processing()
        await self.test_async_tokenize_method()
        await self.test_async_large_batch_processing()

class AsyncioTestRunner(unittest.TextTestRunner):
    def run(self, test):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._run_async(test))

    async def _run_async(self, test):
        result = test(self)
        if asyncio.iscoroutine(result):
            return await result
        return result

if __name__ == '__main__':
    unittest.main(testRunner=AsyncioTestRunner())