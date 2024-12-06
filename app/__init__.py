from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.config import Config
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

csrf = CSRFProtect(app)
csrf.init_app(app)

# Инициализация админки
admin = Admin(app, name='Inventory Admin', template_mode='bootstrap3')

# Импорт моделей
from app.models import User, InventoryItem, Supplier, Order, InventoryChangeHistory

class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

# Настройка Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Добавление моделей в админку
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(InventoryItem, db.session))
admin.add_view(MyModelView(Supplier, db.session))
admin.add_view(MyModelView(Order, db.session))
admin.add_view(MyModelView(InventoryChangeHistory, db.session))

from app import views