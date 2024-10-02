# 🚀 | ClashAI Python Package
**ClashAI Python Package for easy API integration!**

## Installation
```python
pip install clashai
```

## Chat Completions
```python
import clashai

client = clashai.Client(api_key="[YOUR API KEY]")
completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Hello, World!",
        }
    ]
)

print(completion['choices'][0]['message']['content'])
```