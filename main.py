import json
import random
import pprint
import logging

from app import *
from utils import statistics
from utils.executor import Executor

executor = Executor(max_workers=3)

def json_responce(obj, code=200):
    return (
        json.dumps(obj, indent=4, ensure_ascii=False).encode("UTF-8"), 
        code, {
            'Content-Type': 'application/json; charset=utf-8'
        }
    )

@app.route('/')
def index(): 
    image_urls = app.config['THESE_ARE_NOT_THE_DROIDS']
    return render_template(
        'index.html', 
        image_url=random.choice(image_urls)
    )

@app.route('/api/<group_id>')
def api(group_id):
    future = executor.future(group_id)
    if not future:
        executor.submit(group_id, statistics.build, group_id)
        return json_responce({
            "message": ("Got it. "
                       "Processing data. "
                       "You can get back in couple of minutes for result")
        })
    
    if not future.done():
        return json_responce({
            "message": "Sorry, your result is not ready yet."
        })
    
    try:
        stats = future.result()
        return json_responce(stats)
    except Exception as exception:
        return json_responce({
            "message": "Sorry, some error occured.",
            "error": "{}('{}')".format(type(exception).__name__, str(exception))
        })

@app.route('/api/status')
def status():
    return json_responce(executor.status)

@app.route('/api/clear/<group_id>')
def clear(group_id):
    try:
        executor.clear(group_id)
        return json_responce({
            "message": "Success"
        })
    except KeyError:
        return json_responce({
            "message": "No such task. Nothing to clear"
        })

if __name__ == "__main__":
    app.run('0.0.0.0')
