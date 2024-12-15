from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import DateTimeField, HiddenField, SelectField, StringField, PasswordField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import InventoryItem, Supplier, User

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
    
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('new_password', message='Пароли не совпадают')])
    submit = SubmitField('Изменить пароль')

class InventoryItemForm(FlaskForm):
    name = StringField('Наименование товара', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired()])
    min_level = IntegerField('Минимальный уровень запаса', validators=[DataRequired()])
    max_level = IntegerField('Максимальный уровень запаса', validators=[DataRequired()])
    supplier_id = IntegerField('ID поставщика', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')

class SupplierForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    contact_person = StringField('Контактное лицо', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Сохранить')
    
class OrderForm(FlaskForm):
    user_id = QuerySelectField('ID пользователя', query_factory=lambda: User.query.all(), allow_blank=False, get_label='email')
    order_date = DateTimeField('Дата заказа', format='%Y-%m-%d %H:%M:%S', validators=[DataRequired()])
    status = SelectField('Статус', choices=[
        ('new', 'Новый'),
        ('completed', 'Завершен'),
        ('canceled', 'Отменен')
    ], validators=[DataRequired()])
    item_id = QuerySelectField('Товар', query_factory=lambda: InventoryItem.query.all(), get_label='name', allow_blank=False)
    supplier_id = QuerySelectField('Поставщик', query_factory=lambda: Supplier.query.all(), get_label='name', allow_blank=False)
    submit = SubmitField('Добавить заказ')
    
    