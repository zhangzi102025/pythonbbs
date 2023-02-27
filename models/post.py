from exts import db
from datetime import datetime


# 版块模型
class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)


# 帖子模型
class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    #关联表模型
    board = db.relationship('BoardModel', backref='posts')
    author = db.relationship('UserModel', backref='posts')


# 评论模型
class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'), nullable=False)

    # 关联表模型，lazy='dynamic'属性使posts.comments这个query对象可以使用filter或者filter_by进行过滤
    post = db.relationship('PostModel', backref=db.backref('comments', order_by=create_time.desc(), lazy='dynamic'))
    author = db.relationship('UserModel', backref='comments')
