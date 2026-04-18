import cv2
import numpy as np

from constants import *


def draw_frame(canvas, scan):
    # draw a single scan on to the canvas and return an updated display image.
    for _, angle, distance in scan:
        if distance < 100 or distance > (MAP_METERS / 2 * 1000):
            continue
        angle = np.radians(angle)
        dist_m = distance / 1000.0
        wx = int(cx + dist_m * px_per_meter * np.cos(angle))
        wy = int(cy - dist_m * px_per_meter * np.sin(angle))
        cv2.line(canvas, (cx, cy), (wx, wy), 255, 1)
        if 0 <= wx < MAP_SIZE and 0 <= wy < MAP_SIZE:
            cv2.circle(canvas, (wx, wy), 2, 0, -1)
    cv2.circle(canvas, (cx, cy), 5, 0, -1)
    return canvas


def make_display(canvas, scan, count):
    # create the actual display.
    display = cv2.cvtColor(canvas, cv2.COLOR_GRAY2BGR)

    for _, angle, distance in scan:
        if distance < 100 or distance > (MAP_METERS / 2 * 1000):
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
    bar_px = int(px_per_m)
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
