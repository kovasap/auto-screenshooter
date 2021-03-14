from datetime import datetime
import glob
import os
import subprocess
import time
from time import sleep
import logging

import click

from . import photos_api

logger = logging.getLogger(__name__)

DATA_DIR = os.path.expanduser('~/auto_screenshooter_data/')
DATE_PATTERN = '%Y-%m-%d'
IDLE_TIMEOUT_MINS = 15


def make_video(input_img_pattern, output_fname='output.mp4'):
    cmd = ['ffmpeg',
           '-framerate', '5',
           '-y',  # Overwrite output file without asking.
           '-s', '1920x1080',
           '-i', input_img_pattern,
           '-c:v', 'libx264', '-profile:v', 'high', '-crf', '20',
           '-pix_fmt', 'yuv420p',
           output_fname]
    subprocess.run(cmd, cwd=DATA_DIR)
    return DATA_DIR + output_fname


@click.command()
@click.option('--make_video', default=False,
              help='Whether to make a video periodically out of the gathered images.')
def main(make_video: bool):

    session = photos_api.get_authorized_session(
        os.path.join(DATA_DIR, '.auto_screenshooter_cred'))

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    i = 0
    active = True
    while True:
        idle_ms = int(subprocess.run(['xprintidle'],
                                     capture_output=True).stdout)
        if idle_ms / 1000 / 60 > IDLE_TIMEOUT_MINS:
            if active:
                i = 0
                active = False
                if make_video:
                    imgs = glob.glob(f'{DATA_DIR}*.png')
                    if imgs:
                        make_video(
                            f'%05d.png',
                            f'{datetime.now().strftime("%Y-%m-%d_%H:%M")}.mp4')
                        for img in imgs:
                            print(f'Removing {img}')
                            os.remove(img)
        else:
            active = True
            # IF WE WANT TO CAPTURE DAILY VIDEO REPLAYS:
            # Each screenshot is ~2 MB, so taking one screenshot every 10
            # seconds should use 2 * 6 * 60 * 12 hours/day on computer = ~8.6
            # GB
            filename = f'{DATA_DIR}{i:05}.png'
            subprocess.run(
                ['scrot',
                 filename,
                 '-p',  # Take screenshot with mouse pointer.
                 '-o',  # Overwrite existing files (if program was restarted).
                 ])
            i += 1
            photos_api.upload_photos(session, [filename], 'Auto Screenshots')
            if not make_video:
                i = 0
        time.sleep(10 * 60)


if __name__ == '__main__':
    main()
