from models.user import User
from models.article import Article
from models.comment import Comment
from models.db import db

def create_comment(data):
    # 验证用户存在
    user = User.query.get(data.get('user_id'))
    if not user:
        raise ValueError('用户不存在')
    
    # 验证文章存在
    article = Article.query.get(data.get('article_id'))
    if not article:
        raise ValueError('文章不存在')
    
    # 创建评论
    new_comment = Comment(
        content=data['content'],
        user_id=user.id,
        article_id=article.id
    )
    
    db.session.add(new_comment)
    db.session.commit()
    return new_comment
