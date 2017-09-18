from time import sleep
from os import mkdir
from os.path import isdir, join, realpath, split
from datetime import datetime
from picamera import PiCamera


# Default Width + Height resolution.
WIDTH = 3280
HEIGHT = 2464

# Default Settings
SHARPNESS = 0
CONTRAST = 0
BRIGHTNESS = 70 # DEFAULT 50
SATURATION = 0
ISO = 0

# Image Flips
FLIP_VERTICAL = True
FLIP_HORIZONTAL = True

# Default images folder name
FOLDER_IMAGES = 'images'

# Default images folder permissions
FOLDER_IMAGES_PERMISSIONS = 0755

# Datetime Format String
DT_STRING = '%Y%m%d_%H%M%S'

# Prefix for filename.
FILE_PREFIX = 'img'

# File extension.
FILE_EXT = 'jpg'

# Define Integer type for reuse.
INT_TYPE = type(0)

# print 'realpath: {0}'.format(realpath(__file__))

# Camera object
camera = PiCamera()

def print_directory_create(message, path):
    """
    Lazy log print for directory creation.
    :param message:
    :param path:
    :return:
    """
    print('DIRECTORY CREATE - {0} - {1}'.format(message, path))

def ensure_path_exists(string):
    """
    Ensure directory exists (for images).
    :param string:
    :return:
    """
    if isdir(string):
        print_directory_create('EXISTS', string)
    else:
        mkdir(string, FOLDER_IMAGES_PERMISSIONS)
        if not isdir(string):
            print_directory_create('ERROR', string)
            return False
        print_directory_create('SUCCESS', string)
    return True

def get_path_file():
    """
    Get path from current file.
    :return:
    """
    return realpath(__file__)

def get_path_images():
    """
    Compile images path.
    :return:
    """
    _path = get_path_file()
    split_path = split(_path)
    root_path = split_path[0]
    images_path = join(root_path, FOLDER_IMAGES)
    if not ensure_path_exists(images_path):
        print 'EXITING - PATH NOT EXIST'
        exit()
    return images_path

def set_resolution(width, height):
    """
    Set camera resolution.
    :param width:
    :param height:
    :return:
    """
    camera.resolution = (width, height)

def get_dt_string():
    """
    Get datetime string.
    :return:
    """
    now = datetime.utcnow()
    return now.strftime(DT_STRING)

def make_filename():
    """
    Create image filename.
    :return:
    """
    dt_now = get_dt_string()
    images_path = get_path_images()
    # print 'Gotten Path For Images in Make Filename: {0}'.format(images_path)
    filename = '{0}_{1}.{2}'.format(FILE_PREFIX, dt_now, FILE_EXT)
    out = join(images_path, filename)
    print 'IMAGE|{0}'.format(filename)
    return out

def configure_camera(width, height):
    # assert type(width) is INT_TYPE, 'Width {0} is not an integer.'.format(width)
    # assert type(height) is INT_TYPE, 'Height {0} is not an integer.'.format(height)
    set_resolution(width, height)
    camera.sharpness = SHARPNESS
    camera.contrast = CONTRAST
    camera.brightness = BRIGHTNESS
    camera.saturation = SATURATION
    camera.ISO = ISO
    camera.hflip = FLIP_HORIZONTAL
    camera.vflip = FLIP_VERTICAL
    print 'SETTINGS|W={0},H={1},SHARP={2},CONT={3},BRIGHT={4},SAT={5},ISO={6},HFLIP={7},VFLIP={8}'.format(
        width, height, SHARPNESS, CONTRAST, BRIGHTNESS, SATURATION, ISO, FLIP_HORIZONTAL, FLIP_VERTICAL
    )
    # camera.start_preview()

def take_picture(width, height):
    """
    Take a picture from camera.
    :param width:
    :param height:
    :return:
    """
    configure_camera(width, height)

    # Camera warm-up time
    sleep(1)

    # Get filename
    filename = make_filename()
    camera.capture(filename)
    sleep(1)

def snap():
    """
    Snaps picture.
    :return:
    """
    # if get_path_images():
    take_picture(WIDTH, HEIGHT)

snap()
