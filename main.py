import os
import time

import cv2
import numpy as np

# from rplidar import RPLidar  # Lidar control
from pyrplidar import PyRPlidar

from constants import *

# from live_feed import draw_frame, make_display
from live_red_feed import draw_frame, make_display

# Creating a output directory to save the output each time the program is run.
if not os.path.exists("output/"):
    os.makedirs("output/")

# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# csv_path = f"output/scan_{timestamp}.csv"

canvas = np.full((MAP_SIZE, MAP_SIZE), 127, dtype=np.uint8)


lidar = PyRPlidar()
lidar.connect(port=PORT, baudrate=BAUDRATE, timeout=3)
lidar.set_motor_pwm(660)

time.sleep(2)
count = 0

cv2.namedWindow("SLAM map", cv2.WINDOW_NORMAL)
cv2.resizeWindow("SLAM map", 700, 700)

print(f"Collecting scans: {SCANS} scans, move slowly around the room.")
print("Press Q in the window to quit or stop early.")

try:
    scan_generator = lidar.force_scan()
    current_scan = list()

    for measurement in scan_generator():
        current_scan.append(
            (measurement.quality, measurement.angle, measurement.distance)
        )
        if measurement.start_flag and len(current_scan) > MIN_SAMPLES:
            scan = current_scan
            current_scan = list()

            canvas = draw_frame(canvas, scan)
            display = make_display(canvas, scan, count + 1)
            cv2.imshow("SLAM map", display)
            count += 1
            print(f" Scan {count}/{SCANS}  ({len(scan)} points)")

            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Stopped early by user")
                break
            if count >= SCANS:
                break

    # for scan in lidar.iter_scans():
    #     if len(scan) < MIN_SAMPLES:
    #         continue
    #     canvas = draw_frame(canvas, scan)
    #     display = make_display(canvas, scan, count + 1)

    #     cv2.imshow("SLAM map", display)

    #     count += 1
    #     print(f" Scan {count}/{SCANS}  ({len(scan)} points)")

    #     # add the quit (Q) functionality.
    #     if cv2.waitKey(1) & 0xFF == ord("q"):
    #         print("Stopped early by user")
    #         break
    #     if count >= SCANS:
    #         break
except KeyboardInterrupt:
    print("\nCtrl+C recieved")
finally:
    lidar.stop()
    lidar.disconnect()
    cv2.destroyAllWindows()


# saving the final output from the scan.
image_file = f"output/{OUTPUT_FILE}.png"
cv2.imwrite(image_file, canvas)
print(f"saved {OUTPUT_FILE}")
