from models.article import Article

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