# LangChain Huggy

A LangChain integration for HuggingChat models.

## Installation

```bash
pip install langchain-huggy
```

## Usage

```python
from langchain_huggy import HuggingChat
from langchain_core.messages import HumanMessage

chat_model = HuggingChat()
messages = [HumanMessage(content="Tell me a joke about programming.")]
response = chat_model.generate(messages)
print(response.generations[0].message.content)

# For streaming
for chunk in chat_model.stream(messages):
    print(chunk.message.content, end="", flush=True)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.