import os
from dotenv import load_dotenv
from urllib.parse import urlencode

from flask import Flask, render_template, request, redirect, url_for, abort
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask_migrate import Migrate

from app.extansions import db
from app.models import Company, Orders
from app.utils import generate_signature


admin_ext = Admin(template_mode='bootstrap3')
migrate_ext = Migrate()
load_dotenv()


def create_app(testing=False):
    new_app = Flask(__name__)
    if testing:
        new_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    else:
        new_app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
    new_app.config["SECRET_KEY"] = 'TypeMeIn'
    db.init_app(new_app)
    migrate_ext.init_app(new_app, db)
    admin_ext.init_app(new_app)

    @new_app.route("/process", methods=["POST", "GET"])
    def payment_page():
        '''
        http://127.0.0.1:6018/process?company_id=1&order_id=1&callback_url=https://ya.ru&price=1000
        :return:
        '''
        company_id = request.args.get("company_id")
        order_id = request.args.get("order_id")
        callback_url = request.args.get("callback_url")
        price = request.args.get("price")
        print(order_id)
        print(request.args, type(request.args))
        if not (company_id and order_id and callback_url and price):
            return abort(404)

        company = Company.query.get_or_404(1)
        if request.method == "POST":
            print(request.form, type(request.form))
            new_order = Orders(price=price, status="pending", company_id=company_id)
            db.session.add(new_order)
            db.session.commit()
            query_params = {'status': new_order.status, 'company_id': company_id, 'order_id': order_id}
            query_params['signature'] = generate_signature(query_params)
            return redirect(callback_url + '?' + urlencode(query_params))
        return render_template("payment_page.html",
                               company=company, order_id=order_id,
                               callback_url=callback_url, price=price)



    return new_app




class MyModelView(ModelView):
    column_display_all_relations = True
    column_hide_backrefs = False


admin_ext.add_view(MyModelView(Company, db.session))
admin_ext.add_view(MyModelView(Orders, db.session))

