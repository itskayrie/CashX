from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.model import owner_model

class Recipe:
    def __init__(self,data):
        self.id=data["id"]
        self.owner_id=data["owner_id"]
        self.recipe_name=data["recipe_name"]
        self.instructions=data["instructions"]
        self.recipe_price=data["recipe_price"]
        self.recipe_image=data["recipe_image"]
        self.description=data["description"]
        
    
    @classmethod
    def create(cls,data):
        query="""INSERT INTO recipes 
                            (owner_id,recipe_name,instructions,recipe_price,recipe_image,description)
                            VALUES (%(owner_id)s,%(recipe_name)s,%(instructions)s,%(recipe_price)s,%(recipe_image)s,%(description)s);"""
        x=connectToMySQL(DATABASE).query_db(query,data)
        # print(data)
        for i in range (1,int(data['article_count'])+1):
            datax={
                'article_id':int(data[f'article_{i}']),
                'article_per_recipe':float(data[f'article_qte_{i}']),
                'recipe_id':x
            }
            query="""INSERT INTO articles_has_recipes 
                            (recipe_id,article_id,article_per_recipe)
                            VALUES (%(recipe_id)s,%(article_id)s,%(article_per_recipe)s);"""
            connectToMySQL(DATABASE).query_db(query,datax)
        return x
    
    @classmethod
    def get_all(cls,data):
        query="""SELECT * FROM recipes WHERE owner_id=%(owner_id)s;"""
        results=connectToMySQL(DATABASE).query_db(query,data)
        all_recipes=[]
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes
    
    @classmethod
    def get_by_id(cls,data):
        query="""SELECT * FROM recipes WHERE id=%(id)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return None
    @classmethod
    def get_by_name(cls,data):
        query="""SELECT * FROM recipes WHERE recipe_name=%(recipe_name)s"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return False
    
    @classmethod
    def update(cls,data):
        print("🐝"*10, data,"🐝"*10)
        query=""" UPDATE recipes SET recipe_name=%(recipe_name)s,instructions=%(instructions)s,recipe_price=%(recipe_price)s,
                recipe_image=%(recipe_image)s,description=%(description)s WHERE id=%(id)s; """
        return connectToMySQL(DATABASE).query_db(query,data)
    @classmethod
    def destroy(cls,data):
        query2="""DELETE FROM articles_has_recipes WHERE recipe_id=%(id)s;"""
        query="""DELETE FROM recipes WHERE id=%(id)s;"""
        result1 = connectToMySQL(DATABASE).query_db(query2,data)
        result2 = connectToMySQL(DATABASE).query_db(query,data)
        return result2
            
    @staticmethod
    def validate(data):
        is_valid=True
        if len(data['recipe_name'])<3:
            is_valid=False
            flash(" recipe name is required")
        if len(data['instructions'])<3:
            is_valid=False
            flash("recipe instructions is required")
        if len(data['description'])<3:
            is_valid=False
            flash("recipe description must be at least 10")
        if (data['recipe_price'])=="":
            is_valid=False
            flash("recipe price must be provided")
        return is_valid