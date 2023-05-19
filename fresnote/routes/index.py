from flask import Blueprint, render_template, flash
import markdown
from app_classes.notebookclass import Notebook
import configparser

index = Blueprint('index', __name__)

@index.route('/')
def index_func():
    config = configparser.ConfigParser()
    config.read('config.ini')
    notebooks = config.sections()

    return render_template('index.html', data={'notebooks': notebooks}, createNotebook=False)


