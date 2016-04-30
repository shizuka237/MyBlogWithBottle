import hmac
import random
import string
import hashlib
import pymongo
import datetime


# The Posts Data Access Object handles all interactions with the Posts collection.
class PostsDAO:

    def __init__(self, db):
        self.db = db
        self.posts = self.db.posts
        self.SECRET = 'verysecret'
 
    #function for adding posts to the posts collection
    def add_posts(self,username , post):
        new_post ={ '_id' : post['id'], 
                             'owner' : username,
                             'head': post['heading'],
                             'text':   post['content'],
                             }
        print new_post
        user =self.posts.insert(new_post)
        
     #return all posts in the database
    def get_posts(self ):
         doc = self.posts.find()
         return doc
         
    def get_user_posts(self ,username):
         doc = self.posts.find({'owner':username})
         return doc
   
   #function to return a single post      
    def get_post(self , pid):
         doc = self.posts.find_one({'_id':pid})
         return doc
         

