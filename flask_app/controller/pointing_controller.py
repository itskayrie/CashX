from flask_app import app
from flask import render_template, redirect, request, flash, session,url_for
from flask_app.model.pointing_model import Pointing
from flask_app.model.employee_model import Employee


@app.route("/all_pointings")
def all_pointings():
    data={'id':session['user_id']}
    connected_cashier=Employee.get_by_id(data)
    datax={'owner_id':connected_cashier.owner_id}
    pointings = Pointing.get_all(datax)
    all_employees=Employee.get_all(datax)
    return render_template("pointings.html",pointings=pointings,all_employees=all_employees)

@app.route("/pointings/create",methods=['post'])
def createpointing():
    if Pointing.validate(request.form):
        data={'id':session['user_id']}
        connected_cashier=Employee.get_by_id(data)
        data={**request.form,'owner_id':connected_cashier.owner_id}
        Pointing.create(data)
        return redirect("/all_pointings")
    return redirect("/all_pointings")

@app.route('/pointings/<int:id>/destroy')
def destroy_all_pointings(id):
    if not 'user_id' in session:
        return redirect('/log')
    Pointing.destroy({'id':id})
    return redirect("/all_pointings")
