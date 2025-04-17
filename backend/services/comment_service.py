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


def update_comment(data, user):
    """
    更新评论
    :param data: 包含评论ID和新内容的字典
    :param user: 当前用户对象
    :return: 更新后的评论对象
    """
    # 验证用户权限
    if user.user_type != 'admin':
        raise ValueError('只有管理员可以修改评论')
    
    # 验证评论存在
    comment = Comment.query.get(data.get('comment_id'))
    if not comment:
        raise ValueError('评论不存在')
    
    # 更新评论内容
    comment.content = data.get('content', comment.content)
    
    db.session.commit()
    return comment


def delete_comment(comment_id, user):
    """
    删除评论
    :param comment_id: 评论ID
    :param user: 当前用户对象
    :return: 被删除的评论ID
    """
    # 验证用户权限
    if user.user_type != 'admin':
        raise ValueError('只有管理员可以删除评论')
    
    # 验证评论存在
    comment = Comment.query.get(comment_id)
    if not comment:
        raise ValueError('评论不存在')
    
    db.session.delete(comment)
    db.session.commit()
    return comment_id
