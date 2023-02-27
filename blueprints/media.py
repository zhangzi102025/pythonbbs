from flask import Blueprint, current_app, send_file
import os


bp = Blueprint('media', __name__, url_prefix='/media')


# 通过文件名获取文件
@bp.route('/<path:filename>')
def media_file(filename):
    image_file = os.path.join(current_app.config.get('UPLOAD_IMAGE_PATH'), filename)
    # 使用 send_file() 函数返回文件
    return send_file(image_file)