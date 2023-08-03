import multiprocessing
import simpleaudio as sa
import time


def loopSoundFunc(path):
    wave_object = sa.WaveObject.from_wave_file(path)
    while True:
        play_object = wave_object.play()
        play_object.wait_done()


class MusicPlayer:
    def __init__(self):
        self.current = None
        pass

    def loopSong(self, path):
        self.stop()
        loopThread = multiprocessing.Process(
            target=loopSoundFunc, name="backgroundMusicThread", args=[path]
        )
        loopThread.start()
        self.current = loopThread

    def stop(self):
        if self.current:
            print("attempting to stop process")
            self.current.terminate()
            self.current = None


if __name__ == "__main__":
    player = MusicPlayer()

    player.loopSong("./music/elevator1.wav")

    time.sleep(5)

    player.loopSong("./music/elevator2.wav")

    time.sleep(5)

    player.stop()
