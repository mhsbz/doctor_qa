from models.user import User, db

def login_user(login_data):
    """
    用户登录
    :param login_data: 包含用户名和密码的字典
    :return: (success, result) success为布尔值，result为成功时的用户信息或失败时的错误信息
    """
    user = User.query.filter_by(username=login_data['username']).first()
    if not user or user.password != login_data['password']:
        return False, '用户名或密码错误'
    return True, {'user_id': user.id, 'username': user.username, 'user_type': user.user_type}

def register_user(user_data):
    """
    注册新用户
    :param user_data: 包含用户信息的字典
    :return: (success, result) success为布尔值，result为成功时的用户ID或失败时的错误信息
    """
    # 检查用户名是否已存在
    if User.query.filter_by(username=user_data['username']).first():
        return False, '用户名已存在'
    
    try:
        new_user = User(
            username=user_data['username'],
            password=user_data['password'],  # 实际项目中密码应该加密
            gender=user_data.get('gender'),
            region=user_data.get('region'),
            phone=user_data.get('phone'),
            email=user_data.get('email')
        )
        db.session.add(new_user)
        db.session.commit()
        return True, new_user.id
    except Exception as e:
        db.session.rollback()
        return False, str(e)