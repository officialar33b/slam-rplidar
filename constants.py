import sys

# list of constants that will be used in multiple files.
OUTPUT_FILE = sys.argv[1]
PORT = "/dev/ttyUSB0"
MAP_SIZE = 1024
MAP_METERS = 6
SCANS = 10
MIN_SAMPLES = 500

px_per_meter = MAP_SIZE / MAP_METERS
cx = cy = MAP_SIZE // 2
