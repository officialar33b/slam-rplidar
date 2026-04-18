import cv2
import numpy as np
from rplidar import RPLidar  # Lidar control

from constants import *
from live_feed import draw_frame, make_display

canvas = np.full((MAP_SIZE, MAP_SIZE), 127, dtype=np.uint8)


lidar = RPLidar(PORT)
count = 0

cv2.namedWindow("SLAM map", cv2.WINDOW_NORMAL)
cv2.resizeWindow("SLAM map", 700, 700)

print(f"Collecting scans: {SCANS} scans, move slowly around the room.")
print("Press Q in the window to quit or stop early.")

try:
    for scan in lidar.iter_scans():
        if len(scan) < MIN_SAMPLES:
            continue
        canvas = draw_frame(canvas, scan)
        display = make_display(canvas, scan, count + 1)

        cv2.imshow("SLAM map", display)

        count += 1
        print(f" Scan {count}/{SCANS}  ({len(scan)} points)")

        # add the quit (Q) functionality.
        if cv2.waitKey(1) & 0xFF == ord("q"):
            print("Stopped early by user")
            break
        if count >= SCANS:
            break
except KeyboardInterrupt:
    print("\nCtrl+C recieved")
finally:
    lidar.stop()
    lidar.disconnect()
    cv2.destroyAllWindows()


cv2.imwrite(OUTPUT_FILE, canvas)
print(f"saved {OUTPUT_FILE}")
