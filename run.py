from app import app, db
from app.models import User, InventoryItem, Supplier, Order, InventoryChangeHistory
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

def seed_database():
    # Удаляем существующие записи
    db.drop_all()
    db.create_all()

    # Создаем пользователей
    users = [
        User(first_name='Иван', last_name='Иванов', email='ivan@example.com', password=generate_password_hash('password1'), role='admin'),
        User(first_name='Петр', last_name='Петров', email='petr@example.com', password=generate_password_hash('password2'), role='moderator'),
        User(first_name='Сидор', last_name='Сидоров', email='sidor@example.com', password=generate_password_hash('password3'), role='client'),
        User(first_name='Анна', last_name='Антонова', email='anna@example.com', password=generate_password_hash('password4'), role='client'),
        User(first_name='Мария', last_name='Маркова', email='maria@example.com', password=generate_password_hash('password5'), role='client'),
        User(first_name='Елена', last_name='Еленина', email='elena@example.com', password=generate_password_hash('password6'), role='client'),
        User(first_name='Алексей', last_name='Алексеев', email='aleksey@example.com', password=generate_password_hash('password7'), role='client')
    ]

    # Добавляем пользователей в базу данных
    db.session.bulk_save_objects(users)

    # Создаем поставщиков
    suppliers = [
        Supplier(name='Поставщик 1', contact_person='Иван Иванович', phone='+7 (123) 456-78-90', email='supplier1@example.com'),
        Supplier(name='Поставщик 2', contact_person='Петр Петрович', phone='+7 (123) 456-78-91', email='supplier2@example.com'),
        Supplier(name='Поставщик 3', contact_person='Сидор Сидорович', phone='+7 (123) 456-78-92', email='supplier3@example.com'),
        Supplier(name='Поставщик 4', contact_person='Анна Антоновна', phone='+7 (123) 456-78-93', email='supplier4@example.com'),
        Supplier(name='Поставщик 5', contact_person='Мария Марковна', phone='+7 (123) 456-78-94', email='supplier5@example.com'),
        Supplier(name='Поставщик 6', contact_person='Елена Еленина', phone='+7 (123) 456-78-95', email='supplier6@example.com'),
        Supplier(name='Поставщик 7', contact_person='Алексей Алексеевич', phone='+7 (123) 456-78-96', email='supplier7@example.com')
    ]

    # Добавляем поставщиков в базу данных
    db.session.bulk_save_objects(suppliers)

    # Создаем товары
    items = [
        InventoryItem(name='Товар 1', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 2', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 3', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 4', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 5', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 6', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 7', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 8', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 9', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers))),
        InventoryItem(name='Товар 10', quantity=random.randint(10, 100), min_level=random.randint(1, 10), max_level=random.randint(50, 200), supplier_id=random.randint(1, len(suppliers)))
    ]

    # Добавляем товары в базу данных
    db.session.bulk_save_objects(items)

    # Создаем заказы
    orders = [
        Order(user_id=users[i % len(users)].id,
              order_date=datetime.now(),
              status=['new','completed','canceled'][random.choice(range(3))]) for i in range(len(items))
    ]

    # Добавляем заказы в базу данных
    db.session.bulk_save_objects(orders)

    # Создаем историю изменений запасов
    history = [
        InventoryChangeHistory(item_id=item.id,
                                change_date=datetime.now(),
                                changed_quantity=random.choice([-5, -3]), # Пример уменьшения запасов
                                reason="Регулярная проверка запасов") for item in items
    ]

    # Добавляем историю изменений в базу данных
    db.session.bulk_save_objects(history)

    # Сохраняем все изменения в базе данных
    db.session.commit()

if __name__ == '__main__':
    # with app.app_context():
    #     seed_database()
    #     db.create_all()  # Создание всех таблиц
    app.run(debug=True)