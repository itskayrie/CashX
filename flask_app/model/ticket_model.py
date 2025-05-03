from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import session
from flask import flash
from datetime import date,datetime




class Ticket:
        def init(self, data):
            self.id = data["id"]
            self.employee_id = data["employee_id"]
            self.total = data["total"]
            self.created_at = data["created_at"]
            self.updated_at = data["updated_at"]


        @classmethod
        def create_ticket(cls, data):
            ticket_query = """
                INSERT INTO tickets (employee_id,total) 
                VALUES (%(employee_id)s,%(total)s);
            """
            x=connectToMySQL(DATABASE).query_db(ticket_query, data)
            return x

        @classmethod
        def add_recipe_to_ticket(cls, data):

            query = """
                INSERT INTO recipes_has_tickets (ticket_id, recipe_id, quantity_per_ticket) 
                VALUES (%(ticket_id)s, %(recipe_id)s, %(quantity_per_ticket)s);
            """
            return connectToMySQL(DATABASE).query_db(query,data)
        
        @classmethod
        def substract_quantity(cls, data):
            query = """
                        UPDATE articles
                        JOIN (
                        SELECT
                        ahr.article_id,
                        SUM(ahr.article_per_recipe * rht.quantity_per_ticket) AS total_quantity
                        FROM
                        tickets t
                        JOIN recipes_has_tickets rht ON t.id = rht.ticket_id
                        JOIN articles_has_recipes ahr ON rht.recipe_id = ahr.recipe_id
                        WHERE
                        t.id = %(ticket_id)s
                        GROUP BY
                        ahr.article_id
                        ) AS subquery ON articles.id = subquery.article_id
                        SET articles.quantity_in_stock = articles.quantity_in_stock - subquery.total_quantity,
                        articles.stock_value = articles.article_price * (articles.quantity_in_stock - subquery.total_quantity);"""
            query2="""  """
            connectToMySQL(DATABASE).query_db(query,data)
            return connectToMySQL(DATABASE).query_db(query2,data)
        
        @classmethod
        def get_all_today(cls):
            dat = date.today()
            owner=session['user_id']
            query=f"""SELECT * FROM tickets WHERE DATE(created_at)='{dat}' and employee_id={owner};"""
            results=connectToMySQL(DATABASE).query_db(query)
            today_tickets=[]
            print(results)
            for row in results:
                today_tickets.append(row)
            print(today_tickets)
            return today_tickets
        @classmethod
        def get_products_today(cls):
            dat = date.today()
            owner=session['user_id']
            query=f"""SELECT SUM(quantity_per_ticket) as qte, recipes.recipe_name , recipes.recipe_price
                    FROM recipes_has_tickets
                    JOIN recipes 
                    ON recipes_has_tickets.recipe_id = recipes.id
                    JOIN tickets
                    ON recipes_has_tickets.ticket_id = tickets.id WHERE DATE(tickets.created_at)='{dat}' and employee_id={owner} 
                    GROUP by recipe_name , recipe_price;"""
            results=connectToMySQL(DATABASE).query_db(query)
            today_products=[]
            print(results)
            for row in results:
                today_products.append(row)
            print(today_products)
            return today_products
        
        @classmethod
        def sales_today(cls):
            dat = date.today()
            owner=session['user_id']
            query=f"""SELECT SUM(quantity_per_ticket*recipes.recipe_price) as total
                        FROM recipes_has_tickets
                        JOIN recipes 
                        ON recipes_has_tickets.recipe_id = recipes.id
                        JOIN tickets
                        ON recipes_has_tickets.ticket_id = tickets.id 
                        WHERE DATE(tickets.created_at)='{dat}' and employee_id={owner};"""
            results=connectToMySQL(DATABASE).query_db(query)
            total=results[0]
            print(total)
            return total
        # -------------------------------------------------------
        @classmethod
        def top_products_2_dates(cls,data):
            date1 = data['date1']
            date2 = data['date2']
            owner=session['user_id']
            query=f"""SELECT SUM(quantity_per_ticket) as qte, recipes.recipe_name , recipes.recipe_price
                    FROM recipes_has_tickets
                    JOIN recipes 
                    ON recipes_has_tickets.recipe_id = recipes.id
                    JOIN tickets
                    ON recipes_has_tickets.ticket_id = tickets.id WHERE (DATE(tickets.created_at)
                    BETWEEN '{date1}' AND '{date2}') and owner_id={owner} 
                    GROUP by recipe_name , recipe_price;"""
            results=connectToMySQL(DATABASE).query_db(query)
            top_products=[]
            print(results)
            for row in results:
                top_products.append(row)
            print(top_products)
            return top_products
        @classmethod
        def sales_2_dates(cls,data):
            date1 = data['date1']
            date2 = data['date2']
            owner=session['user_id']
            query=f"""SELECT SUM(quantity_per_ticket*recipes.recipe_price) as total
                        FROM recipes_has_tickets
                        JOIN recipes 
                        ON recipes_has_tickets.recipe_id = recipes.id
                        JOIN tickets
                        ON recipes_has_tickets.ticket_id = tickets.id 
                        WHERE  (DATE(tickets.created_at)
                    BETWEEN '{date1}' AND '{date2}') and owner_id={owner} ;"""
            results=connectToMySQL(DATABASE).query_db(query)
            total=results[0]
            print(total)
            return total