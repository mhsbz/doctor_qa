from flask import Blueprint, request, jsonify
from models.user_like import UserLike
from models.article import Article
from models.db import db
from datetime import datetime

like_bp = Blueprint('like', __name__)

@like_bp.route('/user/<int:user_id>/likes', methods=['GET'])
def get_user_likes(user_id):
    """
    获取用户点赞的文章列表
    """
    try:
        # 查询用户点赞记录
        user_likes = UserLike.query.filter_by(user_id=user_id).all()
        
        if not user_likes:
            return jsonify([]), 200
        
        # 获取文章ID列表
        article_ids = [like.article_id for like in user_likes]
        
        # 查询文章详情
        articles = Article.query.filter(Article.id.in_(article_ids)).all()
        
        # 创建文章ID到点赞时间的映射
        like_dates = {like.article_id: like.created_at for like in user_likes}
        
        # 构建响应数据
        result = []
        for article in articles:
            result.append({
                'id': article.id,
                'title': article.title,
                'content': article.content,
                'image_url': article.image_url,
                'likes': article.likes,
                'like_date': like_dates[article.id].isoformat() if article.id in like_dates else None
            })
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@like_bp.route('/articles/<int:article_id>/like_status', methods=['GET'])
def check_like_status(article_id):
    """
    检查用户是否点赞文章
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({'error': '缺少用户ID'}), 400
        
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        existing_like = UserLike.query.filter_by(
            user_id=user_id,
            article_id=article_id
        ).first()
        
        return jsonify({'has_liked': existing_like is not None}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@like_bp.route('/articles/<int:article_id>/like', methods=['POST'])
def like_article(article_id):
    """
    用户点赞文章
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': '缺少用户ID'}), 400
        
        # 检查文章是否存在
        article = Article.query.get(article_id)
        if not article:
            return jsonify({'error': '文章不存在'}), 404
        
        # 检查是否已经点赞
        existing_like = UserLike.query.filter_by(
            user_id=user_id,
            article_id=article_id
        ).first()
        
        if existing_like:
            return jsonify({
                'message': '已经点赞过该文章',
                'likes': article.likes
            }), 200
        
        # 创建点赞记录
        new_like = UserLike(
            user_id=user_id,
            article_id=article_id,
            created_at=datetime.utcnow()
        )
        
        # 更新文章点赞数
        article.likes += 1
        
        # 保存到数据库
        db.session.add(new_like)
        db.session.commit()
        
        return jsonify({
            'message': '点赞成功',
            'likes': article.likes
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500