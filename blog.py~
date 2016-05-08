import pymongo
import sessionDAO ,userDAO , postsDAO
import bottle
import cgi
import re
import os
import datetime
import random
import string

wd=os.path.dirname(os.path.realpath(__file__))
print wd
__author__ = 'aje'



def make_salt():
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt
# General Discussion on structure. This program implements a blog. This file is the best place to start to get
# to know the code. In this file, which is the controller, we define a bunch of HTTP routes that are handled
# by functions. The basic way that this magic occurs is through the decorator design pattern. Decorators
# allow you to modify a function, adding code to be executed before and after the function. As a side effect
# the bottle.py decorators also put each callback into a route table.
# These are the routes that the blog must handle. They are decorated using bottle.py
# This route is the main page of the blog


@bottle.route('/')
def blog_index():

    cookie = bottle.request.get_cookie("session")
    
    username = sessions.get_username(cookie)
    
    # todo: this is not yet implemented at this point in the course
    all_posts=posts.get_posts();
    return bottle.template(wd+'/views/'+'blog_template.tpl.html', dict(username=username,all_posts = all_posts))




# displays the initial blog signup form
@bottle.get('/signup')
def present_signup():
    return bottle.template(wd+'/views/'+'signup.tpl.html',
                           dict(username="", password="",
                                password_error="",
                                email="", username_error="", email_error="",
                                verify_error =""))


# displays the initial blog login form
@bottle.get('/login')
def present_login():
    return bottle.template(wd+'/views/'+'login.tpl.html',
                           dict(username="", password="",
                                login_error=""))




# handles a login request
@bottle.post('/login')
def process_login():

    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")

    print "user submitted ", username, "pass ", password

    user_record = users.validate_login(username, password)
    if user_record:
        # username is stored in the user collection in the _id key
        session_id = sessions.start_session(user_record['_id'])

        if session_id is None:
            bottle.redirect("internal_error.tpl")

        cookie = session_id

        # Warning, if you are running into a problem whereby the cookie being set here is
        # not getting set on the redirect, you are probably using the experimental version of bottle (.12).
        # revert to .11 to solve the problem.
        bottle.response.set_cookie("session", cookie)

        bottle.redirect("welcome")

    else:
        return bottle.template(wd+'/views/'+'login.tpl.html',
                               dict(username=cgi.escape(username), password="",
                                    login_error="Invalid Login"))


@bottle.get('/internal_error')
@bottle.view('error_template')
def present_internal_error():
    return {'error':"System has encountered a DB error"}


@bottle.get('/logout')
def process_logout():

    cookie = bottle.request.get_cookie("session")

    sessions.end_session(cookie)

    bottle.response.set_cookie("session", "")


    bottle.redirect('signup')


@bottle.post('/signup')
def process_signup():

    email = bottle.request.forms.get("email")
    username = bottle.request.forms.get("username")
    password = bottle.request.forms.get("password")
    verify = bottle.request.forms.get("verify")

    # set these up in case we have an error case
    errors = {'username': cgi.escape(username), 'email': cgi.escape(email)}
    if validate_signup(username, password, verify, email, errors):

        if not users.add_user(username, password, email):
            # this was a duplicate
            errors['username_error'] = "Username already in use. Please choose another"
            return bottle.template(wd+'/views/'+'signup.tpl.html', errors)

        session_id = sessions.start_session(username)
        print session_id
        bottle.response.set_cookie("session", session_id)
        bottle.redirect("welcome")
    else:
        print "user did not validate"
        return bottle.template(wd+'/views/'+'signup.tpl.html', errors)



@bottle.get("/welcome")
def present_welcome():
    # check for a cookie, if present, then extract value

    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...redirecting to signup"
        bottle.redirect('signup')
    user_posts = posts.get_user_posts(username)
    print user_posts
    return bottle.template(wd+'/views/'+'welcome.tpl.html', {'username': username,'posts':user_posts})


#function to display a particular post
@bottle.get("/showpost")
def show_posts():
  print "hello"
   

#function to handle creation of the new posts
@bottle.get("/newpost")
def posts():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)  # see if user is logged in
    if username is None:
        print "welcome: can't identify user...redirecting to signup"
        bottle.redirect('signup')
        
    return bottle.template(wd+'/views/'+'mypost.tpl.html')
    
@bottle.post("/newpost")
def add_post():
    cookie = bottle.request.get_cookie("session")
    username = sessions.get_username(cookie)
    
    head =  bottle.request.forms.get("heading")
    string = bottle.request.forms.get("content")
    
    thispost ={
                       #generate a unique id for post 
                      'id' : str(datetime.datetime.now())+"_"+make_salt(),
                      'heading' : head ,
                     'content'  : string ,
                   }
                     
    users.add_posts(username,thispost)
    posts.add_posts(username,thispost)
    bottle.redirect("welcome")
    
    
    
   

# Helper Functions

# validates that the user information is valid for new signup, return True of False
# and fills in the error string if there is an issue
def validate_signup(username, password, verify, email, errors):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    PASS_RE = re.compile(r"^.{3,20}$")
    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

    errors['username_error'] = ""
    errors['password_error'] = ""
    errors['verify_error'] = ""
    errors['email_error'] = ""

    if not USER_RE.match(username):
        errors['username_error'] = "invalid username. try just letters and numbers"
        return False

    if not PASS_RE.match(password):
        errors['password_error'] = "invalid password."
        return False
    if password != verify:
        errors['verify_error'] = "password must match"
        return False
    if email != "":
        if not EMAIL_RE.match(email):
            errors['email_error'] = "invalid email address"
            return False
    return True

connection_string = "mongodb://localhost"
connection = pymongo.MongoClient(connection_string)
database = connection.blog

users = userDAO.UserDAO(database)
sessions = sessionDAO.SessionDAO(database)
posts =  postsDAO.PostsDAO(database)


bottle.debug(True)
bottle.run(host='localhost',port='8080')      # Start the webserver running and wait for requests

