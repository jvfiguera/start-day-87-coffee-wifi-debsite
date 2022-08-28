import random
from flask import Flask, jsonify, render_template, request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,RadioField,Label,SelectField
from flask_ckeditor import CKEditor, CKEditorField
from wtforms.validators import DataRequired, URL,InputRequired, Length

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

db_all_coffee_shops   =[]
##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
has_dict={'Yes':1,'No':0}
get_all =1
# Cofee Form
class CreateCofeeForm(FlaskForm):
    name                = StringField("Local Coffee name:",validators=[DataRequired(),Length(max=100)])
    map_url             = StringField("Ulr Map",validators=[DataRequired(),URL(),Length(max=100)])
    img_url             = StringField("Ulr img",validators=[DataRequired(),URL(),Length(max=100)])
    location            = StringField("Localidad",validators=[DataRequired(),Length(max=20)])
    has_sockets         = SelectField(u'Has it Sockets: ?', choices=["Yes", "No"], default="Yes", validators=[DataRequired()])
    has_toilet          = SelectField(u'Has it toilet: ?', choices=["Yes", "No"], default="Yes", validators=[DataRequired()])
    has_wifi            = SelectField(u'Has it wifi: ?', choices=["Yes", "No"], default="Yes",validators=[DataRequired()])
    can_take_calls      = SelectField(u'Can I take calls: ?', choices=["Yes", "No"],default="Yes",validators=[DataRequired()])
    seats               = StringField("Seats number : ?",validators=[DataRequired(),Length(max=5)])
    coffee_price        = StringField("Coffee price ?",validators=[DataRequired(),Length(max=5)])
    submit              = SubmitField("Done")
    # has_sockets     = StringField("Has it Sockets: ?",validators=[DataRequired()])
    # has_toilet      = StringField("Has it toilet: ?",validators=[DataRequired()])
    # has_wifi        = StringField("Has it wifi: ?",validators=[DataRequired()])
    # can_take_calls  = StringField("can it take calls: ?",validators=[DataRequired()])

#Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

#Definicion de Funciones
def fn_query_all_coffee_shops():
    global db_all_coffee_shops
    db_all_coffee_shops    = db.session.query(Cafe).all()

def fn_query_coffee_shops(pHas_filter):
    global db_all_coffee_shops,get_all
    if pHas_filter == 'socket':
        db_all_coffee_shops = db.session.query(Cafe).filter_by(has_sockets=1).all()
    elif pHas_filter == 'toilet':
        db_all_coffee_shops = db.session.query(Cafe).filter_by(has_toilet=1).all()
    elif pHas_filter == 'wifi':
        db_all_coffee_shops = db.session.query(Cafe).filter_by(has_wifi=1).all()
    elif pHas_filter == 'calls':
        db_all_coffee_shops = db.session.query(Cafe).filter_by(can_take_calls=1).all()
    else : # All coffee Shops
        get_all =1

@app.route("/")
def fn_home():
    global get_all
    if get_all == 1:
        fn_query_all_coffee_shops()
    return render_template("index.html"
                           ,data_coffee_shops=db_all_coffee_shops
                           )

@app.route("/fn_filter_shop_coffee/<has_filter>",methods=["PATCH","POST","GET"])
def fn_filter_shop_coffee(has_filter):
    global get_all
    get_all =0
    fn_query_coffee_shops(has_filter)
    return redirect(url_for("fn_home"))

@app.route("/fn_add_shop_coffee", methods=["GET","POST"])
def fn_add_shop_coffee():
    form= CreateCofeeForm()
    if form.validate_on_submit():
        new_coffee_shop=  Cafe(name             = form.name.data
                               ,map_url         = form.map_url.data
                               ,img_url         = form.img_url.data
                               ,location        = form.location.data
                               ,has_sockets     = has_dict[form.has_sockets.data]
                               ,has_toilet      = has_dict[form.has_toilet.data]
                               ,has_wifi        = has_dict[form.has_wifi.data]
                               ,can_take_calls  = has_dict[form.can_take_calls.data]
                               ,seats           = form.seats.data
                               ,coffee_price    = form.coffee_price.data
                               )

        db.session.add(new_coffee_shop)
        db.session.commit()
        return redirect(url_for("fn_home"))
    return render_template(template_name_or_list="add.html"
                           ,page_title = "ADD NEW COFFEE SHOP"
                           ,form=form
                           )
@app.route("/fn_del_shop_coffee/<cafe_id>", methods=["PATCH","POST","GET"])
def fn_del_shop_coffee(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("fn_home"))


if __name__ == '__main__':
    app.run(debug=True)
