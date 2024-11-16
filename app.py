from flask import Flask ,session,render_template_string
from user import register_user
from user import login_user
from domain import add_domain ,add_bulk
from check_liveness import livness_check



app = Flask(__name__)  # __name__ helps Flask locate resources and configurations
app.secret_key = 'NOT_TO_BAD_SECRET_KEY'

@app.route('/', methods=['GET'])
def home():
    return "Welcome to my Flask app!"

#  http://127.0.0.1:8080/login?username=<username>&password=<password>
@app.route('/login', methods=['GET'])
def login():
    username = request.args.get('username',default=None)
    password = request.args.get('password',default=None)
    print( f"{username} {password}")    #
    status = login_user(username,password) 
    print (username)
    if "Login Successful"== status['message']:
        session['user']=username
    return login_user(username,password)  
    

@app.route('/logoff', methods=['GET'])
def logoff():
    user=session['user']
    session['user']=""
    if user=="":
        return "No user is logged in"
    return f"User {user} is logged off"




#  http://127.0.0.1:8080/register?username=<username>&password=<password>
@app.route('/register', methods=['GET'])
def register():
    username = request.args.get('username',default=None)
    password = request.args.get('password',default=None)
    print( f"{username} {password}")    #
    return register_user(username,password)  




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

@app.route('/add_domain/<domain>')
def add_new_domain(domain):
    return add_domain(session['user'],domain)  
    
@app.route('/add_bulk/<filename>')
def add_from_file(filename):
    return add_bulk(session['user'],filename)  
    
    
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
    return livness_check (username)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
