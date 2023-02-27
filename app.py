import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask.logging import default_handler
from flask_migrate import Migrate

import commands
import config
import filters
from bbs_celery import make_celery
from blueprints.cms import bp as cms_bp
from blueprints.front import bp as front_bp
from blueprints.user import bp as user_bp
from blueprints.media import bp as media_bp
from exts import db, mail, cache, csrf, avatars
import hooks

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


# 完成db初始化
db.init_app(app)
# 完成mail初始化
mail.init_app(app)
# 初始化cache
cache.init_app(app)
# 初始化celery
celery = make_celery(app)
# CSRF保护
csrf.init_app(app)
# 数据库初始化
migrate = Migrate(app, db)
# 初始化头像flask_avatars
avatars.init_app(app)

# 添加钩子函数
# 添加验证用户
app.before_request(hooks.bbs_before_request)

# 添加头像模板过滤器，将函数注册到app模板全局
app.template_filter('email_hash')(filters.email_hash)

# 注册蓝图
# cms模块
app.register_blueprint(cms_bp)
# 前端页面功能
app.register_blueprint(front_bp)
# 用户模块
app.register_blueprint(user_bp)
# 文件模块
app.register_blueprint(media_bp)

# 添加命令行
app.cli.command('create-permission')(commands.create_permission)
app.cli.command('create-role')(commands.create_role)
# 添加测试用户
app.cli.command('create-test-user')(commands.create_test_user)
# 添加管理员
app.cli.command('create-admin')(commands.create_admin)
# 添加版块
app.cli.command('create-board')(commands.create_board)
# 添加测试帖子
app.cli.command('create-test-post')(commands.create_test_post)

# 错误页面钩子
app.errorhandler(401)(hooks.bbs_401_error)
app.errorhandler(404)(hooks.bbs_404_error)
app.errorhandler(500)(hooks.bbs_500_error)


# 日志打印到的文件
file_handler = RotatingFileHandler('pythonbbs.log', maxBytes=16384, backupCount=20, encoding='utf-8')
# 设置日志等级
file_handler.setLevel(logging.INFO)
# 取消控制台日志打印
# file_handler.removeHandler(default_handler)
# 创建日志记录的格式
file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]')
# 将日志格式对象添加到handler中
file_handler.setFormatter(file_formatter)
# 将handler添加到app.logger中
app.logger.addHandler(file_handler)


if __name__ == '__main__':
    app.run()
