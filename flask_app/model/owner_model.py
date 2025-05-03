from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Owner:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.business_name=data["business_name"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
    
    @classmethod
    def create(cls,data):
        query="""INSERT INTO owners
                            (first_name,last_name,email,password,business_name,admin_id)
                            VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(business_name)s,1)"""
        return connectToMySQL(DATABASE).query_db(query,data)
    @classmethod
    def get_all(cls):
        query="""SELECT * FROM owners;"""
        results=connectToMySQL(DATABASE).query_db(query)
        all_owners=[]
        for row in results:
            all_owners.append(cls(row))
        return all_owners
    @classmethod
    def get_by_email(cls,data):
        query="""SELECT * FROM owners WHERE email=%(email)s"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        
        if result:
            print("😂😂😂😂😂😂😂😂😂😂😂😂😂😂")
            return cls(result[0])
        return False
    
    @staticmethod
    def validate(data):
        is_valid=True
        # first & lastname validation
        if len(data["first_name"])<2:
            is_valid=False
            flash("First Name must contains 2 characters minimum ","register")
        if len(data["last_name"])<2:
            is_valid=False
            flash("last Name must contains 2 characters minimum ","register")
        # email validation
        # email pattern:regex
        if not EMAIL_REGEX.match(data['email']):
            flash("invalid email address","register")
            is_valid=False

        #password
        # password length
        if len(data["password"])<6:
            flash("Password too short","register")
            is_valid=False
        # compare password and confirm password
        elif data["password"]!=data["confirm_pw"]:
            flash("Password must match","register")
            is_valid=False
        return is_valid