from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Pointing:
    def init(self, data):
        self.id = data["id"]
        self.employees_id = data["employees_id"]
        self.hours_number = data["hours_number"]
        self.owner_id = data["owner_id"]
        self.date = data["date"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]


    @classmethod
    def create(cls,data):
        query="""INSERT INTO pointings
                        (employees_id,hours_number,date,owner_id)
                        VALUES (%(employees_id)s,%(hours_number)s,%(date)s,%(owner_id)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls,datax):
        query = "SELECT * FROM pointings WHERE owner_id=%(owner_id)s;"
        results=connectToMySQL(DATABASE).query_db(query,datax)
        all_pointings=[]
        for row in results:
            all_pointings.append(row)
        return all_pointings
    @classmethod
    def get_by_id(cls,data):
        query="""SELECT * FROM pointings WHERE id=%(id)s;"""
        result=connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return None

    @classmethod
    def destroy(cls,data):
        query="""DELETE FROM pointings WHERE id=%(id)s;"""
        return connectToMySQL(DATABASE).query_db(query,data)
# --------------------------------------------------------------------------
    @classmethod
    def pointings_2_dates_per_employee(cls,data):
            query="""SELECT SUM(hours_number) as total
                        FROM pointings
                        WHERE (DATE(date) BETWEEN %(date1)s AND %(date2)s) and owner_id= %(owner_id)s group by pointings.employees_id ;"""
            results=connectToMySQL(DATABASE).query_db(query,data)
            total=[]
            for row in results:
                total.append(row)
            print(total)
            return total
    @classmethod
    def pointings_2_dates_total(cls,data):
            query="""SELECT SUM(hours_number) as total
                        FROM pointings
                        WHERE (DATE(date) BETWEEN %(date1)s AND %(date2)s) and owner_id= %(owner_id)s ;"""
            results=connectToMySQL(DATABASE).query_db(query,data)
            return results
    
    @staticmethod
    def validate(data):
        is_valid=True
        # if len(data['employees_id'])=="":
        #     is_valid=False
        #     flash("choose employee !")
        if len(data['date'])== "":
            is_valid=False
            flash(" date is required !")
        # if (data['hours_number'])==None:
        #     is_valid=False
        #     flash("hours_number must be provided !")
        print(is_valid)
        return is_valid