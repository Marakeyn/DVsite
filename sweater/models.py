from flask_security import UserMixin, RoleMixin
from sweater.settings import db, manager
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


class Items(db.Model):
    # Общая информация
    # __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, nullable=True)  # id Объявления
    created = db.Column(db.DateTime, default=datetime.now())
    adType = db.Column(db.String(100), nullable=False)  # Тип (Аренда или Продажа)
    roomType = db.Column(db.String(100), nullable=False)  # Тип Помещения/Здания
    title = db.Column(db.String(100), nullable=False)  # Титул
    description = db.Column(db.Text(999), nullable=False)  # Описание
    city = db.Column(db.String, nullable=False)  # Город
    street = db.Column(db.String, nullable=False)  # Улица
    houseNumber = db.Column(db.String, nullable=False)  # Номер дома
    # status = db.Column(db.String, nullable=False, default="moderation")  # Статус объявления (active / moderation /
    # inactively)
    isActive = db.Column(db.Boolean, default=True)  # Активность объявления (True / False)
    adUser = db.Column(db.String, nullable=False)  # контактное лицо
    adEmail = db.Column(db.String, nullable=False)  # почта лица
    adPhone = db.Column(db.String, nullable=False)  # телефон лица
    price = db.Column(db.Integer, nullable=False)  # цена
    views = db.Column(db.Integer, default=0)  # просмотры

    # Информация о доме

    numberOfStoreys = db.Column(db.Integer, nullable=True)  # Этажность
    wallMaterial = db.Column(db.String, nullable=True)  # Материалы стен
    yearOfConstruction = db.Column(db.Integer, nullable=True)  # Год постройки дома
    yearOfOverhaul = db.Column(db.Integer, nullable=True)  # год капитального ремонта
    # Информация о квартире

    totalArea = db.Column(db.Float, nullable=False)  # Общая площадь
    livingArea = db.Column(db.Float, nullable=False)  # Жилая площадь
    kitchen = db.Column(db.Float, nullable=False)  # Кухня
    rooms = db.Column(db.Integer, nullable=False)  # Кол-во Комнат
    separate_rooms = db.Column(db.Integer, nullable=False)  # Комнат раздельных
    floor = db.Column(db.Integer, nullable=False)  # Этаж
    bathroom = db.Column(db.String, nullable=True)  # Санузел
    balcony = db.Column(db.String, nullable=True)  # Балкон
    # termsOfSale = db.Column(db.String, nullable=False)                   # Условия продажи
    repair = db.Column(db.String, nullable=True)  # ремонт
    files = db.Column(db.String, nullable=True)  # имя картинок

    def __repr__(self):
        return f'{self.title}'


##ADMIN##

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
                       )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(32), nullable=False)
    active = db.Column(db.Boolean())
    password = db.Column(db.String(255), nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(100))
