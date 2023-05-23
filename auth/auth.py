#!/usr/bin/python3
"""
a simple Flask Blueprint for authentication
"""

from flask import Blueprint, render_template
from EcoExchange.models import auth


@auth_bp = Blueprint('auth_bp', __name__,
                     template_folder='templates'
                     static_folder='static', static_url_path='assets')
