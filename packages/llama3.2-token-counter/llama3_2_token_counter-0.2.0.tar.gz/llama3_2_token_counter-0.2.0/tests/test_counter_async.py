import unittest
from pathlib import Path
import sys
import os
import logging
import asyncio
import pytest
from typing import Union, List

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.llama_token_counter.counter import LlamaTokenCounter

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def timeout(seconds):
    return pytest.mark.timeout(seconds)

class TestLlamaTokenCounterAsync(unittest.TestCase):
    def setUp(self):
        root_dir = Path(__file__).parent.parent
        self.tokenizer_dir = root_dir / "src" / "llama_token_counter" / "tokenizer"
        try:
            self.counter = LlamaTokenCounter(self.tokenizer_dir)
        except Exception as e:
            logger.error(f"Failed to initialize LlamaTokenCounter: {str(e)}")
            raise

    async def async_test_with_timeout(self, coro):
        try:
            return await asyncio.wait_for(coro, timeout=30)  # 30 seconds timeout
        except asyncio.TimeoutError:
            self.fail("Test timed out after 30 seconds")

    @pytest.mark.asyncio
    async def test_async_counting(self):
        text = "This is an async test."
        async_count = await self.counter.count_tokens(text)
        sync_count = self.counter.count_tokens_sync(text)
        assert async_count == sync_count

    @pytest.mark.asyncio
    async def test_batch_processing(self):
        texts = ["Text " + str(i) for i in range(100)]
        count_without_batch = await self.counter.count_tokens(texts)
        count_with_batch = await self.counter.count_tokens(texts, batch_size=10)
        self.assertEqual(count_without_batch, count_with_batch)

    @pytest.mark.asyncio
    async def test_code_snippet(self):
        code_snippet = """
        def hello_world():
            print("Hello, World!")
            for i in range(10):
                print(f"Count: {i}")
        """
        token_count = await self.counter.count_tokens(code_snippet)
        logging.info(f"Token count for code snippet: {token_count}")
        self.assertGreater(token_count, 20)

    @pytest.mark.asyncio
    async def test_consistency(self):
        text = "This is a test of tokenization consistency."
        count1 = await self.counter.count_tokens(text)
        count2 = await self.counter.count_tokens(text)
        self.assertEqual(count1, count2)

    @pytest.mark.asyncio
    async def test_count_tokens_invalid_input(self):
        with self.assertRaises(ValueError):
            await self.counter.count_tokens(123)

    @pytest.mark.asyncio
    async def test_count_tokens_list(self):
        texts = ["Hello", "world", "!"]
        token_count = await self.counter.count_tokens(texts)
        logging.info(f"Token count for {texts}: {token_count}")
        self.assertGreater(token_count, 0)

    @pytest.mark.asyncio
    async def test_count_tokens_string(self):
        text = "Hello, world!"
        token_count = await self.counter.count_tokens(text)
        logging.info(f"Token count for '{text}': {token_count}")
        self.assertGreater(token_count, 0)

    @pytest.mark.asyncio
    async def test_edge_case_characters(self):
        edge_cases = "".join(chr(i) for i in range(32, 127)) + "".join(chr(i) for i in range(160, 256))
        token_count = await self.counter.count_tokens(edge_cases)
        logging.info(f"Token count for edge case characters: {token_count}")
        self.assertGreater(token_count, 50)

    @pytest.mark.asyncio
    async def test_long_text(self):
        long_text = "This is a very long text that goes on and on. " * 100
        token_count = await self.counter.count_tokens(long_text)
        logger.info(f"Token count for long text: {token_count}")
        self.assertGreater(token_count, 500)

    @timeout(30)
    async def test_max_length(self):
        very_long_text = "a" * 10000
        token_count = await self.counter.count_tokens(very_long_text)
        max_tokens = self.counter.get_max_tokens()
        logger.info(f"Token count for very long text: {token_count}, Max tokens: {max_tokens}")
        self.assertLessEqual(token_count, max_tokens)

    @pytest.mark.asyncio
    async def test_whitespace_handling(self):
        text1 = "Hello World"
        text2 = "Hello    World"
        count1 = await self.counter.count_tokens(text1)
        count2 = await self.counter.count_tokens(text2)
        logger.info(f"Whitespace handling: '{text1}' count: {count1}, '{text2}' count: {count2}")
        self.assertGreaterEqual(count2, count1)

    @pytest.mark.asyncio
    async def test_empty_input(self):
        self.assertEqual(await self.counter.count_tokens(""), 0)
        self.assertEqual(await self.counter.count_tokens([]), 0)

    @pytest.mark.asyncio
    async def test_json_content(self):
        json_content = """
        {
            "key1": "value1",
            "key2": 42,
            "key3": [1, 2, 3],
            "key4": {"nested": "object"}
        }
        """
        token_count = await self.counter.count_tokens(json_content)
        logger.info(f"Token count for JSON content: {token_count}")
        self.assertGreater(token_count, 15)

    @pytest.mark.asyncio
    async def test_consistency_across_calls(self):
        text = "This is a test of tokenization consistency across multiple calls."
        counts = [await self.counter.count_tokens(text) for _ in range(100)]
        logger.info(f"Token counts across 100 calls: {counts[:5]}...")
        self.assertEqual(len(set(counts)), 1)

    @pytest.mark.asyncio
    async def test_large_batch_processing(self):
        large_batch = ["Text " + str(i) for i in range(10000)]
        token_count = await self.counter.count_tokens(large_batch)
        logger.info(f"Token count for large batch: {token_count}")
        self.assertGreater(token_count, 10000)

    @pytest.mark.asyncio
    async def test_tokenization_reversibility(self):
        original_text = "This is a test of tokenization reversibility."
        tokens = await self.counter.tokenize_async(original_text)
        reconstructed_text = self.counter.tokenizer.decode(tokens)
        logger.info(f"Original: {original_text}")
        logger.info(f"Reconstructed: {reconstructed_text}")
        self.assertEqual(original_text.lower(), reconstructed_text.lower())

    @pytest.mark.asyncio
    async def test_unified_count_tokens(self):
        text = "This is a test."
        count = await self.counter.count_tokens(text)
        self.assertIsInstance(count, int)
        self.assertGreater(count, 0)

    @pytest.mark.asyncio
    async def test_async_batch_processing(self):
        texts = ["Text " + str(i) for i in range(1000)]
        count_sync = self.counter.count_tokens(texts, batch_size=100)
        count_async = await self.counter.count_tokens_async(texts, batch_size=100)
        self.assertEqual(count_sync, count_async)

if __name__ == '__main__':
    pytest.main([__file__])
