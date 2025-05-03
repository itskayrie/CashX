from flask_app import app
from flask import render_template,session,redirect,request
from flask_app.model.recipes_model import Recipe
from flask_app.model.article_model import Articles


@app.route("/all_recipes")
def all_recipes():
    data={'owner_id':session['user_id']}
    recipes = Recipe.get_all(data)
    return render_template("all_recipes.html",recipes=recipes)

@app.route('/recipes/new')
def new_recipe():
    if not 'user_id' in session:
        return redirect('/log')
    data={'owner_id':session['user_id']}
    all_articles=Articles.get_all(data)
    return render_template('add_recipe.html',all_articles=all_articles)

@app.route('/recipes/<int:id>')
def one_recipe(id):
    recipe=Recipe.get_by_id({'id':id})
    return render_template('view_recipe.html',recipe=recipe)

@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    recipe=Recipe.get_by_id({'id':id})
    return render_template('edit_recipe.html',recipe=recipe)


@app.route('/recipes/create',methods=['post'])
def create_recipe():
    if Recipe.validate(request.form):
        data={**request.form,"owner_id":int(session['user_id'])}
        print("🦋🦋🦋🦋🦋🦋🦋🦋",data,"🦋🦋🦋🦋🦋🦋🦋🦋")
        db_return=Recipe.create(data)
        print(db_return)
        return redirect('/all_recipes')
    return redirect ('/recipes/new')

@app.route('/recipes/update',methods=['post'])
def update_recipe():
    if Recipe.validate(request.form):
        data={**request.form}
        print("🦋🦋🦋🦋🦋🦋🦋🦋",data,"🦋🦋🦋🦋🦋🦋🦋🦋")
        Recipe.update(data)
        # print(db_return)
        return redirect('/all_recipes')
    return redirect (f'/recipes/{request.form["id"]}/edit')

@app.route('/recipes/<int:id>/destroy')
def destroy_recipe(id):
    Recipe.destroy({'id':id})
    return redirect("/all_recipes")



