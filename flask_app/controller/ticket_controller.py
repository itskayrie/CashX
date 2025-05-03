from flask_app import app

from flask import render_template,session,redirect,request,jsonify
import json
from flask_app.model.employee_model import Employee
from flask_app.model.recipes_model import Recipe
from flask_app.model.ticket_model import Ticket

@app.route('/cash_register')
def cash_register():
    data={'id':session['user_id']}
    employees=Employee.get_by_id(data)
    print(employees,")))))))))))))")
    datax={'owner_id':employees.owner_id}
    recipes = Recipe.get_all(datax)
    return render_template('cash_register.html',recipes=recipes)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    total= float(request.form.get('totalAmount'))
    data={'total':total,'employee_id':session['user_id']}
    x=Ticket.create_ticket(data)
    cart_items_json = request.form.get('cartItems')
    cart_items = json.loads(cart_items_json)
    for i in cart_items:
        name={'recipe_name':i['name']}
        datax={'ticket_id':x,'recipe_id':Recipe.get_by_name(name).id,'quantity_per_ticket':i['quantity']}
        Ticket.add_recipe_to_ticket(datax)
        Ticket.substract_quantity(datax)

    return redirect('/cash_register')

@app.route('/sales')
def sales_redirect():
    all_tickets=Ticket.get_all_today()
    count_ticket=len(all_tickets)
    all_products=Ticket.get_products_today()
    count_total=Ticket.sales_today()['total']
    return render_template('sails.html',all_tickets=all_tickets,count_ticket=count_ticket,all_products=all_products,count_total=count_total)

