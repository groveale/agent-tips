from flask import Flask, render_template, request, jsonify
import threading
import time
import os
from web_agents import run_agents

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Store ongoing tasks
tasks = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_query():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    task_id = str(int(time.time()))
    tasks[task_id] = {
        'status': 'processing',
        'query': query,
        'results': None
    }
    
    thread = threading.Thread(target=process_query, args=(task_id, query))
    thread.daemon = True
    thread.start()
    
    return jsonify({'taskId': task_id})

@app.route('/status/<task_id>', methods=['GET'])
def get_status(task_id: str):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = tasks[task_id]
    response = {
        'status': task['status'],
        'query': task['query']
    }
    
    if task['status'] == 'completed':
        response['results'] = task['results']
    elif task['status'] == 'failed':
        response['error'] = task.get('error', 'Unknown error')
    
    return jsonify(response)

def process_query(task_id: str, query: str) -> None:
    try:
        results = run_agents(query)
        tasks[task_id].update({
            'status': 'completed',
            'results': results
        })
    except Exception as e:
        tasks[task_id].update({
            'status': 'failed',
            'error': str(e)
        })

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    app.run(host='127.0.0.1', port=5000)