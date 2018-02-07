import os

import time


class KuxToMP4Tool:
    def __init__(self, ffmpeg_path, output_path):
        self.ffmpeg_path = ffmpeg_path.replace("\\", "/")
        self.output_path = output_path.replace("\\", "/")

    def transcoding(self, input_file_path):
        (file_path, file_name) = os.path.split(input_file_path)
        # (name, extension) = os.path.splitext(file_name)
        name = os.path.splitext(file_name)[0]
        output_file_path = "%s/%s.mp4" % (self.output_path, name)

        cmd = '"%s" -y -i "%s" -c:v copy -c:a copy -threads 2 "%s"' % (
            self.ffmpeg_path, input_file_path.replace("\\", "/"), output_file_path)
        print(os.popen(cmd).read(), end="\n==========================\n")
        time.sleep(1)
        return os.path.exists(output_file_path)


if __name__ in "__main__":
    # str = '"D:/Ban/PycharmProjects/bantest/kux_to_mp4/innplayer/ffmpeg.exe" -y -i "D:/Ban/PycharmProjects/bantest/kux_to_mp4/testInputdd/test.kux" -c:v copy -c:a copy -threads 2 "D:/Ban/PycharmProjects/bantest/kux_to_mp4/testOutputaa/test.mp4"'
    str = '"D:/Ban/PycharmProjects/bantest/kux_to_mp4/innplayer/ffmpeg.exe" -y -i "D:/Ban/PycharmProjects/bantest/kux_to_mp4/testInputdd/test.kux" -c:v copy -c:a copy -threads 2 "D:/Ban/PycharmProjects/bantest/kux_to_mp4/testOutputaa/test.mp4"'
    str = str.replace("\\", "/")
