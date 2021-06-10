from flask import Blueprint, render_template

blueprint = Blueprint("blueprint",__name__, static_folder="static", template_folder="templates")

@blueprint.route('/')
def home():
    return render_template('index.html')

@blueprint.route('/test')
def test():
    return "Test"