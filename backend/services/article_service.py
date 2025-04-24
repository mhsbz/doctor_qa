from models.article import Article, db
from services.comment_service import get_comments_by_article
from datetime import datetime
from models.user import User

def get_articles_list():
    """
    获取文章列表
    :return: 文章对象列表
    """
    articles = Article.query.all()
    return [{
        'id': a.id,
        'title': a.title,
        'content': a.content,
        'image_url': a.image_url,
        'likes': a.likes,
        "created_at": a.created_at
    } for a in articles]


def get_article_detail(article_id):
    """
    获取文章详情
    :param article_id: 文章ID
    :return: 文章详情，包括评论
    """
    article = Article.query.get(article_id)
    if not article:
        raise ValueError("文章不存在")
    
    # 获取文章评论
    comments = get_comments_by_article(article_id)

    user = User.query.filter_by(id=article.user_id).first()
    
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'image_url': article.image_url,
        'author': user.username,
        'likes': article.likes,
        'updated_at': article.updated_at.isoformat(),
        'comments': comments
    }


def create_article(data):
    """
    创建新文章
    :param data: 包含文章信息的字典 (title, content, image_url)
    :return: 新创建的文章信息
    """
    try:
        new_article = Article(
            title=data['title'],
            user_id=data['user_id'],
            content=data['content'],
            image_url=data.get('image_url'), # image_url 是可选的
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(new_article)
        db.session.commit()
        return {
            'id': new_article.id,
            'title': new_article.title,
            'content': new_article.content,
            'image_url': new_article.image_url,
            'likes': new_article.likes,
            'user_id': new_article.user_id,
            'created_at': new_article.created_at.isoformat(),
            'updated_at': new_article.updated_at.isoformat()
        }
    except Exception as e:
        print(e)
        db.session.rollback()
        raise e

def update_article(article_id, data):
    """
    更新指定ID的文章
    :param article_id: 文章ID
    :param data: 包含更新信息的字典
    :return: 更新后的文章信息
    """
    article = Article.query.get(article_id)
    if not article:
        raise ValueError("文章不存在")

    # 更新允许修改的字段
    if 'title' in data:
        article.title = data['title']
    if 'content' in data:
        article.content = data['content']
    if 'image_url' in data:
        article.image_url = data['image_url']

    article.updated_at = datetime.utcnow()
    db.session.commit()

    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'image_url': article.image_url,
        'likes': article.likes,
        'created_at': article.created_at.isoformat(),
        'updated_at': article.updated_at.isoformat()
    }


def increment_likes(article_id):
    """
    增加文章点赞数
    :param article_id: 文章ID
    :return: 更新后的点赞数
    """
    article = Article.query.get(article_id)
    if not article:
        raise ValueError("文章不存在")
    
    article.likes += 1
    db.session.commit()
    return article.likes

def delete_article(article_id):
    """
    删除指定ID的文章
    :param article_id: 文章ID
    """
    from models.comment import Comment
    
    article = Article.query.get(article_id)
    if not article:
        raise ValueError("文章不存在")

    try:
        # 删除关联评论
        comments = Comment.query.filter_by(article_id=article_id).all()
        for comment in comments:
            db.session.delete(comment)
        
        # 删除关联点赞
        # from models.user_like import UserLike
        # likes = UserLike.query.filter_by(article_id=article_id).all()
        # for like in likes:
        #     db.session.delete(like)
        
        # 删除文章
        db.session.delete(article)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        raise e

    # 可选：删除关联的评论或点赞记录，取决于业务逻辑
    # from models.comment import Comment
    # Comment.query.filter_by(article_id=article_id).delete()
    # from models.user_like import UserLike
    # UserLike.query.filter_by(article_id=article_id).delete()

    db.session.delete(article)
    db.session.commit()