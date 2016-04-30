
import hmac
import random
import string
import hashlib
import pymongo
import datetime


# The User Data Access Object handles all interactions with the User collection.
class UserDAO:

    def __init__(self, db):
        self.db = db
        self.users = self.db.users
        self.SECRET = 'verysecret'
 
    #function for adding posts to the user
    def add_posts(self,username , post):
        new_post ={ '_id' : post['id'] ,
                            'head' : post['heading']}
        print new_post
        #print self.users.find_one({'_id':username})
        user =self.users.update({'_id':username},
                                                    {  '$push' : { 'posts': new_post} }
                                                    )
        
      
    def get_posts(self , username):
         doc = self.users.find_one({'_id':username})
         return doc['posts']
         

    # makes a little salt
    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    # implement the function make_pw_hash(name, pw) that returns a hashed password
    # of the format:
    # HASH(pw + salt),salt
    # use sha256

    def make_pw_hash(self, pw,salt=None):
        if salt == None:
            salt = self.make_salt();
        return hashlib.sha256(pw + salt).hexdigest()+","+ salt

    # Validates a user login. Returns user record or None
    def validate_login(self, username, password):

        user = None
        try:
            # XXX HW 2.3 Students Work Here
            # you will need to retrieve right document from the users collection.
            user=self.users.find_one({'_id':username})
            print "This space intentionally left blank."
        except:
            print "Unable to query database for user"

        if user is None:
            print "User not in database"
            return None

        salt = user['password'].split(',')[1]

        if user['password'] != self.make_pw_hash(password, salt):
            print "user password is not a match"
            return None

        # Looks good
        return user


    # creates a new user in the users collection
    def add_user(self, username, password, email):
        password_hash = self.make_pw_hash(password)

        user = {'_id': username, 'password': password_hash,'posts':[]}
        if email != "":
            user['email'] = email

        try:
            # XXX HW 2.3 Students work here
            # You need to insert the user into the users collection.
            # Don't over think this one, it's a straight forward insert.
            self.users.insert(user)
            print "This space intentionally left blank."

        except pymongo.errors.OperationFailure:
            print "oops, mongo error"
            return False
        except pymongo.errors.DuplicateKeyError as e:
            print "oops, username is already taken"
            return False

        return True


