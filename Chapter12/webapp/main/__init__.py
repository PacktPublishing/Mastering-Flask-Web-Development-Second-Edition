
def create_module(app, **kwargs):
    from .controllers import main_blueprint
    app.register_blueprint(main_blueprint)
