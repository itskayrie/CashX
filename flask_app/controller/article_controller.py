from flask_app import app
from flask import render_template, redirect, request, flash, session,url_for
from flask_app.model.article_model import Articles

@app.route("/all_articles")
def all():
    data={'owner_id':session['user_id']}
    articles = Articles.get_all(data)
    return render_template("all_articles.html",articles=articles)

@app.route("/articles/new")
def add():
    return render_template("add_article.html")


@app.route("/create",methods=['post'])
def create():
    # print("qqqqqqq",Articles.validate(request.form))
    if Articles.validate(request.form):
        data={
        **request.form,"stock_value":float(request.form["article_price"])*float(request.form["quantity_in_stock"]),"owner_id":session["user_id"]
        }
        # print(data)
        Articles.create(data)
        return redirect("all_articles")
    return redirect("add_articles")


@app.route('/articles/<int:id>/edit')
def edit_article(id):
    article=Articles.get_by_id({'id':id})
    return render_template('edit_article.html',article=article)

@app.route('/articles/update',methods=['post'])
def update_article():
    if Articles.validate(request.form):
        data={
        **request.form,"stock_value":float(request.form["article_price"])*float(request.form["quantity_in_stock"]),"owner_id":session["user_id"]
        }
        print("🦋🦋🦋🦋🦋🦋🦋🦋",data,"🦋🦋🦋🦋🦋🦋🦋🦋")
        Articles.update(data)
        return redirect('/all_articles')
    return redirect (f'/articles/{request.form["id"]}/edit')

@app.route('/articles/<int:id>/destroy')
def destroy_article(id):
    if not 'user_id' in session:
        return redirect('/')
    Articles.destroy({'id':id})
    return redirect("/all_articles")
