from time import sleep
from os import mkdir
from os.path import isdir, join, realpath, split
from datetime import datetime
from picamera import PiCamera


# EXAMPLE
#
# BRIGHTNESS    50
# CONTRACT      0
# EXPOSURE_MODE 'none'
# ISO           0
# SATURATION    0
# SHARPNESS     0
#

CONFIG = {
    # Default Flip Settings
    'FLIP':{
        'HORIZONTAL': True,
        'VERTICAL': True,
    },

    # Exposure Dependant
    'SHORT': {
        # Default Width + Height resolution.
        'RESOLUTION': {
            'WIDTH': 3280,
            'HEIGHT': 2464
        },
        'DAY': {
            'BRIGHTNESS': 50,
            'CONTRAST': 0,
            'EXPOSURE_MODE': 'none',
            'ISO': 100,
            'SATURATION': 0,
            'SHARPNESS': 0,
        },
        'NIGHT': {
            'BRIGHTNESS': 50,
            'CONTRAST': 0,
            'EXPOSURE_MODE': 'none',
            'ISO': 100,
            'SATURATION': 0,
            'SHARPNESS': 0,
        }
    },
    'LONG': {
        # Default Width + Height resolution.
        'RESOLUTION': {
            'WIDTH': 1920,
            'HEIGHT': 1200
        },
        'DAY': {
            'BRIGHTNESS': 50,
            'CONTRAST': 0,
            'EXPOSURE_MODE': 'off',
            'ISO': 100,
            'SATURATION': 0,
            'SHARPNESS': 0,
            'SHUTTER': 10000000,  # 6000000 = 6s
        },
        'NIGHT': {
            'BRIGHTNESS': 75,
            'CONTRAST': 0,
            'EXPOSURE_MODE': 'night',
            'ISO': 800,
            'SATURATION': 0,
            'SHARPNESS': 0,
            'SHUTTER': 10000000,  # 6000000 = 6s
        }
    }
}


# -----------------------
#
# PREDEFINES
#
# -----------------------

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



# -----------------------
#
# SETTINGS
#
# -----------------------

# Is this long exposure?
LONG_EXPOSURE = True

# Is it day time?
# TODO Match to sunrise sunset.
TIME_DAY = False

ACTIVE_CONFIG = CONFIG['LONG'] if LONG_EXPOSURE else CONFIG['SHORT']
RESOLUTION_CONFIG = ACTIVE_CONFIG['RESOLUTION']
ACTIVE_CONFIG = ACTIVE_CONFIG['DAY'] if TIME_DAY else ACTIVE_CONFIG['NIGHT']
FLIP_CONFIG = CONFIG['FLIP']


# Camera object
camera = PiCamera(sensor_mode=3) if LONG_EXPOSURE else PiCamera()


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
    camera.sharpness = ACTIVE_CONFIG['SHARPNESS']
    camera.contrast = ACTIVE_CONFIG['CONTRAST']
    camera.brightness = ACTIVE_CONFIG['BRIGHTNESS']
    camera.saturation = ACTIVE_CONFIG['SATURATION']
    if LONG_EXPOSURE:
        camera.shutter_speed = ACTIVE_CONFIG['SHUTTER']
    camera.ISO = ACTIVE_CONFIG['ISO']
    camera.hflip = FLIP_CONFIG['HORIZONTAL']
    camera.vflip = FLIP_CONFIG['VERTICAL']
    # camera.start_preview()

def take_picture(width, height):
    """
    Take a picture from camera.
    :param width:
    :param height:
    :return:
    """

    # Get filename
    filename = make_filename()

    configure_camera(width, height)

    # Camera warm-up time
    if LONG_EXPOSURE:
        sleep(30)
        camera.exposure_mode = ACTIVE_CONFIG['EXPOSURE_MODE']
    else:
        sleep(2)

    camera.capture(filename)
    sleep(1)
    print 'SETTINGS|W={0},H={1},SHARP={2},CONT={3},BRIGHT={4},SAT={5},ISO={6},HFLIP={7},VFLIP={8},TIME_DAY={9},EXP_MODE={10}'.format(
        width,
        height,
        ACTIVE_CONFIG['SHARPNESS'],
        ACTIVE_CONFIG['CONTRAST'],
        ACTIVE_CONFIG['BRIGHTNESS'],
        ACTIVE_CONFIG['SATURATION'],
        ACTIVE_CONFIG['ISO'],
        FLIP_CONFIG['HORIZONTAL'],
        FLIP_CONFIG['VERTICAL'],
        TIME_DAY,
        ACTIVE_CONFIG['EXPOSURE_MODE']
    )

def snap():
    """
    Snaps picture.
    :return:
    """
    # if get_path_images():
    take_picture(RESOLUTION_CONFIG['WIDTH'], RESOLUTION_CONFIG['HEIGHT'])

snap()
