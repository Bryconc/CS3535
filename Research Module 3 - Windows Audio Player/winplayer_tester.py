__author__ = 'Brycon'

import os
import winplayer as wp

def main():
    test_directory = "Test_Files"

    files = [f for f in os.listdir(test_directory) if os.path.isfile(os.path.join(test_directory, f))]
    player = wp.WinPlayer()

    from random import shuffle
    shuffle(files)

    for f in files:
        player.add_audio("%s/%s" % (test_directory, f))

    player.play()

    import time

    time.sleep(50)
    player.pause()
    time.sleep(20)
    player.play()


if __name__ == "__main__":
    main()