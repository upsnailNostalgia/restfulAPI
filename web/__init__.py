from flask import Blueprint

web = Blueprint('web', __name__)

from restfulAPI.web import code_views
from restfulAPI.web import commit_views
from restfulAPI.web import error_views
from restfulAPI.web import repository_views