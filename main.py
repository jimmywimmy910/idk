from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

SCRATCH_USERNAME = 'Fox8snow'
SCRATCH_PASSWORD = 'claw91011'
SCRATCH_LOGIN_URL = 'https://scratch.mit.edu/login/'
SCRATCH_PROJECT_URL = 'https://scratch.mit.edu/site-api/projects/all/'

@app.route('/create_project', methods=['POST'])
def create_project():
    data = request.json
    project_name = data.get('project_name')
    project_description = data.get('project_description')

    session = requests.Session()

    # Log in to Scratch
    login_payload = {
        'username': SCRATCH_USERNAME,
        'password': SCRATCH_PASSWORD
    }
    login_response = session.post(SCRATCH_LOGIN_URL, json=login_payload)

    if login_response.status_code != 200:
        return jsonify({'success': False, 'message': 'Login failed'}), 401

    # Create the project
    project_payload = {
        'title': project_name,
        'description': project_description
    }
    project_response = session.post(SCRATCH_PROJECT_URL, json=project_payload)

    if project_response.status_code == 200:
        return jsonify({'success': True}), 201
    else:
        return jsonify({'success': False, 'message': 'Failed to create project'}), 500

if __name__ == '__main__':
    # Use gunicorn as the production server
    # gunicorn -w 4 -b 0.0.0.0:5000 main:app
    # Adjust workers (-w) and bind address (-b) as needed
    import os
    host = '0.0.0.0'
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)
