from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Employee:
    def __init__(self,data):
        self.id=data["id"]
        self.first_name=data["first_name"]
        self.last_name=data["last_name"]
        self.email=data["email"]
        self.password=data["password"]
        self.role=data["role"]
        self.owner_id=data["owner_id"]
    
    @classmethod
    def create(cls,data):
        
        print("🎆"*10)
        query="""INSERT INTO employees (first_name,last_name,email,password,role,owner_id) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,%(role)s,%(owner_id)s);"""
        x=connectToMySQL(DATABASE).query_db(query,data)
        print(x)
        return x
    @classmethod
    def get_all(cls,data):
        query = """SELECT * FROM employees WHERE owner_id=%(owner_id)s;"""
        results=connectToMySQL(DATABASE).query_db(query,data)
        all_employees=[]
        for row in results:
            all_employees.append(cls(row))
        return all_employees
    
    @classmethod
    def get_by_id(cls,data):
        query="""SELECT * FROM employees WHERE id=%(id)s"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
    
    @classmethod
    def get_by_email(cls, data):
        query = """SELECT * FROM employees WHERE email=%(email)s"""
        result = connectToMySQL(DATABASE).query_db(query, data)

        if result:
            print("❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️❤️", result[0])
            return cls(result[0])
        return False  # Change False to None

    
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
        # if len(data["role"])=="":
        #     is_valid=False
        #     flash("you must select a role !","register")    
        # email validation
        # email pattern:regex
        # if not EMAIL_REGEX.match(data['email']):
        #     flash("invalid email address","register")
        #     is_valid=False
        # #email must be unique
        # if Owner.get_by_email({'email':data['email']}):
        #     flash("Email already in use, hope by you","register")
        #     is_valid=False
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