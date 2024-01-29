import atexit
import subprocess

import pathlib

from FFmpegTask.ffmpeg.info import FFMPEGInfo
from FFmpegTask.utils.process_utils import close_subprocess_process


class FFMPEGCommand(object):
    input_file_info: FFMPEGInfo

    input_subtitle_files: list[pathlib.Path]

    output_file: pathlib.Path

    choose_video_streams: list[int]
    choose_audio_streams: list[int]
    choose_subtitle_streams: list[int]

    @property
    def _subtitle_file_inputs(self) -> str:
        input_list = []

        for input_subtitle_file in self.input_subtitle_files:
            input_list.append(f"-i {input_subtitle_file}")

        return " ".join(input_list)

    @property
    def _choose_video_streams_map(self) -> str:
        map_list = []

        for choose_stream in self.choose_video_streams:
            map_list.append(f"-map 0:v:{choose_stream}")

        return " ".join(map_list)

    @property
    def _choose_audio_streams_map(self) -> str:
        map_list = []

        for choose_stream in self.choose_audio_streams:
            map_list.append(f"-map 0:a:{choose_stream}")

        return " ".join(map_list)

    @property
    def _choose_subtitle_streams_map(self) -> str:
        map_list = []

        for choose_stream in self.choose_subtitle_streams:
            map_list.append(f"-map 0:s:{choose_stream}")

        return " ".join(map_list)

    @property
    def _input_subtitle_files_map(self) -> str:
        map_list = []

        for input_subtitle_file_inx in range(len(self.input_subtitle_files)):
            map_list.append(f"-map {input_subtitle_file_inx + 1}:s")

        return " ".join(map_list)

    @property
    def _convert_video(self) -> str:
        convert_list = []

        for choose_stream_inx in self.choose_video_streams:
            stream = self.input_file_info.video_streams[choose_stream_inx]
            if stream.codec_name == "av1":
                continue
            else:
                convert_list.append(f"-c:v:{choose_stream_inx} av1")

        return " ".join(convert_list)

    @property
    def _convert_audio(self) -> str:
        convert_list = []

        for choose_stream_inx in self.choose_audio_streams:
            stream = self.input_file_info.audio_streams[choose_stream_inx]
            if stream.codec_name == "aac":
                continue
            else:
                convert_list.append(f"-c:a:{choose_stream_inx} aac")

        return " ".join(convert_list)

    @property
    def _convert_subtitle(self) -> str:
        convert_list = []

        for choose_stream_inx in self.choose_subtitle_streams:
            stream = self.input_file_info.subtitle_streams[choose_stream_inx]
            if stream.codec_name == "ass":
                continue
            else:
                convert_list.append(f"-c:s:{choose_stream_inx} ass")

        return " ".join(convert_list)

    @property
    def command(self) -> str:
        return f"ffmpeg -hide_banner -threads 1 " \
               f"-i {self.input_file_info.input_file} " \
               f"{self._subtitle_file_inputs} " \
               f"{self._convert_video} " \
               f"{self._convert_audio} " \
               f"{self._convert_subtitle} " \
               f"{self._choose_video_streams_map} " \
               f"{self._choose_audio_streams_map} " \
               f"{self._choose_subtitle_streams_map} " \
               f"{self._input_subtitle_files_map} " \
               f"{self.output_file} -y"

    def __init__(self,
                 input_file_info: FFMPEGInfo,
                 input_subtitle_files: list[pathlib.Path],
                 output_file: pathlib.Path,
                 choose_video_streams: list[int],
                 choose_audio_streams: list[int],
                 choose_subtitle_streams: list[int],
                 ):
        self.input_file_info = input_file_info
        self.input_subtitle_files = input_subtitle_files
        self.output_file = output_file

        self.choose_video_streams = choose_video_streams
        self.choose_audio_streams = choose_audio_streams
        self.choose_subtitle_streams = choose_subtitle_streams

    def __str__(self) -> str:
        return self.command

    def __call__(self, ) -> subprocess.Popen:
        process = subprocess.Popen(args=self.command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=False, text=True)
        atexit.register(close_subprocess_process(process, kill=True))
        return process

    @staticmethod
    def call(command: str):
        process = subprocess.Popen(args=command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, shell=False, text=True)
        atexit.register(close_subprocess_process(process, kill=True))
        return process
