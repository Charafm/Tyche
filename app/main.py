from ollama import Client

client = Client()
response = client.chat(model='phi3:mini', messages=[
    {'role': 'system', 'content': 'You are an expert reasoning assistant.'},
    {'role': 'user', 'content': 'Hello, can you help me with a problem?'},
])
print(response['message']['content'])
