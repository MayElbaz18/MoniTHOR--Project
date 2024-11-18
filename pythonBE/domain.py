import os
import json
import re


def add_domain (userName,domain) :

    successMessage = { 'message' : "Domain successfully added"}
    failureMessageExist = { 'message' : "Domain already exist in file"}
    failureMessageNotValid = { 'message' : "Invalid Domain Name"}
    
    domain=domain.replace('"','')
    
    if not is_valid_domain(domain):
        return failureMessageNotValid

    userDoaminFile=f'./userdata/{userName}_domains.json'
    
    if not os.path.exists(userDoaminFile):
        with open(userDoaminFile, 'w') as f:
            f.write("{}")



    with open(f'./userdata/{userName}_domains.json', 'r') as f:
        current_info = json.load(f)
        currentListOfDomains=list(current_info)
        
       
    for d in currentListOfDomains :        
        if d['domain'] == domain:
            return failureMessageExist

    newDomain ={'domain':domain,'status':'unknown','ssl_expiration':'unknown','ssl_issuer':'unknown' }
    
    currentListOfDomains.append(newDomain)        

    with open(userDoaminFile, 'w') as f:
        json.dump(currentListOfDomains, f, indent=4)        
        return successMessage



# function to read from file a list of domain and add to domain file.

def add_bulk(userName,fileName):
    fileName=fileName.replace('"','')
    print (fileName , userName)
    try:
        with open(fileName, 'r') as infile:
            for line in infile:
                add_domain(userName,line.strip())
    
    except Exception as e:
        return (str(e))
     
    return "Bulk upload finished"




# Function to validate the domain name

def is_valid_domain(s):
    # Regex to check valid Domain Name
    pattern = r"^[A-Za-z0-9-]{1,63}\.[A-Za-z0-9-]{0,63}\.[A-Za-z]{2,6}$"
    #pattern= r"^((?!-)[A-Za-z0-9-]{1, 63}(?<!-)\\.)+[A-Za-z]{2, 6}$"

    # Return true if the string matches the regex
    #return bool(re.match(pattern, s))
    return True


# add_bulk("alex" , "Domains_for_upload.txt")
# add_bulk("Eli" , "Domains_for_upload.txt")
