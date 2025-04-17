from models.feedback import Feedback, db
from models.user import User
from sqlalchemy import func

def create_feedback(feedback_data):
    """
    创建新的用户反馈
    :param feedback_data: 包含反馈信息的字典
    :return: 创建的反馈对象或错误信息
    """
    # 验证用户是否存在
    user_id = feedback_data.get('user_id')
    if user_id and not User.query.get(user_id):
        raise ValueError('用户不存在')
    
    # 验证反馈类型
    valid_types = ['UI设计', '系统性能', '回答效果', '其他']
    if feedback_data.get('feedback_type') not in valid_types:
        raise ValueError('无效的反馈类型')
    
    try:
        new_feedback = Feedback(
            user_id=user_id,
            feedback_type=feedback_data.get('feedback_type'),
            description=feedback_data.get('description')
        )
        db.session.add(new_feedback)
        db.session.commit()
        return new_feedback
    except Exception as e:
        db.session.rollback()
        raise e

def get_feedback_statistics():
    """
    获取反馈类型的统计数据，用于生成饼状图
    :return: 包含各类型反馈数量和比例的列表
    """
    try:
        # 查询各类型反馈的数量
        result = db.session.query(
            Feedback.feedback_type,
            func.count(Feedback.id).label('count')
        ).group_by(Feedback.feedback_type).all()
        
        # 计算总数
        total = sum(item.count for item in result)
        
        # 格式化结果，添加百分比
        statistics = []
        for item in result:
            statistics.append({
                'type': item.feedback_type,
                'count': item.count,
                'percentage': round(item.count / total * 100, 2) if total > 0 else 0
            })
        
        return statistics
    except Exception as e:
        raise e

def get_feedbacks_by_type(feedback_type=None):
    """
    根据反馈类型获取反馈列表
    :param feedback_type: 反馈类型，如果为None则返回所有反馈
    :return: 反馈列表
    """
    try:
        query = Feedback.query
        
        # 如果指定了反馈类型，则进行筛选
        if feedback_type:
            # 验证反馈类型
            valid_types = ['UI设计', '系统性能', '回答效果', '其他']
            if feedback_type not in valid_types:
                raise ValueError('无效的反馈类型')
            query = query.filter(Feedback.feedback_type == feedback_type)
        
        # 按创建时间降序排序
        feedbacks = query.order_by(Feedback.created_at.desc()).all()
        
        # 序列化结果
        return [
            {
                'id': f.id,
                'user_id': f.user_id,
                'feedback_type': f.feedback_type,
                'description': f.description,
                'created_at': f.created_at.isoformat()
            }
            for f in feedbacks
        ]
    except Exception as e:
        raise e