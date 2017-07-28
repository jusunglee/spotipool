from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    user = {'name': 'jusung'}
    title = "jusung's world"
    data = {
        'title': title,
        'user': user
    }
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)