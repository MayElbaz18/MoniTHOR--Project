from flask import Flask, session, render_template_string, render_template
from pythonBE import user , check_liveness ,domain
from pythonBE.logs import logger
import json
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
import pytz
import uuid
from datetime import datetime 


app = Flask(__name__)  # __name__ helps Flask locate resources and configurations
app.secret_key = 'NOT_TO_BAD_SECRET_KEY'

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.start()

scheduled_jobs = [] # Store scheduled jobs

@app.route('/schedule_bulk_monitoring', methods=['POST'])
def schedule_bulk_monitoring():
    # Get form data
    schedule_time = request.form['schedule_time']
    timezone = request.form['timezone']
    user = session['user']

    # Convert time to UTC
    local_tz = pytz.timezone(timezone)
    local_time = local_tz.localize(datetime.fromisoformat(schedule_time))
    utc_time = local_time.astimezone(pytz.utc)

    # Generate a unique job ID
    job_id = str(uuid.uuid4())

    # Schedule job
    scheduler.add_job(
        func=add_from_file,
        trigger=DateTrigger(run_date=utc_time),
        args=[user],
        id=job_id
    )

    # Save job info
    scheduled_jobs.append({
        'id': job_id,
        'user': user,
        'time': schedule_time,
        'timezone': timezone
    })

    return {'message': 'Monitoring scheduled successfully!'}

@app.route('/cancel_job/<job_id>', methods=['POST'])
def cancel_job(job_id):
    scheduler.remove_job(job_id)
    global scheduled_jobs
    scheduled_jobs = [job for job in scheduled_jobs if job['id'] != job_id]
    return {'message': 'Job canceled successfully!'}

@app.route('/', methods=['GET'])
def home():
        return render_template('login.html')

#  http://127.0.0.1:8080/login?username=<username>&password=<password>
@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username',default=None)
    password = request.args.get('password',default=None)
    print( f"{username} {password}")    #
    status = user.login_user(username,password) 
    print (username)
    if "Login Successful"== status['message']:
        session['user']=username
        return "Login Successful"
    session['message']=user.login_user(username,password)  
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
def main():
    user_file = f'./userdata/{session['user']}_domains.json'
    if os.path.exists(user_file):
     with open(user_file, 'r') as f:
          data = json.load(f)
    else:
        data = []      

    # Extract the required parts for the forms
    all_domains = [item['domain'] for item in data]  # List of domain names
    latest_results = data[:6]  # Last 6 results
    # Pass scheduled jobs for the current user
    user_jobs = [job for job in scheduled_jobs if job['user'] == session['user']]
    utc_timezones = [tz for tz in pytz.all_timezones if tz.startswith('UTC')]

    return render_template('dashboard.html', user=session['user'], data=data, all_domains=all_domains, latest_results=latest_results, scheduled_jobs=user_jobs,
                            utc_timezones=utc_timezones)

@app.route('/logoff', methods=['GET'])
def logoff():
    user=session['user']
    if user=="":
        return  render_template_string("<h1>No user is logged in.</h1>")
    session['message']=f"User {session['user']} is logged off now."
    session['user']=""
    print (session['message'])
    return  render_template('login.html')




#  http://127.0.0.1:8080/register?username=<username>&password1=<password1>&password2=<password2>
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.args.get('username')
    password1 = request.args.get('password1')
    password2 = request.args.get('password2')
    print(f"Received: username={username}, password1={password1}, password2={password2}")
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
    



#  http://127.0.0.1:8080/get_user
@app.route('/get_user')
def get_user():
    return render_template_string("""
            {% if session['user'] %}
                <h1>Welcome {{ session['user'] }}!</h1>
            {% else %}
                <h1>No User is logged in </h1>
            {% endif %}
        """)
  
@app.route('/text')
def text_response():
    return "This is a plain text response."

@app.route('/json')
def json_response():
    return {"message": "This is a JSON response"}, 200  # JSON response with status code

from flask import request

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()  # Parse JSON payload
    return {"received": data}, 200

@app.route('/add_domain/<domainName>',methods=['GET', 'POST'])
def add_new_domain(domainName):
    logger.debug(f'Route being code {domainName}')
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>") 
    # Get the domain name from the form data
    logger.debug(f'Domain name is {domainName}')
        
    return domain.add_domain(session['user'],domainName)   
    

@app.route('/remove_domain/<domainName>',methods=['GET', 'POST'])
def remove_domain(domainName):
    logger.debug(f'Route being code {domainName}')
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>") 
    # Get the domain name from the form data
    logger.debug(f'Domain name is {domainName}')    
    return domain.remove_domain(session['user'],domainName)   


@app.route('/single_domain/<domainName>',methods=['GET', 'POST'])
def single_domain(domainName):
    logger.debug(f'Route being code {domainName}')
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>") 
    # Get the domain name from the form data
    logger.debug(f'Domain name is {domainName}')
        
    return domain.add_domain(session['user'],domainName)   

# usage : http://127.0.0.1:8080/bulk_upload/.%5Cuserdata%5CDomains_for_upload.txt 
# using  %5C instaed of  "\"  
#  in UI put    ./userdata/Domains_for_upload.txt
@app.route('/bulk_upload/<filename>')
def add_from_file(filename):    
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>")           
    print (filename)
    return domain.add_bulk(session['user'],filename)
    
    
def save_to_file(text):
    with open('message.txt', 'w') as file:
        file.write(text)
    
@app.route('/search')
def search():
    query = request.args.get('query')  # Retrieves ?query=value
    query2 = request.args.get('query2')

    save_to_file(f'{query},{query2}')

    return f"Search results for: {query}, {query2}"

@app.route('/check/<username>')
def check_livness(username):    
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>") 
    return check_liveness.livness_check (username)




@app.route('/single_check/<username>')
def single_check_livness(username):    
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>") 
    return check_liveness.livness_check (username)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)