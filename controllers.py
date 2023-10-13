from flask import render_template, request, redirect, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import *
from forms import *
from werkzeug.security import check_password_hash
from werkzeug.exceptions import Unauthorized
from app import app
import math

with app.app_context():
  from functions import *


@app.route("/search", methods=["POST", "GET"])
def search():
    # Search
    args = request.args
    if args.get('search'):
        products = Product.query.filter(Product.name.contains(args.get('search'))).all()
    # End Search

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("search.html", products=products, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/shop/", methods=["POST", "GET"])
def shop():
    # Pagenation
    products_per_page = 9
    page = int(request.args.get('page', 1))
    offset = (page - 1) * products_per_page
    total_products = Product.query.count()
    num_pages = math.ceil(total_products / products_per_page)
    products = Product.query.offset(offset).limit(products_per_page).all()
    # End Pagenation

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("shop.html", products=products, categories=categories, num_pages=num_pages, page=page, favorites_count=favorites_count, stocks=stocks)


@app.route("/shop/<category>", methods=["POST", "GET"])
def shop_category(category):
    # Category
    category_id = Category.query.filter(Category.name == category).first().id
    products_per_page = 9
    page = int(request.args.get('page', 1))
    offset = (page - 1) * products_per_page
    products = Product.query.filter(Product.category_id == category_id).all()
    total_products = len(products)
    products = Product.query.filter(Product.category_id == category_id).offset(offset).limit(products_per_page).all()
    num_pages = math.ceil(total_products / products_per_page)
    # End Category

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites
    return render_template("shop.html", products=products, category=category, categories=categories, num_pages=num_pages, page=page, favorites_count=favorites_count, stocks=stocks)


@app.route("/detail/<int:id>", methods=["POST", "GET"])
def detail(id):
    # Product
    product = Product.query.filter(Product.id==id).first()
    # End Product

    # Form Reviews
    post_data = request.form
    if request.method == 'POST':
        form = ReviewForm(data=post_data)
        if form.validate_on_submit():
            review = Reviews(current_user.full_name, form.message.data, product.id)
            review.save()
            return redirect(f'/detail/{id}')
    else:
        form = ReviewForm()
    # End Reviews

    # add or remove favorites
    favorites = []
    if current_user.is_authenticated:
        favorites = Favorites.query.filter(Favorites.user_id == current_user.id).all()
    products = [] # Hal-hazırdakı istifadəçinin favorit productları
    for favorite_item in favorites:
        products.append(Product.query.filter(Product.id == favorite_item.product_id).first())
    # end

    # Similar Products
    category_products = Product.query.filter(Product.category_id == product.category_id).all()
    # End Similar Products
    
    # Reviews
    reviews = Reviews.query.filter(Reviews.product_id == id).all()
    len_reviews = len(reviews)
    # End Reviews

    # Detail Images
    detail_images = Detail.query.filter(Detail.product_id == id).all()
    # End Detail Images

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("detail.html", product=product, products=products, reviews=reviews, len_reviews=len_reviews, form=form, category_products=category_products, detail_images=detail_images, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/add-to-favorites/<int:product_id>", methods=["POST"])
@login_required
def add_to_favorites(product_id):
    favorite = Favorites(current_user.id, product_id)
    favorite.save()
    return redirect(f'/detail/{product_id}')


@app.route("/remove-from-favorites/<int:product_id>", methods=["POST"])
@login_required
def remove_from_favorites(product_id):
    favorite = Favorites.query.filter(Favorites.user_id == current_user.id, Favorites.product_id == product_id).first()
    if favorite:
        favorite.remove()
    return redirect(f'/detail/{product_id}')


@app.route("/favorites")
@login_required
def favorites():
    if current_user.is_authenticated:
        favorites = Favorites.query.filter(Favorites.user_id == current_user.id).all()
    products = []
    for favorite_item in favorites:
        products.append(Product.query.filter(Product.id == favorite_item.product_id).first())
    categories = Category.query.all()

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("favorites.html", products=products, categories=categories, favorites_count=favorites_count, stocks = stocks)


@app.route("/remove-item/<int:product_id>", methods=["POST"])
@login_required
def remove_item(product_id):
    item = Favorites.query.filter(Favorites.user_id == current_user.id, Favorites.product_id == product_id).first()
    if item:
        item.remove()
        return redirect('/favorites')
    else:
        return 'Item not found'


@app.route("/contact", methods=['GET', 'POST'] )
def contact():
    # Contact Form
    post_data = request.form
    if request.method == 'POST':
        form = ContactForm(data=post_data)
        if form.validate_on_submit():
            message = Contact(form.full_name.data, form.email.data, form.subject.data, form.message.data)
            message.save()

            return redirect('/contact')
    else:
        form = ContactForm()
    # End Contact Form

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # Favorites Count

    return render_template("contact.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/", methods=['GET', 'POST'])
def visit():
    # Login Form
    post_data = request.form
    if request.method == 'POST':
        form = LoginForm(data=post_data)
        user = User.query.filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/shop/')
        else:
            return redirect('/login')
    else:
        form = LoginForm()
    # End Login Form

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("login.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/register", methods=['GET', 'POST'])
def register():
    # Register Form
    post_data = request.form
    if request.method == 'POST':
        form = RegisterForm(data=post_data)
        if form.validate_on_submit():
            if form.password.data != form.confirm_password.data:
                form.confirm_password.errors.append("Wrong password!")
                flash('Hər iki şifrə uyğun olmalıdır')
                return redirect('/wrong-confirm-password')
            else:
                user = User.query.filter(User.email == form.email.data).first()
                if user:
                    flash("Bu istifadəçi adı mövcuddur")
                    return redirect('/wrong-register')
                else:
                    user = User(form.full_name.data, form.email.data, form.password.data)
                    user.save()
                    return redirect('/login')
    else:
        form = RegisterForm()
    # End Register Form
    
    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("register.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/wrong-register", methods=['GET', 'POST'])
def wrong_register():
    # Form
    post_data = request.form
    if request.method == 'POST':
        form = RegisterForm(data=post_data)
        if form.validate_on_submit():
            if form.password.data != form.confirm_password.data:
                form.confirm_password.errors.append("Wrong password!")
                flash('Hər iki şifrə uyğun olmalıdır')
                return redirect('/wrong-confirm-password')
            else:
                user = User.query.filter(User.email == form.email.data).first()
                if user:
                    flash("Bu istifadəçi adı mövcuddur")
                    return redirect('/wrong-register')
                else:
                    user = User(form.full_name.data, form.email.data, form.password.data)
                    user.save()
                    return redirect('/login')
    else:
        form = RegisterForm()
    # End Form

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("wrong_register.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/wrong-confirm-password", methods=['GET', 'POST'])
def wrong_confirm_password():
    # Form
    post_data = request.form
    if request.method == 'POST':
        form = RegisterForm(data=post_data)
        if form.validate_on_submit():
            if form.password.data != form.confirm_password.data:
                form.confirm_password.errors.append("Wrong password!")
                flash('Hər iki şifrə uyğun olmalıdır')
                return redirect('/wrong-confirm-password')
            else:
                user = User.query.filter(User.email == form.email.data).first()
                if user:
                    flash("Bu istifadəçi adı mövcuddur")
                    return redirect('/wrong-register')
                else:
                    user = User(form.full_name.data, form.email.data, form.password.data)
                    user.save()
                    return redirect('/login')
    else:
        form = RegisterForm()
    # End Form
    
    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count
    
    return render_template("wrong-confirm-password.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/login", methods=['GET', 'POST'])
def login():
    # Login Form
    post_data = request.form
    if request.method == 'POST':
        form = LoginForm(data=post_data)
        user = User.query.filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/shop/')
        else:
            flash("İstifadəçi adı və ya şifrə düzgün daxil edilməyib")
            return redirect('/wrong-login')
    else:
        form = LoginForm()
    # End Login Form

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("login.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route("/wrong-login", methods=['GET', 'POST'])
def wrong_login():
    # Form
    post_data = request.form
    if request.method == 'POST':
        form = LoginForm(data=post_data)
        user = User.query.filter(User.email == form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect('/shop/')
        else:
            flash("İstifadəçi adı və ya şifrə düzgün daxil edilməyib")
            return redirect('/wrong-login')
    else:
        form = LoginForm()
    # End Form

    # Favorites Count
    if current_user.is_authenticated:
        favorites_count = Favorites.query.filter_by(user_id=current_user.id).count()
    else:
        favorites_count = 0
    # End Favorites Count

    return render_template("wrong_login.html", form=form, categories=categories, favorites_count=favorites_count, stocks=stocks)


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


# @app.route('/admin/user/')
# def admin_user():
#     if current_user.is_authenticated and current_user.is_superuser: #sonsuz loop-a girir

#     else:
#         return render_template('error.html')


# @app.route('/admin/')
# def admin():
#     if current_user.is_authenticated and current_user.is_superuser:
#         return redirect('/admin/user/')
#     else:
#         return render_template('error.html')


@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    print(e)
    return render_template("error.html")