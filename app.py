from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
from os import getenv

app = Flask(__name__)

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url=getenv('KEYVAULTURL'), credential=credential)

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/secret')
def secret():
   secret = secret_client.get_secret("secret")
   return secret.value


@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run()