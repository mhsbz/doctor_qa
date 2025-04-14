from flask import Blueprint, request, jsonify
from services.comment_service import create_comment, get_comments_by_article

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