from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
app = Flask(__name__)


from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient

credential = DefaultAzureCredential()

key_client = KeyClient(vault_url="https://ccsdevtestus.vault.azure.net/", credential=credential)



@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/list')
def listsecret():
   try:
      keys = key_client.list_properties_of_keys()
      keys=[]
      for key in keys:
         keys.append(key.name)
         print(key.name)
      return jsonify(keys)
   except Exception as e:
      return e


@app.route('/secret')
def secret():
   try:
      key = key_client.get_key("secret")
      return key.value
   except Exception as e:
      return e


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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