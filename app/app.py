from flask import Flask
from redis import Redis
import logging, os
app = Flask(__name__)
redis = Redis(host='redis', port=6379)

logging.basicConfig(level=logging.DEBUG)
LOG = logging.getLogger(__name__)

@app.route('/')
def hello():
  redis.incr('hits')
  return 'Seen %s times.\n' % redis.get('hits')

if __name__ == "__main__":
  import netifaces, requests
  my_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
  my_port = lb_port = 5000
  lb_ip = os.environ['LB_PORT_{}_TCP_ADDR'.format(lb_port)]
  r = requests.post('http://{}:{}/join'.format(lb_ip, lb_port), data={'ip': my_ip, 'port': my_port})
  LOG.debug(r.text)
  app.run(host="0.0.0.0", debug=True)
