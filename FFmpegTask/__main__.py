import multiprocessing

import uvicorn

from FFmpegTask.api.app import app
from FFmpegTask.background import background

if __name__ == "__main__":
    background_process = multiprocessing.Process(target=background)
    background_process.start()

    uvicorn.run(app=app, host="127.0.0.1", port=8888)
