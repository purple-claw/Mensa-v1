from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from routes.auth_routes import auth_bp
from routes.file_routes import file_bp
from routes.b2_routes import b2_routes
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(file_bp, url_prefix="/files")
app.register_blueprint(b2_routes)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "Message": "Backend is Running!",
        "API": Config.API_URL,
        "debug_mode": True
    })

if __name__ == "__main__":
    app.run(debug=True)