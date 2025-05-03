from flask_app import app
from flask import render_template,session,redirect,request,flash
from flask_app.model.employee_model import Employee
from flask_app.model.recipes_model import Recipe
from flask_app.model.owner_model import Owner
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/employee_reg')
def employee_reg():
    data={'owner_id':session['user_id']}
    all_employees= Employee.get_all(data)
    return render_template('employees_registration.html',all_employees=all_employees)


@app.route('/reg_employee', methods=['post'])
def register_employee():
    if Employee.validate(request.form):
        pw_hash=bcrypt.generate_password_hash(request.form['password'])
        data={**request.form,'password':pw_hash,'owner_id':session['user_id']}
        employee_id=Employee.create(data)
        return redirect("/employee_reg")
    return redirect("/employee_reg")


@app.route('/login', methods=['post'])
def login():
    user_from_owner_db=Owner.get_by_email({'email':request.form['email']})
    user_from_db=Employee.get_by_email({'email':request.form['email']})
    
    if request.form['email']=="admin@admin.com" and request.form['password']=="admin":
        session['user_id']=1
        return redirect('/owner_register')

    if not user_from_owner_db and not user_from_db :
        flash("Email doesn't exist.try to register first","login")
        return redirect('/log')
    if user_from_owner_db:
        if not bcrypt.check_password_hash(user_from_owner_db.password,request.form["password"]):
            flash("Password wrong please try again","login")
            return redirect('/log')
    if user_from_db:
        if not bcrypt.check_password_hash(user_from_db.password,request.form["password"]):
            flash("Password wrong please try again","login")
            return redirect('/log')
    
    if user_from_owner_db:
        session['user_id']=user_from_owner_db.id
        return redirect("/dashboard")
    if user_from_db :
        session['user_id']=user_from_db.id
        return redirect("/cash_register")