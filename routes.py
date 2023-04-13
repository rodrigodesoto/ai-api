import os

import openai
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['API_KEY'], os.environ['S3_SECRET'])
from flask import Flask, request, jsonify
openai.api_key = os.environ['OPENAI_API_KEY']

application = Flask(__name__)

valid_api_keys = os.environ['API_KEY']

def check_api_key():
    if 'api_key' not in request.headers:
        return jsonify({'message': 'API key missing'}), 401
    elif request.headers['api_key'] not in valid_api_keys:
        return jsonify({'message': 'Invalid API key'}), 401

@application.before_request
def before_request():
    check_api_key()

@application.route('/askai', methods=['POST'])
def askai():
    # Recebe a pergunta em formato JSON
    data = request.get_json()
    question = data['question']

    # Processa a pergunta e obtém a resposta
    answer = prompt(question)

    # Retorna a resposta em formato JSON
    return jsonify({'answer': answer})

def prompt(question):

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        temperature=0.5,
        top_p=1.0,
        max_tokens=500)
    response = response.choices[0]['text'].strip()
    return response

if __name__ == '__main__':
    application.run()
