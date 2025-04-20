from flask import Blueprint, request, jsonify
from services.comment_service import create_comment, get_comments_by_article, update_comment, delete_comment
from models.user import User

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/articles/<int:article_id>/comments', methods=['GET'])
def get_comments(article_id):
    try:
        comments = get_comments_by_article(article_id)
        return jsonify({"comments": comments}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@comment_bp.route('/comments', methods=['POST'])
def handle_create_comment():
    data = request.get_json()
    print(data)
    try:
        result = create_comment(data)
        return jsonify({
            'message': '评论创建成功',
            'comment_id': result.id
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': '服务器内部错误'}), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['PUT'])
def handle_update_comment(comment_id):
    data = request.get_json()
    data['comment_id'] = comment_id
    
    # 验证用户身份
    if 'user_id' not in data:
        return jsonify({'error': '缺少用户ID'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    try:
        result = update_comment(data, user)
        return jsonify({
            'message': '评论更新成功',
            'comment': {
                'id': result.id,
                'content': result.content,
            }
        }), 200
    except ValueError as e:
        print(e)
        return jsonify({'error': '无效请求参数'}), 400
    except Exception as e:
        print(e)
        return jsonify({'error': '服务器内部错误'}), 500


@comment_bp.route('/comments/<int:comment_id>', methods=['DELETE'])
def handle_delete_comment(comment_id):
    # data = request.get_json()
    
    try:
        delete_comment(comment_id)
        return jsonify({
            'message': '评论删除成功',
            'comment_id': comment_id
        }), 200
    except Exception as e:
        print(e)
        return jsonify({'error': '服务器内部错误'}), 500