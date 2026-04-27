import sys
from datetime import datetime

# list of constants that will be used in multiple files.
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# OUTPUT_FILE = sys.argv[1]
OUTPUT_FILE = f"{str(sys.argv[1])}_{timestamp}"
PORT = "/dev/ttyUSB0"
DIST_MIN_MM = 10
DIST_MAX_MM = 40000
MAP_SIZE = 1024
MAP_METERS = 3
SCANS = 200
MIN_SAMPLES = 500
BAUDRATE = 115200

px_per_meter = MAP_SIZE / MAP_METERS
cx = cy = MAP_SIZE // 2
