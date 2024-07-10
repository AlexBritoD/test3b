from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
scheduler = APScheduler()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    
    if not app.config.get('TESTING'):
        scheduler.init_app(app)
        scheduler.start()

    from .routes import main
    app.register_blueprint(main)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test 3B"
        }
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()
        
        from .jobs import check_stock
        if not scheduler.get_job('check_stock'):
            scheduler.add_job(id='check_stock', func=check_stock, trigger='interval', seconds=10)

    return app
