import os
import shutil
from os.path import join, dirname, realpath
from PIL import Image
from sweater import app
from sweater.models import Items
from werkzeug.utils import secure_filename


def resize_image(input_image_path,
                 output_image_path,
                 size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize(size)
    resized_image.save(output_image_path)


def img_check():
    items = Items.query.all()
    for el in items:
        for i in el.files.split(','):
            if os.path.exists(app.config['UPLOAD_FOLDER'] + "/" + str(el.id) + "/" + i):
                continue
            else:
                shutil.copyfile(app.config['UPLOAD_FOLDER'] + "/default.png", UPLOAD_FOLDER + "/" + str(el.id) + "/" + i)
