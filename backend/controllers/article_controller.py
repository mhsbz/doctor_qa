from flask import Blueprint, jsonify, request, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from utils import allowed_file # 从 utils.py 导入辅助函数
from services.article_service import get_articles_list, increment_likes, get_article_detail, create_article, update_article, delete_article

article_bp = Blueprint('article', __name__)

@article_bp.route('/articles', methods=['GET'])
def get_articles():
    articles = get_articles_list()
    return jsonify(articles), 200

@article_bp.route('/articles', methods=['POST'])
def post_article():
    if 'title' not in request.form or 'content' not in request.form or 'user_id' not in request.form:
        return jsonify({"error": "缺少标题、内容或用户ID"}), 400

    title = request.form['title']
    content = request.form['content']
    user_id = request.form['user_id'] # 获取 user_id
    image_file = request.files.get('image')
    image_url = None

    if image_file:
        if not allowed_file(image_file.filename):
            return jsonify({"error": "无效的文件类型"}), 400
        
        try:
            filename = secure_filename(image_file.filename)
            # 生成唯一文件名防止冲突
            unique_filename = str(uuid.uuid4()) + '_' + filename
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
            image_file.save(upload_path)
            # 构造可访问的URL
            image_url = f'/uploads/images/{unique_filename}' 
        except Exception as e:
             return jsonify({"error": f"文件上传失败: {str(e)}"}), 500

    try:
        article_data = {'title': title, 'content': content, 'image_url': image_url,'user_id':user_id}
        # 将 user_id 传递给服务层函数
        new_article = create_article(article_data)
        return jsonify(new_article), 201
    except Exception as e:
        # 如果数据库操作失败，可能需要考虑删除已上传的文件
        if image_url and os.path.exists(upload_path):
             try:
                 os.remove(upload_path)
             except OSError as oe:
                 print(f"Error deleting file {upload_path}: {oe}") # 记录删除失败日志
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
    # 注意：此版本仅处理 JSON 数据更新，未包含图片更新逻辑
    # 如果需要支持更新时上传图片，需要类似 post_article 的逻辑处理 request.files 和 request.form
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
