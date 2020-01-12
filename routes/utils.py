from datetime import datetime, timedelta
from application import IMAGE_PATH
import os
import re

TIME_ZONE_HOURS_DIFFERENCE = 0
TILL_HOUR = 3
TIME_FORMAT = "%Y%m%d%H%M%S"
IMAGE_FORMAT = "jpg"


def get_sorted_files(
        src_dir,
        regex_ext='*',
        sort_reverse=False,
        latest_time=datetime.now() - timedelta(hours=1)): # SHOW LAST HOUR IMAGES BY DEFAULT
    if TIME_ZONE_HOURS_DIFFERENCE > 0:
        latest_time += timedelta(hours=TIME_ZONE_HOURS_DIFFERENCE)
    else:
        latest_time -= timedelta(hours=TIME_ZONE_HOURS_DIFFERENCE)

    files_to_evaluate = []
    for f in os.listdir(src_dir):
        try:
            creation_time = datetime.strptime(f.split(".")[0], TIME_FORMAT)
            conditions = (
                re.search(r'\d{14}', f[:len(f) - 4]) and
                re.search(r'.*\.({})$'.format(regex_ext), f) and
                creation_time > latest_time
            )
            if conditions:
                files_to_evaluate.append(creation_time)
        except Exception as e:
            pass
    files_to_evaluate.sort(reverse=sort_reverse)
    files_to_evaluate = [
        open(os.path.join(
            src_dir, "{}.{}".format(i.strftime(TIME_FORMAT), regex_ext)
        ), 'rb').read() for i in files_to_evaluate
    ]
    return files_to_evaluate


class Camera:

    def __init__(self):
        # self.frames = self.get_all_frames()
        self.current_time = datetime.now()
        self.last_frame_number = -1
        self.latest_time = self.current_time - timedelta(hours=TIME_ZONE_HOURS_DIFFERENCE+TILL_HOUR)
        self.last_image = None

    def get_live_frame(self):
        curr_time = datetime.now()
        while True:
            try:
                image_file = open(
                    os.path.join(
                        IMAGE_PATH, "{}.{}".format(
                            curr_time.strftime(TIME_FORMAT),
                            IMAGE_FORMAT)), 'rb').read()
                self.last_image = image_file
                return image_file
            except FileNotFoundError:
                curr_time -= timedelta(seconds=1)
                if self.last_image:
                    return self.last_image
            except Exception as e:
                return open("loading.jpg", "rb").read()

    def get_frame(self):
        self.current_time -= timedelta(seconds=1)
        while self.current_time > self.latest_time:
            try:
                image_file = open(
                    os.path.join(
                        IMAGE_PATH, "{}.{}".format(
                            self.current_time.strftime(TIME_FORMAT),
                            IMAGE_FORMAT)), 'rb').read()
                return image_file
            except FileNotFoundError:
                self.current_time -= timedelta(seconds=1)
        return open("loading.jpg", "rb").read()

    @staticmethod
    def get_all_frames():
        return get_sorted_files(
            src_dir=IMAGE_PATH,
            regex_ext="jpg",
            sort_reverse=True,
        )


