from flask_wtf import FlaskForm
from wtforms import DateTimeField, HiddenField, SelectField, StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class InventoryItemForm(FlaskForm):
    name = StringField('Наименование товара', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    min_level = IntegerField('Минимальный уровень запаса', validators=[DataRequired()])
    max_level = IntegerField('Максимальный уровень запаса', validators=[DataRequired()])
    supplier_id = IntegerField('ID поставщика', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')

class SupplierForm(FlaskForm):
    name = StringField('Наименование поставщика', validators=[DataRequired()])
    contact_person = StringField('Контактное лицо')
    phone = StringField('Телефон')
    email = StringField('Email', validators=[Email()])
    submit = SubmitField('Добавить поставщика')
    
class OrderForm(FlaskForm):
    user_id = HiddenField('ID пользователя', validators=[DataRequired()])
    order_date = DateTimeField('Дата заказа', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    status = SelectField('Статус', choices=[
        ('new', 'Новый'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен')
    ], validators=[DataRequired()])
    submit = SubmitField('Добавить заказ')