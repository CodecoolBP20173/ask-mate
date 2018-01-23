from flask import Blueprint, render_template, request, redirect, url_for
import data_manager, utility
from datetime import datetime

login = Blueprint('login', __name__, template_folder='templates')

