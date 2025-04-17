from flask import Blueprint, request, jsonify
from services.feedback_service import create_feedback, get_feedback_statistics, get_feedbacks_by_type

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()
    required_fields = ['user_id', 'feedback_type', 'description']
    
    # 验证必填字段
    if not all(field in data for field in required_fields):
        return jsonify({'error': '缺少必填字段'}), 400
    
    try:
        feedback = create_feedback(data)
        return jsonify({
            'message': '反馈提交成功',
            'feedback_id': feedback.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '服务器内部错误'}), 500

@feedback_bp.route('/feedback/statistics', methods=['GET'])
def get_feedback_stats():
    """获取反馈类型统计数据，用于生成饼状图"""
    try:
        statistics = get_feedback_statistics()
        return jsonify({
            'statistics': statistics
        }), 200
    except Exception as e:
        return jsonify({'error': '服务器内部错误'}), 500

@feedback_bp.route('/feedback/list', methods=['GET'])
def get_feedback_list():
    """获取反馈列表，可按类型筛选"""
    feedback_type = request.args.get('feedback_type')
    try:
        feedbacks = get_feedbacks_by_type(feedback_type)
        return jsonify({
            'feedbacks': feedbacks
        }), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '服务器内部错误'}), 500