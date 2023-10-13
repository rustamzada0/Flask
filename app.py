from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:123@127.0.0.1:3330/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = 'my_project'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

from controllers import *
from extensions import *
from models import *

if __name__ == '__main__':
    app.init_app(db)
    app.init_app(migrate)
    app.run(port=5000, debug=True)

admin = Admin(app, name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Reviews, db.session))
admin.add_view(ModelView(Favorites, db.session))
admin.add_view(ModelView(Detail, db.session))
# admin.add_view(Controller(User, db.session))