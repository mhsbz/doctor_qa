from flask import Blueprint, jsonify, request
from services.article_service import get_articles_list, increment_likes, get_article_detail

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = get_articles_list()
    return jsonify(articles), 200

@article_bp.route('/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    try:
        article = get_article_detail(article_id)
        return jsonify(article), 200
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