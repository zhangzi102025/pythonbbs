from flask import Blueprint, render_template, redirect, g, request, flash, url_for, current_app
from flask_paginate import Pagination

from decorators import permission_required
from exts import db
from forms.board import EditBoardForm
from forms.cms import AddStaffForm, EditStaffForm
from models.post import PostModel, BoardModel
from models.user import PermissionEnum, UserModel, RoleModel
from utils import restful

bp = Blueprint('cms', __name__, url_prefix='/cms')


# 页面进入前的鉴权，钩子函数
@bp.before_request
def cms_before_request():
    if not hasattr(g, 'user') or g.user.is_staff == False:
        return redirect('/')


@bp.context_processor
def cms_context_processor():
    return {'PermissionEnum': PermissionEnum}


# cms首页
@bp.get('')
def index():
    return render_template('cms/index.html')


# 员工列表页
@bp.get('/staff/list')
# 装饰器权限限制，必须有CMS_USER模块的权限
@permission_required(PermissionEnum.CMS_USER)
def staff_list():
    users = UserModel.query.filter_by(is_staff=True).all()
    return render_template('cms/staff_list.html', users=users)


# 添加员工
@bp.route('/staff/add', methods=['GET', 'POST'])
# 装饰器权限限制，必须有CMS_USER用户管理权限
@permission_required(PermissionEnum.CMS_USER)
def add_staff():
    if request.method == 'GET':
        roles = RoleModel.query.all()
        return render_template('cms/add_staff.html', roles=roles)
    else:
        form = AddStaffForm(request.form)
        if form.validate():
            email = form.email.data
            role_id = form.role.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                flash('用户不存在')
                return redirect(url_for('cms.add_staff'))
            user.is_staff = True
            user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for('cms.staff_list'))


# 编辑员工
@bp.route('/staff/edit/<string:user_id>', methods=['GET', 'POST'])
@permission_required(PermissionEnum.CMS_USER)
def edit_staff(user_id):
    user = UserModel.query.get(user_id)
    if request.method == 'GET':
        roles = RoleModel.query.all()
        return render_template('cms/edit_staff.html', user=user, roles=roles)
    else:
        form = EditStaffForm(request.form)
        if form.validate():
            is_staff = form.is_staff.data
            role_id = form.role.data
            user.is_staff = is_staff
            # 判断角色是否有修改
            if user.role.id != role_id:
                user.role = RoleModel.query.get(role_id)
            db.session.commit()
            return redirect(url_for('cms.staff_list', user_id=user_id))
        else:
            for message in form.messages:
                flash(message)
            return redirect(url_for('cms.edit_staff', user_id=user_id))


# 前台用户列表
@bp.route('/users')
@permission_required(PermissionEnum.FRONT_USER)
def user_list():
    users = UserModel.query.filter_by(is_staff=False).all()
    return render_template('cms/users.html', users=users)


@bp.post('/users/active/<string:user_id>')
@permission_required(PermissionEnum.FRONT_USER)
def active_user(user_id):
    # 账号状态
    is_active = request.form.get('is_active', type=int)
    if is_active is None:
        return restful.params_error(message='请求参数错误')
    user = UserModel.query.get(user_id)
    user.is_active = bool(is_active)
    db.session.commit()
    return restful.ok()


# 后台帖子管理列表页
@bp.get('/posts')
@permission_required(PermissionEnum.POST)
def post_list():
    # 获取页码参数
    page = request.args.get('page', type=int, default=1)
    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get('PER_PAGE_COUNT')
    # 当前page下的结束位置
    end = start + current_app.config.get('PER_PAGE_COUNT')
    # 查询对象
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    # 帖子总数
    total = query_obj.count()
    # 当前page下的帖子列表
    posts = query_obj.slice(start, end)
    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment='right')
    context = {
        'posts': posts,
        'pagination': pagination,
    }
    return render_template('cms/posts.html', **context)


# 隐藏/取消隐藏帖子
@bp.post('/posts/active/<int:post_id>')
def active_post(post_id):
    is_active = request.form.get('is_active', type=int)
    if is_active is None:
        return restful.params_error(message='参数错误')
    post = PostModel.query.get(post_id)
    post.is_active = is_active
    db.session.commit()
    return restful.ok()


# 版块管理
@bp.get('/boards')
@permission_required(PermissionEnum.BOARD)
def board_list():
    # 获取页码参数
    page = request.args.get('page', type=int, default=1)
    # 当前page下的起始位置
    start = (page - 1) * current_app.config.get('PER_PAGE_COUNT')
    # 当前page下的结束位置
    end = start + current_app.config.get('PER_PAGE_COUNT')
    # 查询对象
    query_obj = BoardModel.query.order_by(BoardModel.create_time.desc())
    # 帖子总数
    total = query_obj.count()
    # 当前page下的帖子列表
    boards = query_obj.slice(start, end)
    # 分页对象
    pagination = Pagination(bs_version=4, page=page, total=total, outer_window=0, inner_window=2, alignment='right')
    context = {
        'boards': boards,
        'pagination': pagination,
    }
    return render_template('cms/boards.html', **context)


# 隐藏/取消隐藏版块
@bp.post('/boards/active/<int:board_id>')
@permission_required(PermissionEnum.BOARD)
def active_board(board_id):
    is_active = request.form.get('is_active', type=int)
    if is_active is None:
        return restful.params_error(message='参数错误')
    post = BoardModel.query.get(board_id)
    post.is_active = is_active
    db.session.commit()
    return restful.ok()


# 编辑版块
@bp.route('/boards/edit/<int:board_id>', methods=['GET', 'POST'])
@permission_required(PermissionEnum.BOARD)
def edit_board(board_id):
    if request.method == 'GET':
        board = BoardModel.query.get(board_id)
        return render_template('cms/edit_board.html', board=board)
    else:
        form = EditBoardForm(request.form)
        if form.validate():
            name = request.form.get('name')
            board = BoardModel.query.get(board_id)
            # 判断名称是否有修改
            board.name = name
            if board.name != name:
                board.name = name
            db.session.commit()
            return redirect(url_for('cms.board_list'))
        else:
            for message in form.messages:
                flash(message)
            print(form.messages)
            return redirect(url_for('cms.edit_board', board_id=board_id))

