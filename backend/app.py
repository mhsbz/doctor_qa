from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
import os
from pathlib import Path
import uuid
from werkzeug.utils import secure_filename

# 将当前目录添加到Python路径中，解决导入问题
sys.path.append(str(Path(__file__).parent))

# 从models中导入db实例
from models.db import db

# 加载环境变量
load_dotenv()

app = Flask(__name__)

# 配置上传文件
UPLOAD_FOLDER = os.path.join(Path(__file__).parent, 'uploads', 'images')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB Max Size

# 确保上传目录存在
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# 从 utils 导入文件检查函数
from utils import allowed_file
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:password@localhost/doctor_qa')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 配置CORS，允许所有来源、方法和头部
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": "*"
    }
})

print(app.config)
# 初始化数据库
db.init_app(app)
migrate = Migrate(app, db)

# 注册蓝图
from controllers.user_controller import user_bp
from controllers.article_controller import article_bp
from controllers.comment_controller import comment_bp
from controllers.feedback_controller import feedback_bp
from controllers.chat_controller import chat_bp
from controllers.like_controller import like_bp

app.register_blueprint(like_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(article_bp, url_prefix='/api')
app.register_blueprint(comment_bp, url_prefix='/api')
app.register_blueprint(feedback_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# 添加静态文件服务路由
@app.route('/uploads/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保数据库表已创建
    app.run(debug=True)