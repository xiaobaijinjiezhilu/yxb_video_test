import os
import time

from yxb_app.libs.base_qiniu import video_qiniu
from yxb_app.models import Video,VideoSub


def video_task(command, out_path, path_name,
               video_file_name, video_sub_id):
    from yxb_app.utils.common import remove_path

    os.system(command)

    out_name = '.'.join([out_path, 'mp4'])

    if not os.path.exists(out_name):
        remove_path([out_path, path_name])
        return False

    final_name = '{}_{}'.format(int(time.time()), video_file_name)
    url = video_qiniu.put(final_name, out_name)

    if url:
        try:
            video_sub = VideoSub.objects.get(pk=video_sub_id)
            video_sub.url = url
            video_sub.save()
            return True
        except:
            return False
        finally:
            remove_path([out_path, path_name])
    remove_path([out_path, path_name])