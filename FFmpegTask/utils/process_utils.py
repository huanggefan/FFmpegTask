import subprocess


def close_subprocess_process(process: subprocess.Popen, kill: bool = False):
    def close():
        try:
            if process.poll() is None:
                if kill:
                    process.kill()
                else:
                    process.terminate()
        except:
            pass

    return close
