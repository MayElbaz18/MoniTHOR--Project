from flask import Flask, session, render_template_string, render_template
from pythonBE import user , check_liveness ,domain



app = Flask(__name__)  # __name__ helps Flask locate resources and configurations
app.secret_key = 'NOT_TO_BAD_SECRET_KEY'

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

@app.route('/0', methods=['GET'])
def main():
    return render_template('dashboard.html', user=session['user'])

  

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
    username = request.args.get('username',default=None)
    password1 = request.args.get('password1',default=None)
    password2 = request.args.get('password2',default=None)
    print(f"Received: username={username}, password1={password1}, password2={password2}")
    
    # Validate input parameters
    if not username or not password1 or not password2:
        session['message'] = {'message': 'All fields are required'}
        return render_template('register.html')

    if password1 != password2:
        session['message'] = {'message': 'Passwords do not match'}
        return render_template('register.html')

    # Process registration
    status = user.register_user(username, password1)
    session['message'] = status

    if status['message'] == "Registered successfully":
        return "Registered successfully"  
    else:
        return status['message']  




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
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>")     
    session['message'] =domain.add_domain(session['user'],domainName)     
    return render_template_string("<h1>{{session['message']['message']}}.</h1>")

# usage : http://127.0.0.1:8080/add_bulk/.%5Cuserdata%5CDomains_for_upload.txt 
# using  %5C instaed of  "\"  
@app.route('/add_bulk/<filename>')
def add_from_file(filename):    
    if session['user']=="" :
        return render_template_string("<h1>No User is logged in </h1>")           
    session['message']=domain.add_bulk(session['user'],filename)  
    return render_template_string("<h1>{{session['message']}}.</h1>")
    
    
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)