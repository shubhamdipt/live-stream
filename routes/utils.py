from datetime import datetime, timedelta
from application import IMAGE_PATH


def get_last_frame():
    current_time = datetime.now() + timedelta(hours=1, minutes=55)  # timezone difference
    # check for latest in last 1hours
    latest_time = current_time - timedelta(hours=1)
    frame_found = False
    while current_time > latest_time and not frame_found:
        current_time = current_time - timedelta(seconds=1)
        time_string = current_time.strftime("%Y%m%d%H%M%S")
        file_string = IMAGE_PATH + time_string + ".jpg"
        try:
            frame = open(file_string, 'rb').read()
            return frame
        except:
            pass
    return open("blank.png", "rb").read()


class Camera:

    def __init__(self):
        self.frames = self.get_all_frames()
        self.last_frame_number = -1

    def get_frame(self):
        if len(self.frames) == 0:
            return open("blank.png", "rb").read()
        self.last_frame_number += 1
        if self.last_frame_number >= len(self.frames):
            self.last_frame_number = 0
        return self.frames[self.last_frame_number]

    @staticmethod
    def get_all_frames(number_of_frames=20):
        current_time = datetime.now() + timedelta(hours=1, minutes=50)  # timezone difference
        # check for latest in last 1hours
        latest_time = current_time - timedelta(hours=1)
        frames = list()
        count = 0
        failed = 0
        while current_time > latest_time and failed < 50 and count < number_of_frames:
            current_time = current_time - timedelta(seconds=1)
            time_string = current_time.strftime("%Y%m%d%H%M%S")
            file_string = IMAGE_PATH + time_string + ".jpg"
            try:
                frames.append(open(file_string, 'rb').read())
                count += 1
            except:
                failed += 1
        return frames


