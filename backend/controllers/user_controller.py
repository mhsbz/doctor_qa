from flask import Blueprint, request, jsonify
# 修正导入路径
from services.user_service import register_user, login_user, update_user_info

user_bp = Blueprint('user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    required_fields = ['username', 'password', 'gender', 'region', 'phone', 'email']
    
    # 验证必填字段
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必填字段'}), 400
    
    success, result = register_user(data)
    
    if success:
        return jsonify({
            'message': '注册成功',
            'user_id': result
        }), 201
    else:
        return jsonify({'error': result}), 400

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    required_fields = ['username', 'password']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 获取用户类型，默认为普通用户
    user_type = data.get('user_type', 'user')
    data['user_type'] = user_type
    
    success, result = login_user(data)
    
    if success:
        return jsonify({
            'message': '登录成功',
            'user_info': result,
            'user_type': result['user_type']
        }), 200
    else:
        return jsonify({'error': result}), 401

@user_bp.route('/update_profile', methods=['PUT'])
def update_profile():
    data = request.get_json()
    
    # 验证必填字段
    if 'user_id' not in data:
        return jsonify({'error': '缺少用户ID'}), 400
    
    # 可更新的字段
    updateable_fields = ['username', 'gender', 'region', 'phone', 'email']
    
    # 检查是否有至少一个可更新字段
    if not any(field in data for field in updateable_fields):
        return jsonify({'error': '没有提供任何可更新的字段'}), 400
    
    success, result = update_user_info(data)
    
    if success:
        return jsonify({
            'message': '个人信息更新成功',
            'user_info': result
        }), 200
    else:
        return jsonify({'error': result}), 400