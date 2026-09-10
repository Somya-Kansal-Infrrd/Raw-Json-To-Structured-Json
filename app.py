"""Application entry point."""

from flask import Flask

from controllers.conversion_controller import conversion_controller


def create_app() -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(conversion_controller)
    return app


app = create_app()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )