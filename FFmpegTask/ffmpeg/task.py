import pathlib
import typing
import multiprocessing

import tqdm

from FFmpegTask.ffmpeg.command import FFMPEGCommand
from FFmpegTask.ffmpeg.info import FFMPEGInfo
from FFmpegTask.ffmpeg.progress import FFMPEGProgress
from FFmpegTask.utils.queue_utils import queue_clear


def parse_ffmpeg_process(stdout: typing.IO[str]) -> typing.Generator[FFMPEGProgress, None, None]:
    for line in stdout:
        progress = FFMPEGProgress(line)

        if not progress.is_progress:
            continue
        else:
            yield progress


def exec_ffmpeg_task(
        input_info: FFMPEGInfo,
        ffmpeg_command: FFMPEGCommand | str,
        progress_queue: multiprocessing.Queue,
):
    if isinstance(ffmpeg_command, str):
        process = FFMPEGCommand.call(ffmpeg_command)
    elif isinstance(FFMPEGCommand, str):
        process = ffmpeg_command()
    else:
        raise ValueError("'ffmpeg_command' must be FFMPEGCommand or str")

    with tqdm.tqdm(total=input_info.total_frame, initial=0, desc="ffmpeg progress") as tqdm_bar:
        frame_progress = 0
        for progress in parse_ffmpeg_process(process.stdout):
            rate = progress.frame / input_info.total_frame
            tqdm_bar.update(progress.frame - frame_progress)
            frame_progress = progress.frame
            progress_queue.put(rate)
        progress_queue.put("1")

if __name__ == "__main__":
    input_file = pathlib.Path("D:\\Videos\\ffmpeg\\1.mkv")
    input_subtitle_files = []
    output_file = pathlib.Path("D:\\Videos\\ffmpeg\\1.mp4")
    choose_video_streams = [0]
    choose_audio_streams = [0]
    choose_subtitle_streams = []

    input_info = FFMPEGInfo(input_file)
    ffmpeg_command = FFMPEGCommand(input_info, input_subtitle_files, output_file, choose_video_streams, choose_audio_streams, choose_subtitle_streams)
    progress_queue = multiprocessing.Queue()

    print(input_info)
    print(ffmpeg_command)

    exec_ffmpeg_task(input_info, ffmpeg_command, progress_queue)

    queue_clear(progress_queue)
