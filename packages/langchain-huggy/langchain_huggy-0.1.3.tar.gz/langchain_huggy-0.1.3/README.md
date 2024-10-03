# langchain_huggy

langchain_huggy is a Python package that provides an easy-to-use interface for interacting with HuggingChat models through the LangChain framework.

## Available Models

langchain_huggy comes with several pre-configured models:

1. 'meta-llama/Meta-Llama-3.1-70B-Instruct'
2. 'CohereForAI/c4ai-command-r-plus-08-2024'
3. 'Qwen/Qwen2.5-72B-Instruct'
4. 'meta-llama/Llama-3.2-11B-Vision-Instruct'
5. 'NousResearch/Hermes-3-Llama-3.1-8B'
6. 'mistralai/Mistral-Nemo-Instruct-2407'
7. 'microsoft/Phi-3.5-mini-instruct'

You can choose any of these models when initializing the HuggingChat instance.

## Installation

Install the package using pip:

```bash
pip install langchain_huggy
```

## Quick Start

Here's a simple example to get you started:

```python
from langchain_huggy import HuggingChat

# Initialize the HuggingChat model
llm = HuggingChat(
    hf_email = "your_huggingface_email@example.com",
    hf_password = "your_huggingface_password",
    model = "Qwen/Qwen2.5-72B-Instruct"  # Optional: specify a model
)

# Stream the response to a question
llm.pstream("Who is Modi?")
```

This will print the streamed response to your question about Modi using the specified model.

## Features

- Easy integration with LangChain
- Supports streaming responses
- Uses HuggingChat models
- Customizable with different model options

## Configuration

You can configure the HuggingChat instance with the following parameters:

- `hf_email`: Your HuggingFace account email
- `hf_password`: Your HuggingFace account password
- `model`: (Optional) Specify a particular model to use from the available models list

## Viewing Available Models

You can view the list of available models at any time using:

```python
print(llm.get_available_models)
```

## Note

Make sure to keep your HuggingFace credentials secure and never share them in public repositories.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you encounter any problems or have any questions, please open an issue on the GitHub repository.

Happy chatting with langchain_huggy!