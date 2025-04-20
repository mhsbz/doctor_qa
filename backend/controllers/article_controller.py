from flask import Blueprint, jsonify, request
from services.article_service import get_articles_list, increment_likes, get_article_detail, create_article, update_article, delete_article

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = get_articles_list()
    return jsonify(articles), 200

@article_bp.route('/articles', methods=['POST'])
def post_article():
    data = request.get_json()
    if not data or 'title' not in data or 'content' not in data:
        return jsonify({"error": "缺少标题或内容"}), 400
    try:
        new_article = create_article(data)
        return jsonify(new_article), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@article_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        article = get_article_detail(article_id)
        return jsonify(article), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@article_bp.route('/articles/<int:article_id>', methods=['PUT'])
def put_article(article_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "缺少请求体"}), 400
    try:
        updated_article = update_article(article_id, data)
        return jsonify(updated_article), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@article_bp.route('/articles/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    try:
        updated_likes = increment_likes(article_id)
        return jsonify({
            "message": "点赞成功",
            "likes": updated_likes
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
@article_bp.route('/articles/<int:article_id>', methods=['DELETE'])
def remove_article(article_id):
    try:
        delete_article(article_id)
        return jsonify({"message": "文章删除成功"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
