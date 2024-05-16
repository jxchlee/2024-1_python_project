from flask import Flask, request, redirect
import random

topics = [
    {"id": 1, "title": "html", "body": "html is ..."},
    {"id": 2, "title": "javascript", "body": "javascript is..."},
    {"id": 3, "title": "css", "body": "css is..."},
]

def template(contents, content={'title': 'welcome', 'body': 'hello'}, id=None):
    update = ''
    if id != None:
        update += f'''<li><a href="/update/{id}/">update</a></li>
<li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"><form></li>'''
    return f'''
        <!doctype html>
        <html>
            <body>
                <h1><a href="/">WEB</a></h1>
                <ol>
                    {contents}
                </ol>
                <a href="/create/">create</a>
                <ul>
                    <h2>{content['title']}</h2>
                    {content['body']}
                    {update}
                </ul>
            </body>
        </html>
        '''
def getContents():
    list = ''
    for s in topics:
        list += f'<li><a href="/read/{s['id']}/">{s['title']}</a></li>'
    return list

app = Flask(__name__)
@app.route('/')
def index():
    return template(getContents())


@app.route('/create/', methods=['GET', 'POST'])
def index1():
        if request.method == 'GET':
            inform = {
                'title': 'create',
                'body': '''
                <form method="post" action="/create/">
                    <p><input type="test" placeholder="title" name="title"></p>
                    <p><textarea placeholder="body" name="body"></textarea></p>
                    <p><input type="submit" value="create"></p>
                </form>
                '''
            }

            return template(getContents(), inform)
        elif request.method == 'POST':
            newTopic = {
                'id': len(topics)+1,
                'title': request.form['title'],
                'body': request.form['body'],
            }
            topics.append(newTopic)
            url = f'/read/{len(topics)}/'
            return redirect(url)


@app.route('/read/<int:id>/')
def read(id):
    inform = {}
    for x in topics:
        if id == x['id']:
            inform['title'] = x['title']
            inform['body'] = x['body']
            break
    return template(getContents(), inform, id)


@app.route('/update/<int:id>/', methods=['GET', 'POST'])
def update(id):
        if request.method == 'GET':
            title = topics[id-1]['title']
            body = topics[id-1]['body']
            inform = {
                'title': 'create',
                'body': f'''
                <form method="post" action="/update/{id}">
                    <p><input type="test" placeholder="title" name="title" value="{title}"></p>
                    <p><textarea placeholder="body" name="body">{body}</textarea></p>
                    <p><input type="submit" value="update"></p>
                </form>
                '''
            }
            return template(getContents(), inform)
        elif request.method == 'POST':
            title = request.form['title']
            body = request.form['body']
            for topic in topics:
                if id == topic['id']:
                    topic['title'] = title
                    topic['body'] = body
                    break
            url = f'/read/{id}/'
            return redirect(url)


@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if id == topic['id']:
            topics.remove(topic)
            break
    url = '/'
    return redirect(url)

app.run(debug=True)