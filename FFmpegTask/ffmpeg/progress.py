import re

from FFmpegTask.utils.str_utils import str_has_token


class FFMPEGProgress(object):
    is_progress: bool

    frame: int

    hour: int
    minute: int
    second: int
    microsecond: int

    def __init__(self, output_line: str):
        process_out = ["frame=", "fps=", "q=", "size=", "time=", "bitrate=", "speed="]
        process_re = r"frame= (\d+) fps=.*? q=.*? size= .*? time=(\d+):(\d+):(\d+)\.([1-9]\d{0,2}) bitrate= .*? speed=.*?"

        if not str_has_token(output_line, process_out):
            self.is_progress = False
            return

        output_line = re.sub(r"\s+", " ", output_line)

        search_result = re.search(process_re, output_line)
        if search_result is None:
            self.is_progress = False
            return
        else:
            self.is_progress = True

        frame, hour, minute, second, microsecond = search_result.groups()

        self.frame = int(frame)
        self.hour = int(hour)
        self.minute = int(minute)
        self.second = int(second)
        self.microsecond = int(microsecond)

    def __str__(self) -> str:
        return f"" \
               f"frame: {self.frame}," \
               f"duration: {self.hour}.{self.minute}.{self.second}.{self.microsecond}"
