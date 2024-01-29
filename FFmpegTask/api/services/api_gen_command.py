import os
import pathlib
from pydantic import BaseModel

from FFmpegTask.ffmpeg.command import FFMPEGCommand
from FFmpegTask.ffmpeg.info import FFMPEGInfo


class Item(BaseModel):
    input_file: pathlib.Path
    input_subtitle_files: list[pathlib.Path]

    output_file: str

    choose_video_streams: list[int]
    choose_audio_streams: list[int]
    choose_subtitle_streams: list[int]


class ApiGenCommandBody(BaseModel):
    src_folder: pathlib.Path
    out_folder: pathlib.Path
    item_list: list[Item]


def api_gen_command(body: ApiGenCommandBody):
    result = []

    os.makedirs(body.out_folder, exist_ok=True)

    for item in body.item_list:
        input_file = body.src_folder / item.input_file
        input_file_info = FFMPEGInfo(input_file)

        input_subtitle_files = [body.src_folder / s for s in item.input_subtitle_files]

        output_file_name = item.output_file + ".mkv"
        output_file = body.out_folder / output_file_name

        command = FFMPEGCommand(
            input_file_info,
            input_subtitle_files,
            output_file,
            item.choose_video_streams,
            item.choose_audio_streams,
            item.choose_subtitle_streams
        )

        u = {
            "src_video": item.input_file,
            "out_video": output_file_name,
            "command": command.command,
        }

        result.append(u)

    return result
