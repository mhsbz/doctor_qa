from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import os
from dotenv import load_dotenv
import sys
from pathlib import Path

# 将当前目录添加到Python路径中，解决导入问题
sys.path.append(str(Path(__file__).parent))

# 从models中导入db实例
from models.user import db

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root:password@localhost/doctor_qa')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

print(app.config)
# 初始化数据库
db.init_app(app)
migrate = Migrate(app, db)

# 注册蓝图
from controllers.user_controller import user_bp
app.register_blueprint(user_bp, url_prefix='/api')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 确保数据库表已创建
    app.run(debug=True)