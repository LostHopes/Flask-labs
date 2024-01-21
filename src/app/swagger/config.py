from flask import request
from flask_swagger_ui import get_swaggerui_blueprint

swagger = get_swaggerui_blueprint(
    base_url="/swagger",
    api_url="http://127.0.0.1:5000/api/swagger.json",
    config={
        "app_name": "Portfolio API"
    }
)