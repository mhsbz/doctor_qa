from models.article import Article, db
from services.comment_service import get_comments_by_article

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
    
    return {
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'image_url': article.image_url,
        'likes': article.likes,
        'updated_at': article.updated_at.isoformat(),
        'comments': comments
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