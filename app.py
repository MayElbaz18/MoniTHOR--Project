from flask import Flask, session, render_template_string, render_template, redirect, url_for, request
from pythonBE import user, check_liveness, domain
from pythonBE.logs import logger
import json
import os
from authlib.integrations.flask_client import OAuth
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
import config

app = Flask(__name__)  # __name__ helps Flask locate resources and configurations
app.config.from_object(config.Config)
app.secret_key = 'NOT_TO_BAD_SECRET_KEY'

# Initialize OAuth
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    refresh_token_url=None,
    client_kwargs={'scope': 'openid profile email'}
)

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    # Delete the user's profile and the credentials stored by oauth2
    session.pop('user', None)
    return redirect('/')

@app.route('/authorize')
def authorize():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    domain = user['hd']
    
    if app.config['RESTRICT_DOMAIN'] and domain != app.config['REQUIRED_DOMAIN']:
        # User authenticated with disallowed domain
        print("\n------------------------------------------------------")
        print("User attempted to authenticate with disallowed domain.")
        print("------------------------------------------------------\n")
        return redirect('/logout')

    session['user'] = user
    return redirect('/')

@app.route('/restricted')
def restricted():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('restricted.html')

@app.route('/dashboard', methods=['GET'])
def main():
    user_file = f'./userdata/{session["user"]["email"]}_domains.json'
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            data = json.load(f)
    else:
        data = []      

    # Extract the required parts for the forms
    all_domains = [item['domain'] for item in data]  # List of domain names
    latest_results = data[:6]  # Last 6 results

    return render_template('dashboard.html', user=session['user'], data=data, all_domains=all_domains, latest_results=latest_results)

@app.route('/logoff', methods=['GET'])
def logoff():
    user = session.get('user', '')
    if not user:
        return render_template_string("<h1>No user is logged in.</h1>")
    session['message'] = f"User {user['email']} is logged off now."
    session.pop('user', None)
    print(session['message'])  # Debug print
    return render_template('login.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.args.get('username')
    password1 = request.args.get('password1')
    password2 = request.args.get('password2')
    print(f"Received: username={username}, password1={password1}, password2={password2}")  # Debug print

    # Process registration
    status = user.register_user(username, password1, password2)

    # Validate input parameters
    if password1 != password2:
        session['message'] = {'message': 'Passwords do not match'}
        return "Passwords do not match"
    if status['message'] == 'Username already taken':
        return "Username already taken"
    if status['message'] == 'Registered successfully':
        return "Registered successfully"

    return render_template('register.html')

@app.route('/get_user')
def get_user():
    return render_template_string("""
        {% if session['user'] %}
            <h1>Welcome {{ session['user']['email'] }}!</h1>
        {% else %}
            <h1>No User is logged in</h1>
        {% endif %}
    """)

@app.route('/text')
def text_response():
    return "This is a plain text response."

@app.route('/json')
def json_response():
    return {"message": "This is a JSON response"}, 200  # JSON response with status code

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()  # Parse JSON payload
    return {"received": data}, 200

@app.route('/add_domain/<domainName>', methods=['GET', 'POST'])
def add_new_domain(domainName):
    logger.debug(f'Route being called {domainName}')
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    logger.debug(f'Domain name is {domainName}')
    return domain.add_domain(session['user'], domainName)

@app.route('/remove_domain/<domainName>', methods=['GET', 'POST'])
def remove_domain(domainName):
    logger.debug(f'Route being called {domainName}')
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    logger.debug(f'Domain name is {domainName}')
    return domain.remove_domain(session['user'], domainName)

@app.route('/single_domain/<domainName>', methods=['GET', 'POST'])
def single_domain(domainName):
    logger.debug(f'Route being called {domainName}')
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    logger.debug(f'Domain name is {domainName}')
    return domain.add_domain(session['user'], domainName, False)

@app.route('/bulk_upload/<filename>')
def add_from_file(filename):    
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    print(filename)
    return domain.add_bulk(session['user'], filename)

def save_to_file(text):
    with open('message.txt', 'w') as file:
        file.write(text)

@app.route('/search')
def search():
    query = request.args.get('query')  # Retrieves ?query=value
    query2 = request.args.get('query2')
    save_to_file(f'{query}, {query2}')
    return f"Search results for: {query}, {query2}"

@app.route('/check/<username>')
def check_livness(username):    
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    return check_liveness.livness_check(username, True)

@app.route('/single_check/<username>')
def single_check_livness(username):    
    if session.get('user', '') == "":
        return render_template_string("<h1>No User is logged in</h1>")
    return check_liveness.livness_check(username, False)

# Scheduler job function
def job_function():
    print(f"Job executed at {datetime.now()}")

# Create and start the scheduler
scheduler = BackgroundScheduler()
time_zone = pytz.timezone('Asia/Tokyo')

# Add a job that runs every day at 10:30 AM in the specified time zone
scheduler.add_job(job_function, CronTrigger(hour=10, minute=30, timezone=time_zone))

# Add a job that runs every Monday at 12:00 PM in the specified time zone
scheduler.add_job(job_function, CronTrigger(day_of_week='mon', hour=12, minute=0, timezone=time_zone))

scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
