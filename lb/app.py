from flask import Flask, request
import itertools, logging, eventlet
import requests as http
from requests.exceptions import ConnectionError
from threading import Lock

eventlet.monkey_patch()
app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

group = {}
group_iterator = itertools.cycle(group)

m = Lock()

def update_group(ip, port, delete=False):
    global group, group_iterator
    m.acquire()
    if delete:
        del group[ip]
    else:
        group[ip] = port
    group_iterator = itertools.cycle(group)
    m.release()

def get_host():
    global group, group_iterator
    m.acquire()
    try:
        return group_iterator.next()
    except StopIteration:
        return None
    finally:
        m.release()

@app.route('/', methods=['GET', ])
def proxy():
    global group

    r = None
    while r is None:
        host = get_host()
        if host is None:
            return 'No host available', 400

        with eventlet.Timeout(3, False):
            r = http.get(('http://{}:{}/').format(host, group[host]))
        
        if r is None:
            # this means the host left the group
            update_group(host, None, True)

    LOG.debug('Request proxied to {}:{}'.format(host, group[host]))
    return r.text

@app.route('/join', methods=['POST', ])
def join():
    ip = request.form['ip']
    port = request.form['port']
    update_group(ip, port)
    return 'Joined as {}:{}'.format(ip, port) 

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
