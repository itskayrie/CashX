from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash


class Articles:
    def __init__(self, data):
        self.id = data["id"]
        self.article_name = data["article_name"]
        self.quantity_in_stock = data["quantity_in_stock"]
        self.supplier = data["supplier"]
        self.article_price = data["article_price"]
        self.stock_value = data["stock_value"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    

    @classmethod
    def create(cls,data):
        
        query="""INSERT INTO articles 
                            (article_name,quantity_in_stock,supplier,stock_value,article_price,owner_id)
                            VALUES (%(article_name)s,%(quantity_in_stock)s,%(supplier)s,%(stock_value)s,%(article_price)s,%(owner_id)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def get_all(cls,data):
        query = "SELECT * FROM articles WHERE owner_id=%(owner_id)s;"
        results=connectToMySQL(DATABASE).query_db(query,data)
        allArticles=[]
        for row in results:
            
            allArticles.append(cls(row))
        return allArticles
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM articles WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return cls(result[0]) if result else None
    @classmethod
    def get_by_id(cls,data):
        query="""SELECT * FROM articles WHERE id=%(id)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return None
    
    @classmethod
    def update(cls,data):
        print("🐝"*10, data,"🐝"*10)
        query=""" UPDATE articles SET 
        article_name=%(article_name)s,quantity_in_stock=%(quantity_in_stock)s,
        stock_value=%(stock_value)s,article_price=%(article_price)s
                WHERE id=%(id)s; """
        return connectToMySQL(DATABASE).query_db(query,data)
    @classmethod
    def destroy(cls,data):
        query="""DELETE FROM articles WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @staticmethod   
    def validate(data):
        is_valid=True
        if len(data['article_name'])<3:
            is_valid=False
            flash("article_name is required")
        if len(data['article_name'])<3:
            is_valid=False
            flash(" article_name is required")
        if (data['article_price'])==None:
            is_valid=False
            flash("article_price must be provided")
        if (data['quantity_in_stock'])==None:
            is_valid=False
            flash("quantity_in_stock must be provided")
        print(is_valid)
        return is_valid