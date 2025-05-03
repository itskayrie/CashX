from flask_app import app
from flask import render_template, redirect, request, flash, session,url_for
from flask_app.model.purchase_model import Purchase
from flask_app.model.article_model import Articles


@app.route("/all_purchases")
def allpurchases():
    data={'owner_id':session['user_id']}
    purchases = Purchase.get_all(data)
    all_articles=Articles.get_all(data)
    return render_template("purchase.html",purchases=purchases,all_articles=all_articles)

@app.route("/purchases/create",methods=['post'])
def createpurchase():
    if Purchase.validate(request.form):
        data={**request.form,'owner_id':session['user_id']}
        Purchase.create(data)
        return redirect("/all_purchases")
    return redirect("/all_purchases")

@app.route('/purchases/<int:id>/destroy')
def destroy_purchase(id):
    if not 'user_id' in session:
        return redirect('/log')
    Purchase.destroy({'id':id})
    return redirect("/all_purchases")
