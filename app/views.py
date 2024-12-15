from flask import abort, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from app import app, db
from app.forms import ChangePasswordForm, OrderForm, RegistrationForm, LoginForm, InventoryItemForm, SupplierForm
from app.models import InventoryItem, Supplier, User, Order, InventoryChangeHistory

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        # Данные для авторизованных пользователей
        total_orders = Order.query.filter_by(user_id=current_user.id).count()
        total_suppliers = Supplier.query.count()
        
        # Получаем данные для графиков
        orders_data = Order.query.with_entities(Order.order_date, Order.status).filter_by(user_id=current_user.id).all()
        
        # Преобразуем данные о заказах в стандартный формат (список кортежей)
        orders_data_list = [(order.order_date.strftime('%Y-%m-%d'), order.status) for order in orders_data]
        
        return render_template('index.html', 
                               total_orders=total_orders, 
                               total_suppliers=total_suppliers,
                               orders_data=orders_data_list,
                               is_authenticated=True)
    else:
        # Фейковые данные для неавторизованных пользователей
        fake_orders_data = [
            ('2024-01-01', 'new'),
            ('2024-01-02', 'completed'),
            ('2024-01-03', 'canceled'),
            ('2024-01-04', 'new'),
            ('2024-01-05', 'completed'),
            ('2024-01-06', 'completed'),
            ('2024-01-07', 'new')
        ]
        
        return render_template('index.html', 
                               orders_data=fake_orders_data,
                               is_authenticated=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)  # Хешируем пароль
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверный email или пароль.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из аккаунта.', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Неверный текущий пароль.', 'danger')
            return redirect(url_for('profile'))
        
        if form.new_password.data != form.confirm_password.data:
            flash('Новый пароль и подтверждение не совпадают.', 'danger')
            return redirect(url_for('profile'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Пароль успешно изменен.', 'success')
        return redirect(url_for('profile'))

    # Получаем статистику по заказам
    total_orders = Order.query.filter_by(user_id=current_user.id).count()
    total_suppliers = Supplier.query.count()
    
    # Получаем данные для графиков
    orders_data = Order.query.with_entities(Order.order_date, Order.status).filter_by(user_id=current_user.id).all()
    
    # Преобразуем данные о заказах в стандартный формат (список кортежей)
    orders_data_list = [(order.order_date.strftime('%Y-%m-%d'), order.status) for order in orders_data]
    
    # Получаем данные о поставках
    supplier_counts = {supplier.name: 0 for supplier in Supplier.query.all()}
    
    for item in InventoryItem.query.all():
        supplier_name = Supplier.query.get(item.supplier_id).name
        supplier_counts[supplier_name] += item.quantity

    return render_template('profile.html', 
                           user=current_user, 
                           total_orders=total_orders, 
                           total_suppliers=total_suppliers,
                           orders_data=orders_data_list,
                           supplier_counts=supplier_counts,
                           form=form)  # Передаем форму в шаблон

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    inventory_form = InventoryItemForm()
    supplier_form = SupplierForm()
    
    if inventory_form.validate_on_submit():
        item = InventoryItem(
            name=inventory_form.name.data,
            quantity=inventory_form.quantity.data,
            min_level=inventory_form.min_level.data,
            max_level=inventory_form.max_level.data,
            supplier_id=inventory_form.supplier_id.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Товар добавлен!', 'success')
    
    if supplier_form.validate_on_submit():
        supplier = Supplier(
            name=supplier_form.name.data,
            contact_person=supplier_form.contact_person.data,
            phone=supplier_form.phone.data,
            email=supplier_form.email.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Поставщик добавлен!', 'success')

    return render_template('admin.html', inventory_form=inventory_form, supplier_form=supplier_form)

# Маршрут для отображения всех товаров
@app.route('/inventory')
@login_required
def inventory():
    items = InventoryItem.query.all()
    return render_template('inventory.html', items=items)

# Маршрут для добавления нового товара
@app.route('/inventory/new', methods=['GET', 'POST'])
@login_required
def new_inventory_item():
    form = InventoryItemForm()
    if form.validate_on_submit():
        item = InventoryItem(
            name=form.name.data,
            quantity=form.quantity.data,
            min_level=form.min_level.data,
            max_level=form.max_level.data,
            supplier_id=form.supplier_id.data
        )
        db.session.add(item)
        db.session.commit()
        flash('Товар добавлен!', 'success')
        return redirect(url_for('inventory'))
    return render_template('new_inventory_item.html', form=form)



# Маршрут для отображения всех поставщиков
@app.route('/suppliers')
@login_required
def suppliers():
    form = SupplierForm()
    suppliers = Supplier.query.all()
    return render_template('suppliers.html', suppliers=suppliers, form=form)

# Маршрут для добавления нового поставщика
@app.route('/suppliers/new', methods=['GET', 'POST'])
@login_required
def new_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            contact_person=form.contact_person.data,
            phone=form.phone.data,
            email=form.email.data
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Поставщик добавлен!', 'success')
        return redirect(url_for('suppliers'))
    return render_template('new_supplier.html', form=form)

# Маршрут для отображения всех заказов
@app.route('/orders')
@login_required
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

# Маршрут для добавления нового заказа (можно расширить)
@app.route('/orders/new', methods=['GET', 'POST'])
@login_required
def new_order():
    form = OrderForm()
    if form.validate_on_submit():
        order_date = request.form.get('order_date')  # Получаем значение из поля даты
        order = Order(
            user_id=form.user_id.data,
            order_date=order_date,
            status=form.status.data,
            item_id=form.item_id.data.id,  # Получаем ID выбранного товара
            supplier_id=form.supplier_id.data.id  # Получаем ID выбранного поставщика
        )
        db.session.add(order)
        db.session.commit()
        flash('Заказ добавлен!', 'success')
        return redirect(url_for('orders'))
    return render_template('new_order.html', form=form)

@app.route('/orders/edit/<int:order_id>', methods=['GET', 'POST'])
@login_required
def edit_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm(obj=order)
    
    if form.validate_on_submit():
        order.user_id = form.user_id.data
        order.order_date = form.order_date.data
        order.status = form.status.data
        order.supplier_id = form.supplier_id.data
        order.item_id = form.item_id.data
        db.session.commit()
        flash('Заказ обновлен!', 'success')
        return redirect(url_for('orders'))
    
    return render_template('edit_order.html', form=form, order=order)

# Маршрут для отображения истории изменений запасов
@app.route('/inventory/history')
@login_required
def inventory_history():
    history = InventoryChangeHistory.query.all()
    return render_template('inventory_history.html', history=history)

@app.route('/inventory/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_inventory_item(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    form = InventoryItemForm(obj=item)
    
    if form.validate_on_submit():
        # Сохраняем старое количество для записи в историю
        old_quantity = item.quantity
        
        item.name = form.name.data
        item.min_level = form.min_level.data
        item.max_level = form.max_level.data
        
        # Обновляем количество и записываем изменение в историю
        new_quantity = form.quantity.data
        change_quantity = new_quantity - old_quantity
        if change_quantity > 0:
            item.update_quantity(change_quantity, "Обновление товара")
        elif change_quantity < 0:
            item.update_quantity(change_quantity, "Регулярная проверка запасов")
            
        
        db.session.commit()
        flash('Товар обновлен!', 'success')
        return redirect(url_for('inventory'))
    
    return render_template('edit_inventory_item.html', form=form, item=item)

@app.route('/statistics')
@login_required
def statistics():
    # Получаем данные для графиков
    orders_data = Order.query.with_entities(Order.order_date, Order.status).filter_by(user_id=current_user.id).all()
    
    # Преобразуем данные о заказах в стандартный формат
    orders_data_list = [(order.order_date.strftime('%Y-%m-%d'), order.status) for order in orders_data]
    
    # Получаем данные о поставках
    supplier_counts = {supplier.name: 0 for supplier in Supplier.query.all()}
    
    for item in InventoryItem.query.all():
        supplier_name = Supplier.query.get(item.supplier_id).name
        supplier_counts[supplier_name] += item.quantity

    return render_template('statistics.html', orders_data=orders_data_list, supplier_counts=supplier_counts)

@app.errorhandler(400)
def bad_request(error):
    return render_template('error_400.html'), 400

@app.errorhandler(500)
def internal_error(error):
    return render_template('error_500.html'), 500

@app.route('/test_bad_request')
def test_bad_request():
    abort(400)
    
@app.route('/test_internal_error')
def test_internal_error():
    raise Exception("Это тестовая ошибка 500")  # Принудительно вызываем ошибку 500


@app.route('/suppliers/edit/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm(obj=supplier)  # Предполагается, что у вас есть форма SupplierForm

    if form.validate_on_submit():
        supplier.name = form.name.data
        supplier.contact_person = form.contact_person.data
        supplier.phone = form.phone.data
        supplier.email = form.email.data
        db.session.commit()
        flash('Поставщик обновлен!', 'success')
        return redirect(url_for('suppliers'))

    return render_template('edit_supplier.html', form=form, supplier=supplier)

@app.route('/suppliers/delete/<int:supplier_id>', methods=['POST'])
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    db.session.delete(supplier)
    db.session.commit()
    flash('Поставщик удален!', 'success')
    return redirect(url_for('suppliers'))