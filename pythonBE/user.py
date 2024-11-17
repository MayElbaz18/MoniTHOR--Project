import os
import json

  
def register_user (userName,password) :

    successMessage = { 'message' : "Registered successfully"}
    failureMessage = { 'message' : "Username already taken"}

# checking if users file is exist , if not it will be created 
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as f:
            f.write("{}")

    with open('users.json', 'r') as f:
        current_info = json.load(f)
        currentListOfUsers=list(current_info)
    
    

    for user in currentListOfUsers :
        if user['username'] == userName:
            return failureMessage
 
    
    
    
    newUser ={'username':userName,'password': password }
    currentListOfUsers.append(newUser)

        
    with open('users.json', 'w') as f:
        json.dump(currentListOfUsers, f, indent=4)
        return successMessage


# Login function
def login_user (userName,password) :
        
        successMessage = { 'message' : "Login Successful"}
        failureMessage = { 'message' : "error : invalid user name or password"} 
        
        # Create users file if not exist 
        if not os.path.exists('users.json'):
            return failureMessage
        
        # loadin current data fro users file and convert to list 
        with open('users.json', 'r') as f:
            current_info = json.load(f)
            currentListOfUsers=list(current_info)
    
        # checking is user in file , if yes , validating password 
        for user in currentListOfUsers :        
            if user['username'] == userName:
                if user['password']== password:
                    return successMessage
                else:
                    return failureMessage
 
        return failureMessage
    
    



