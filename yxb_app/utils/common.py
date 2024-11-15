# coding:utf-8
from config import settings
import os
import time
import shutil
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
import tempfile
import subprocess
from yxb_app.libs.base_qiniu import video_qiniu
from yxb_app.model.video import VideoSub, Video
from yxb_app.tasks.task import video_task


def check_and_get_video_type(type_obj, type_value, message):
    try:
        type_obj(type_value)

    except:
        return {'code': -1, 'msg': message}

    return {'code': 0, 'msg': 'success'}


def remove_path(paths):
    for path in paths:
        if os.path.exists(path):
            os.remove(path)


def handel_video(video_file, video_id, number):
    in_path = os.path.join(settings.BASE_DIR, 'yxb_app/dashboard/temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'yxb_app/dashboard/temp_out')

    # 确保输入和输出目录存在
    os.makedirs(in_path, exist_ok=True)
    os.makedirs(out_path, exist_ok=True)

    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = os.path.join(in_path, name)

    # 处理 TemporaryUploadedFile 和 InMemoryUploadedFile 对象
    if isinstance(video_file, TemporaryUploadedFile):
        temp_path = video_file.temporary_file_path()
        shutil.copyfile(temp_path, path_name)
    elif isinstance(video_file, InMemoryUploadedFile):
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(video_file.name)[-1]) as temp_file:
            temp_file.write(video_file.read())
            temp_path = temp_file.name

        try:
            shutil.copyfile(temp_path, path_name)
        finally:
            os.remove(temp_path)  # 删除临时文件

    # 确保文件已写入磁盘，并打印路径进行调试
    if not os.path.exists(path_name):
        print(f"Error: The input file {path_name} does not exist.")
        return

    print(f"Input file {path_name} exists.")

    out_name = '{}_{}'.format(int(time.time()), os.path.splitext(video_file.name)[0])
    out_path = os.path.join(out_path, out_name)

    # 构建并执行 ffmpeg 命令
    command = ['ffmpeg', '-i', path_name, '-c', 'copy', f'{out_path}.mp4']

    try:
        subprocess.run(command, check=True)
        out_name = '.'.join([out_path, 'mp4'])
        if not os.path.exists(out_name):
            remove_path([out_name, path_name])
            return False
        url = video_qiniu.put(video_file.name, out_name)
        print(url)
        if url:
            video = Video.objects.get(pk=video_id)
            try:
                video_sub = VideoSub.objects.create(
                    video=video,
                    url=url,
                    number=number
                )
                video_task.delay(
                    command, out_path, path_name, video_file.name, video_sub.id)
                return True
            except:
                return False
            finally:
                remove_path([out_name, path_name])
        remove_path([out_name, path_name])
        return False

    except subprocess.CalledProcessError as e:
        print(f"Error during ffmpeg execution: {e}")

    # 清理临时输入文件
    if os.path.exists(path_name):
        os.remove(path_name)
