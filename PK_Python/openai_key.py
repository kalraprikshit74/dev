import openai
APIKEY =

open.api_key = APIKEY

output = openai.chatcompletion.create(model = "gpt-3.5-turbo",message=[{"role": "user", "content": "write me a script for hosting a conference on technology"}])

print(output)
