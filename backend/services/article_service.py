from models.article import Article

def get_articles_list():
    """
    获取文章列表
    :return: 文章对象列表
    """
    return Article.query.all()