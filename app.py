from flask import Flask, session, render_template_string, render_template,redirect,request
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

# Route for Job schedule 
@app.route('/schedule_bulk_monitoring', methods=['POST'])
def schedule_bulk_monitoring():
    # Get form data    
    schedule_time = request.form['schedule_time']
    timezone = request.form['timezone']
    interval = request.form.get('interval')
    user = session['user']    

    # Convert time to UTC
    local_tz = pytz.timezone(timezone)
    local_time = local_tz.localize(datetime.fromisoformat(schedule_time))
    utc_time = local_time.astimezone(pytz.utc)

    # Generate a unique job ID
    job_id = str(uuid.uuid4())

    if interval:
        # Schedule a recurring job
        scheduler.add_job(Checkjob,trigger='interval',hours=int(interval),args=[user],id=job_id,start_date=utc_time)
    else:
        # Schedule a one-time job
        scheduler.add_job(Checkjob,trigger=DateTrigger(run_date=utc_time),args=[user],id=job_id)
    
    # Save job info
    scheduled_jobs.append({'id': job_id,'user': user,'time': schedule_time,'timezone': timezone,'interval': interval})    

    return {'message': 'Monitoring scheduled successfully!'}

# Route for job cancel 
@app.route('/cancel_job/<job_id>', methods=['POST'])
def cancel_job(job_id):
    scheduler.remove_job(job_id)
    global scheduled_jobs
    scheduled_jobs = [job for job in scheduled_jobs if job['id'] != job_id]
    return {'message': 'Job canceled successfully!'}

# Route for login page 
@app.route('/', methods=['GET'])
def home():
        return render_template('login.html')

# Route for login page 
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
    return render_template('login.html')

# Route for Dashboard  
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
                            utc_timezones=utc_timezones,last_run=session['lastRun'][0] ,number_of_domains=session['lastRun'][1]  )

# Route for Logoff
@app.route('/logoff', methods=['GET'])
def logoff():
    user=session['user']
    if user=="":
        return  ("No user is logged in")    
    session['user']=""    
    return  render_template('login.html')



# Route for Register 
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
        return "Passwords do not match"
    if status['message'] == 'Username already taken':
        return "Username already taken"
    if status['message'] == 'Registered successfully':
        return "Registered successfully"         

    return render_template('register.html')
    





# @app.route('/submit', methods=['POST'])
# def submit_data():
#     data = request.get_json()  # Parse JSON payload
#     return {"received": data}, 200

# Route to add a single domain 
@app.route('/add_domain/<domainName>',methods=['GET', 'POST'])
def add_new_domain(domainName):
    logger.debug(f'Route being code {domainName}')
    if session['user']=="" :
        return "No User is logged in" 
    # Get the domain name from the form data
    logger.debug(f'Domain name is {domainName}')
        
    return domain.add_domain(session['user'],domainName)   
    
# Route to remove a single domain 
@app.route('/remove_domain/<domainName>',methods=['GET', 'POST'])
def remove_domain(domainName):
    logger.debug(f'Route being code {domainName}')
    if session['user']=="" :
        return "No User is logged in"
    # Get the domain name from the form data
    logger.debug(f'Domain name is {domainName}')    
    return domain.remove_domain(session['user'],domainName)   

 

# usage : http://127.0.0.1:8080/bulk_upload/.%5Cuserdata%5CDomains_for_upload.txt 
# using  %5C instaed of  "\"  
# in UI put    ./userdata/Domains_for_upload.txt

@app.route('/bulk_upload/<filename>')
def add_from_file(filename):    
    if session['user']=="" :
        return "No User is logged in"           
    print (filename)
    return domain.add_bulk(session['user'],filename)
    
    
# Route to run Livness check 
@app.route('/check/<username>')
def check_livness(username):    
    if session['user']=="" :
        return "No User is logged in" 
    session["lastRun"]=check_liveness.livness_check (username)    
    return session["lastRun"]
    


def Checkjob(username):    
    check_liveness.livness_check (username)
    return redirect('/dashboard')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    