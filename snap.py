from time import sleep
from os import mkdir
from os.path import isdir, join, realpath, split
from datetime import datetime
from picamera import PiCamera


# Default Width + Height resolution.
WIDTH = 1920
HEIGHT = 1080

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
    if not isdir(string):
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
        print 'EXITING'
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
    return '{0}/{1}_{2}.{3}'.format(FOLDER_IMAGES, FILE_PREFIX, dt_now, FILE_EXT)

def configure_camera(width, height):
    assert type(width) is INT_TYPE, 'Width {0} is not an integer.'.format(width)
    assert type(height) is INT_TYPE, 'Height {0} is not an integer.'.format(height)
    set_resolution(width, height)
    camera.start_preview()

def take_picture(width, height):
    """
    Take a picture from camera.
    :param width:
    :param height:
    :return:
    """
    configure_camera(width, height)

    # Camera warm-up time
    sleep(2)

    # Get filename
    filename = make_filename()
    camera.capture(filename)

def snap():
    """
    Snaps picture.
    :return:
    """
    if get_path_images():
        take_picture(WIDTH, HEIGHT)


if __name__ == '__main__':
    snap()
