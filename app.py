import openai
from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

# Replace 'your-openai-api-key' with your actual OpenAI API key
openai.api_key = 'sk-proj-ZsU8BzB]F]sreeAXwBByT3BLbkF]VwsRuH92Dxh02xLduouG'

# Optionally, configure other client options
openai.base_url = "https://api.openai.com/v1"
openai.default_headers = {"x-foo": "true"}

# Function to get a completion from the OpenAI API
def get_completion(prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a helpful personal trainer assistant specialized in athlete injury prevention."
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
    )
    return completion.choices[0].message['content']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data['prompt']
    response = get_completion(prompt)
    return jsonify({'response': response})

if __name__ == "__main__":
    app.run(debug=True)
