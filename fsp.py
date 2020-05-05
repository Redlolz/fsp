from sanic import Sanic
from sanic.response import json, html, redirect, file_stream
from sanic_session import Session, InMemorySessionInterface
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import urllib.parse
import json
import os.path
import os

with open('config.json', 'r') as configfile:
    configdata = configfile.read()
config = json.loads(configdata)

app = Sanic(__name__)
app.static('/static', './static')
session = Session(app, interface=InMemorySessionInterface())

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html','xml'])
)

def request_parse(body):
    return urllib.parse.parse_qs(body.decode('utf-8'))

def render_template(template, **kwargs):
    template = env.get_template(template)
    return html(template.render(kwargs, url_for=app.url_for))

def get_file_locations(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

@app.route('/')
async def main(request):
    if not request['session'].get('logged_in'):
        return render_template('login.html')
    else:
        return redirect(app.url_for('files'))

@app.route('/loginattempt', methods=['POST'])
async def loginattempt(request):
    request_form = request_parse(request.body)

    if request_form['password'][0] == config['password']:
        request['session']['logged_in'] = True
        return redirect(app.url_for('files'))

    return redirect(app.url_for('main'))

@app.route('/files')
async def files(request):
    if not request['session'].get('logged_in'):
        return redirect(app.url_for('main'))

    return render_template('files.html', files=get_file_locations(config['path']))

@app.route('/download/<f>')
async def download(request, f):
    if not request['session'].get('logged_in'):
        return redirect(app.url_for('main'))

    if f not in get_file_locations(config['path']):
        return html("<p>Can't find file</p>")

    return await file_stream(config['path'] + '/' + f)

if __name__ == "__main__":
    app.run(host=config['webhost'], port=config['webport'])