import binascii
from contextlib import contextmanager
import os
import time

from age.age import get_wall_data

from flask import Flask, send_from_directory


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return '''
        <p>Open edX dashboard.</p>
        <p>You might like <a href="/age.html">Pull Request ages</a>.</p>
        '''

@app.route('/boom')
def boom():
    1/0

@app.route('/age/write', methods=['GET', 'POST'])
def write_age():
    start = time.time()
    age_json = get_wall_data()
    with replace_file("age/age.json") as age_json_file:
        age_json_file.write(age_json)
    end = time.time()
    return "Wrote {} bytes in {:.1f}s".format(len(age_json), end - start)

@app.route('/age/<path:filename>')
def send_age_static(filename):
    return send_from_directory('age', filename)

@app.route('/<path:filename>')
def send_static(filename):
    if filename.startswith("age"):
        return send_from_directory('age', filename)


@contextmanager
def replace_file(name):
    tmpname = '%s.tmp-%s' % (name, binascii.hexlify(os.urandom(10)))
    try:
        with open(tmpname, 'w+') as f:
            yield f
        os.rename(tmpname, name)
    finally:
        try:
            os.unlink(tmpname)
        except OSError:
            pass
