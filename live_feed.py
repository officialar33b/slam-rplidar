import csv

import cv2
import numpy as np

from constants import *

# csv_file = open(csv_path, "w", newline="")
# writer = csv.writer(csv_file)
# writer.writerow(["scan_num", "quality", "angle", "distance", "x_m", "y_m"])


def draw_frame(canvas, scan):
    # make a sub-process that handles saving the data into a csv file.
    csv_path = f"output/{OUTPUT_FILE}.csv"
    csv_file = open(csv_path, "w", newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["scan_num", "quality", "angle", "distance", "x_m", "y_m"])
    # draw a single scan on to the canvas and return an updated display image.
    count = 0
    for quality, angle, distance in scan:
        if quality == 0 or distance < 100 or distance > (MAP_METERS / 2 * 1000):
            continue
        angle = np.radians(angle)
        dist_m = distance / 1000.0
        wx = int(cx + dist_m * px_per_meter * np.cos(angle))
        wy = int(cy - dist_m * px_per_meter * np.sin(angle))
        cv2.line(canvas, (cx, cy), (wx, wy), 255, 1)
        if 0 <= wx < MAP_SIZE and 0 <= wy < MAP_SIZE:
            cv2.circle(canvas, (wx, wy), 2, 0, -1)
        writer.writerow(
            [count, quality, round(angle, 3), distance, round(wx, 4), round(wy, 4)]
        )
        count += 1
    csv_file.close()
    cv2.circle(canvas, (cx, cy), 5, 0, -1)
    return canvas


def make_display(canvas, scan, count):
    # create the actual display.
    display = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)

    for quality, angle, distance in scan:
        if quality == 0 or distance < 100 or distance > (MAP_METERS / 2 * 1000):
            continue
        angle = np.radians(angle)
        dist_m = distance / 1000.0
        wx = int(cx + dist_m * px_per_meter * np.cos(angle))
        wy = int(cy - dist_m * px_per_meter * np.sin(angle))

        if 0 <= wx < MAP_SIZE and 0 <= wy < MAP_SIZE:
            cv2.circle(canvas, (wx, wy), 2, 0, -1)

    cv2.circle(display, (cx, cy), 6, (0, 0, 255), -1)
    cv2.putText(
        display,
        f"Scan: {count}/{scan}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
    )
    cv2.putText(
        display,
        "Press Q to stop and save early",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (200, 200, 200),
        1,
    )

    # draw the scale bar.
    bar_px = int(px_per_meter)
    bar_y = MAP_SIZE - 20

    cv2.line(display, (10, bar_y), (10 + bar_px, bar_y), (0, 255, 255), 2)
    cv2.putText(
        display,
        "1m",
        (10 + bar_px + 5, bar_y + 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        1,
    )

    return display
