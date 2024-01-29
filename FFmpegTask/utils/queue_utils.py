import queue
import typing


def queue_clear(input_queue: queue.Queue):
    while input_queue.qsize() > 0:
        try:
            input_queue.get_nowait()
        except queue.Empty:
            continue


def queue_loader(input_queue: queue.Queue, timeout: float = 0.1, stop: str = "STOP") -> typing.Iterable:
    while True:
        try:
            data = input_queue.get(block=True, timeout=timeout)

            if data == stop:
                break
            else:
                yield data
        except queue.Empty:
            continue
