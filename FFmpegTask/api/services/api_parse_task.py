import os
import pathlib
from pydantic import BaseModel

from FFmpegTask.ffmpeg.info import FFMPEGInfo


class ApiParseTaskBody(BaseModel):
    src_folder: str

    video_files: list[str]

    subtitle_files: list[str]


def api_parse_task(body: ApiParseTaskBody):
    src_folder = pathlib.Path(body.src_folder)
    video_files = []
    subtitle_files = []

    info_map = []

    for file in body.video_files:
        fp = src_folder / pathlib.Path(file)
        video_files.append(fp)

    for file in body.subtitle_files:
        fp = src_folder / pathlib.Path(file)
        subtitle_files.append(fp)

    for file in video_files:
        u = {
            "video_file": file.name,
            "subtitle_file": [],
            "info": FFMPEGInfo(file)
        }

        name, _ = os.path.splitext(file.name)

        match_name_list = [f"{name}{ext}" for ext in [".ass", ".srt"]]
        match_result = []

        for subtitle_file in subtitle_files:

            if subtitle_file.name in match_name_list:
                match_result.append(subtitle_file.name)

        u["subtitle_file"] = match_result.copy()

        info_map.append(u)

    return info_map
