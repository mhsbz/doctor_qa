from flask import Blueprint, jsonify
from services.article_service import get_articles_list

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = get_articles_list()
    return jsonify(articles), 200