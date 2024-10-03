import unittest
from langchain_huggy import HuggingChat
from langchain_core.messages import HumanMessage

class TestHuggingChat(unittest.TestCase):
    def setUp(self):
        self.chat_model = HuggingChat()

    def test_generate(self):
        messages = [HumanMessage(content="Hello, how are you?")]
        response = self.chat_model.generate(messages)
        self.assertIsNotNone(response)
        self.assertTrue(len(response.generations) > 0)
        self.assertIsNotNone(response.generations[0].message.content)

    def test_stream(self):
        messages = [HumanMessage(content="Count to 5.")]
        stream = self.chat_model.stream(messages)
        content = "".join(chunk.message.content for chunk in stream)
        self.assertIsNotNone(content)
        self.assertTrue(len(content) > 0)

if __name__ == "__main__":
    unittest.main()