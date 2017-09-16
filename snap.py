from time import sleep
from datetime import datetime
from picamera import PiCamera


# Default Width + Height resolution.
WIDTH = 1920
HEIGHT = 1080

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
    return 'images/{0}_{1}.{2}'.format(FILE_PREFIX, dt_now, FILE_EXT)

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
    filename = make_filename()
    camera.capture(filename)


if __name__ == '__main__':
    take_picture(WIDTH, HEIGHT)
