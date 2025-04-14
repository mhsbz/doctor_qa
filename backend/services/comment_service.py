from models.user import User
from models.article import Article
from models.comment import Comment
from models.db import db
from sqlalchemy import desc

def get_comments_by_article(article_id):
    # 验证文章存在
    article = Article.query.get(article_id)
    if not article:
        raise ValueError('文章不存在')
    
    # 获取评论并关联用户信息
    comments = Comment.query\
        .join(User)\
        .filter(Comment.article_id == article_id)\
        .order_by(desc(Comment.created_at))\
        .all()
    
    # 序列化结果
    return [
        {
            'id': c.id,
            'content': c.content,
            'username': c.user.username,
            'created_at': c.created_at.isoformat()
        }
        for c in comments
    ]


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
