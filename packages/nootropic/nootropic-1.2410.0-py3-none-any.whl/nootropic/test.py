#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio

from anthropic import Anthropic
from groq import AsyncGroq, Groq
from ollama import AsyncClient, Client
from openai import OpenAI

from nootropic import Nootropic

original_payload = {
    'model': '',
    'messages': [{
        "role": "user",
        "content": 'Hola, cómo estás?',
    }],
    'max_tokens': 512,
}


# OpenAI
payload = dict(original_payload)
client = Nootropic(OpenAI(
    base_url='https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-70B-Instruct/v1/',
    api_key='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',
))
completion = client.chat.completions.create(**payload)
message = completion.choices[0].message.content
print(message)

# Anthropic
payload = dict(original_payload)
payload['model'] = 'claude-3-5-sonnet-20240620'
client = Nootropic(Anthropic(
    api_key="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",
))
message = client.messages.create(**payload).content[0].text
print(message)

# Groq
payload = dict(original_payload)
payload['model'] = 'llama-3.1-70b-versatile'
client = Nootropic(Groq(
    api_key='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',
))
message = client.chat.completions.create(**payload).choices[0].message.content
print(message)

# Groq Async
payload = dict(original_payload)
payload['model'] = 'llama-3.1-70b-versatile'
client = Nootropic(AsyncGroq(
    api_key='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',
))


async def chat():
    message = (await client.chat.completions.create(**payload)).choices[0].message.content
    print(message)

asyncio.run(chat())

# Ollama
payload = dict(original_payload)
payload['model'] = 'llama3.1:8b'
del payload['max_tokens']
client = Nootropic(Client(
    host='10.0.0.105:11435',
))
message = client.chat(**payload)['message']['content']
print(message)
stream = client.chat(stream=True, **payload)
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

# Ollama Async
payload = dict(original_payload)
client = Nootropic(AsyncClient(host='10.0.0.105:11435'))
payload['model'] = 'llama3.1:8b'
del payload['max_tokens']


async def chat():
    message = (await client.chat(**payload))['message']['content']
    print(message)

asyncio.run(chat())
