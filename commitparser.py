import requests
import json
from pprint import * # For nice debugging messages
from termcolor import colored # For debugging colors 

import whatthepatch # for diff handling
import os # for deleting files

authentication = ( "tadeuszk733" , "<Put Token Here>" )

class diff():
    filename = ""
    patch    = ""
    url      = "" # DEV
    status   = ""



def get_diffs(commit_url) :
    '''
    Return list of diff objects associated with commit url in the form: 
    https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/691f310af5a7d176b6d52bf9176375a288a83ed9
    '''
    diff_container = []

    r = requests.get(
        commit_url ,
        auth=authentication
    )
    commits = json.loads(r.text) # Parse response    
    for line in commits["files"] : 
        d = diff()
        d.filename = line["filename"]
        d.patch = line["patch"]
        d.status = line["status"]
        d.url = commit_url # DEV
        diff_container+=[d]
    return diff_container

def get_diffs_dev(commit_url) :
    '''
    Return list of diff objects associated with commit url in the form: 
    https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/691f310af5a7d176b6d52bf9176375a288a83ed9
    '''
    diff_container = []

    r = requests.get(
        commit_url ,
        auth=authentication
    )
    commits = json.loads(r.text) # Parse response

    #pprint(commits)
    
    
    for line in commits["files"] : 
        print( line["status"] )
    

def get_commits(repo_url) :
    '''
    Return list of commit urls in chronological order, 
    WARNING: each commit can contain multiple diffs !
    '''
    # Change repo_url "https://github.com/HakierGrzonzo/tinyPub"
    # into api_call_url "https://api.github.com/repos/HakierGrzonzo/tinyPub/commits"
    api_call_url = repo_url.replace(
        "github.com/",
        "api.github.com/repos/"
    ) 
    if api_call_url[-1] != '/' :
        api_call_url += '/'
    api_call_url += "commits"

    # Call github api
    r = requests.get( 
        api_call_url,
        auth=authentication,
    )     

    # Parse api response
    reverse_order_response = json.loads( r.text ) 
    url_list = []
    for part in reversed(reverse_order_response) :
        url = part["url"]
        url_list += [url]

    return url_list




repo = "https://github.com/HakierGrzonzo/tinyPub"

commit_list = get_commits(repo)

'''
l = ['https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/7dfb244bb20fe95150c37286ff9b0eb7556e8297', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/7dfb244bb20fe95150c37286ff9b0eb7556e8297', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/8786b71ceb9bc2deff83e22ea06d7a1c1aa80e44', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/8786b71ceb9bc2deff83e22ea06d7a1c1aa80e44', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/8786b71ceb9bc2deff83e22ea06d7a1c1aa80e44', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/edf13b1fa9b12537e26847c143740bae0745f83c', 'https://api.github.com/repos/HakierGrzonzo/tinyPub/commits/131a3c940ce3c0afd49daa2128e7d6bffa4fec85']

'''

# Try to rebuild a repo from diffs only
# NOTE: create the folder before using

folder = "test/"
l =[] # DEV

for url in commit_list :
    for d in get_diffs(url) :
        d.filename = folder+d.filename
        try:
            if d.status == "removed" :
                try:
                    os.remove(d.filename)
                except:
                    print("File deleted twice")
            else: 
                if d.status == "added" :
                    text = ''
                elif d.status == "modified" :
                    text = open(d.filename , 'r').read()
                else :
                    print(colored("Undefined file status", "red"))

                print(colored("Patching "+d.filename, "green"))
            
                for dif in whatthepatch.parse_patch( d.patch ) :
                    text = whatthepatch.apply_diff(dif , text)
                    text = ''.join(x+'\n' for x in text)
                f = open(d.filename, 'w' )
                f.write(text)
                f.close()
        except Exception as e:
            print(colored("Failed on "+d.filename, "red"))
            print(colored(d.url , "yellow"))  # DEV
            l+=[d.url] # DEV
            print(e)
'''
#test
#'''







print("\n\nend")