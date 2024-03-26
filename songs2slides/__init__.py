from flask import Flask, render_template

def error_404(e):
    return render_template('error.html', message='404 Not Found'), 404

def create_app():
    app = Flask(__name__)

    from . import routes
    app.register_blueprint(routes.bp)
    app.register_error_handler(404, error_404)

    return app
