import json
import pprint

from flask import Flask
from utils import statistics
from logging import getLogger

logger = getLogger(__name__)
app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>These Are Not the Droids You Are Looking For</title>
    </head>
    <body>
        <img src="http://i0.kym-cdn.com/entries/icons/facebook/000/018/682/obi-wan.jpg"></img>
    </body>
    </html>
    """

@app.route('/api/<group_id>')
def api(group_id):
    try:
        stats = statistics.build(group_id)
    except Exception as e:
        logger.info("Exception: {}".format(str(e)))
        return '{"error": "Probably there is no such group"}'
    
    return json.dumps(stats, indent=4, ensure_ascii=False).encode("UTF-8"), 200, {'Content-Type': 'application/json; charset=utf-8'}
        
if __name__ == "__main__":
    app.run('0.0.0.0')
