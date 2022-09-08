import os
from flask import render_template, redirect, url_for, request, flash
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from sweater import defs, user_datastore
from sweater.settings import db, app, manager
from sweater.models import Items, User, Role
from sweater.defs import resize_image, img_check


@app.route('/')
def index():
    items = Items.query.order_by(Items.price).all()
    return render_template('index.html', data=items)


@app.route('/admin')
@login_required
def admin():
    if current_user.admin == "admin":
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/ad_<int:id>')
def check_ad(id):
    items = Items.query.get(id)
    items.views += 1
    db.session.commit()
    return render_template('ad.html', data=items)


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    email = request.form.get('email')
    password = request.form.get('password')

    if email and password:
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неверная почта или пароль')

    else:
        flash('Введите почту или пароль')
    return render_template('security/login_user.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    phone = request.form.get('phone')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    name = request.form.get('name')
    surname = request.form.get('surname')
    email = request.form.get('email')

    if request.method == 'POST':
        if not (email or password or password2):
            flash('Заполните все поля')
        elif password != password2:
            flash('Пароли не совпадают')
        elif User.query.filter(User.email == email).all():
            flash('Такой пользователь уже существует')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(password=hash_pwd, name=name,
                            surname=surname, email=email, phone=phone)
            role = Role.query.get(2)
            user_datastore.add_role_to_user(new_user, role)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if not current_user.has_role('admin'):
        return redirect(url_for('index'))
    if request.method == "POST":
        adType = request.form['adType']
        roomType = request.form['roomType']
        title = request.form['title']
        description = request.form['description']
        city = request.form['city']
        street = request.form['street']
        houseNumber = request.form['houseNumber']
        adUser = request.form['adUser']
        adEmail = request.form['adEmail']
        adPhone = request.form['adPhone']
        price = request.form['price']
        numberOfStoreys = request.form['numberOfStoreys']
        wallMaterial = request.form['wallMaterial']
        yearOfConstruction = request.form['yearOfConstruction']
        yearOfOverhaul = request.form['yearOfOverhaul']
        totalArea = request.form['totalArea']
        livingArea = request.form['livingArea']
        kitchen = request.form['kitchen']
        rooms = request.form['rooms']
        separate_rooms = request.form['separate_rooms']
        floor = request.form['floor']
        bathroom = request.form['bathroom']
        balcony = request.form['balcony']
        repair = request.form['repair']
        files = ""


        try:
            title_file = request.files['title_file']
            file = request.files.getlist('files')
            for el in file:
                filename = secure_filename(el.filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(item.id) + "/", filename))
                files += filename + ","
            files = title_file.filename + "," + files
        except:
            return "Ошибка добавления названия картинок"

        item = Items(adType=adType, roomType=roomType,
                     title=title, description=description, city=city, street=street,
                     houseNumber=houseNumber, adUser=adUser,
                     adEmail=adEmail, adPhone=adPhone, price=price, numberOfStoreys=numberOfStoreys,
                     yearOfConstruction=yearOfConstruction, yearOfOverhaul=yearOfOverhaul, totalArea=totalArea,
                     livingArea=livingArea,
                     kitchen=kitchen, rooms=rooms, separate_rooms=separate_rooms, floor=floor,
                     wallMaterial=wallMaterial, bathroom=bathroom, balcony=balcony, repair=repair, files=files[:-1])
        try:
            db.session.add(item)
            db.session.commit()
            os.mkdir(app.config['UPLOAD_FOLDER'] + "/" + str(item.id))
            filename = secure_filename(title_file.filename)
            image_path = (app.config['UPLOAD_FOLDER'] + "/" + str(item.id) + "/" + filename)
            title_file.save(image_path)
            resize_image(image_path, image_path, (1536, 1024))
            for el in file:
                # os.path.join()
                filename = secure_filename(el.filename)
                image_path = (app.config['UPLOAD_FOLDER'] + "/" + str(item.id) + "/" + filename)
                # file.save(os.path.join(app.config['UPLOAD_FOLDER'] + "/" + str(item.id) + "/", filename))
                el.save(image_path)
                resize_image(image_path, image_path, (1536, 1024))
            img_check()
            return redirect('/')
        except:
            return "Ошибка создания объявления"
    else:
        return render_template('create.html')
