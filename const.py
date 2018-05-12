# encoding: UTF-8

import os


class Constant:
    conf_dir = os.path.join(os.path.expanduser('~'), '.netease-music_api')
    download_dir = conf_dir + "/cached"
