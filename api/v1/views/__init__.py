from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
app_views_states = Blueprint('app_views_states', __name__,
                             url_prefix="/api/v1")
app_views_cities = Blueprint('app_views_cities', __name__,
                             url_prefix="/api/v1")
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
