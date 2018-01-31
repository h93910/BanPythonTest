import os

import time


class KuxToMP4Tool:
    def __init__(self, ffmpeg_path, output_path):
        self.ffmpeg_path = ffmpeg_path
        self.output_path = output_path

    def transcoding(self, input_file_path):
        (file_path, file_name) = os.path.split(input_file_path)
        # (name, extension) = os.path.splitext(file_name)
        name = os.path.splitext(file_name)[0]
        output_file_path = "%s%s%s.mp4" % (self.output_path, os.path.sep, name)

        os.system(
            '%s -y -i %s -c:v copy -c:a copy -threads 2 %s' % (self.ffmpeg_path, input_file_path, output_file_path))
        time.sleep(1)
        return os.path.exists(output_file_path)


if __name__ in "__main__":
    s = "D:\dd\cache.rar"
    (filepath, tempfilename) = os.path.split(s)
    (shotname, extension) = os.path.splitext(tempfilename)
    print(type(os.path.sep))
