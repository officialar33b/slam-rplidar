import csv

import cv2
import numpy as np

from constants import *

def _polar_to_pixel(angle_deg, dist_mm):
    # fixes the orientation hopefully of the simulation.
    if dist_mm < DIST_MIN_MM or dist_mm > DIST_MAX_MM:
        return None 
    rotated_deg = (ANGLE_DIRECTION * angle_deg + ANGLE_OFFSET) % 360. 
    angle = np.radians(rotated_deg)
    dist_m = dist_mm/ 1000. 
    wx = int(cx + dist_m * px_per_meter * np.cos(angle))
    wy = int(cy - dist_m * px_per_meter * np.sin(angle))

    return wx, wy
    

def draw_frame(canvas, scan):
    csv_path = f"output/{OUTPUT_FILE}.csv"
    csv_file = open(csv_path, "w", newline="")
    writer = csv.writer(csv_file)
    writer.writerow(["scan_num", "quality", "angle", "distance", "x_m", "y_m"])
 
    # draw a single scan on to the canvas and return an updated display image.
    count = 0
    for quality, angle_deg, dist_mm in scan:
        if quality == 0:
            continue
 
        pixel = _polar_to_pixel(angle_deg, dist_mm)
        if pixel is None:
            continue
        wx, wy = pixel
 
        if 0 <= wx < MAP_SIZE and 0 <= wy < MAP_SIZE:
            canvas[wy, wx] = 0  # mark as wall
        count += 1
 
    csv_file.close()
    return canvas
 
 
def make_display(canvas, scan, count):
    # Black background — no ray fill
    display = np.zeros((MAP_SIZE, MAP_SIZE, 3), dtype=np.uint8)
 
    # Draw all accumulated wall points in dark red
    wall_mask = canvas < 64  # black pixels = walls
    display[wall_mask] = (40, 40, 120)
 
    # Draw latest scan points as bright red dots (RViz style)
    for quality, angle_deg, dist_mm in scan:
        if quality == 0:
            continue
 
        pixel = _polar_to_pixel(angle_deg, dist_mm)
        if pixel is None:
            continue
        wx, wy = pixel
 
        if 0 <= wx < MAP_SIZE and 0 <= wy < MAP_SIZE:
            cv2.circle(display, (wx, wy), 2, (0, 0, 220), -1)  # red dots
 
    # Lidar center — white crosshair
    cv2.drawMarker(
        display, (cx, cy), (255, 255, 255), cv2.MARKER_CROSS, 20, 1, cv2.LINE_AA
    )
 
    # Small "nose" indicator: a short line from the center pointing in the
    # current ANGLE_OFFSET direction, so you can see at a glance which way
    # the sensor's front is on screen.
    # nose_len = int(px_per_meter * 0.4)
    # nose_rad = np.radians((ANGLE_OFFSET + 180.) % 360.0)
    # nose_x = int(cx + nose_len * np.cos(nose_rad))
    # nose_y = int(cy - nose_len * np.sin(nose_rad))
    # cv2.arrowedLine(
        # display, (cx, cy), (nose_x, nose_y), (0, 200, 200), 2, cv2.LINE_AA, tipLength=0.3
    # )
 
    # Grid lines (subtle dark gray)
    grid_spacing = int(px_per_meter * 0.25)  # every 25cm
    for x in range(0, MAP_SIZE, grid_spacing):
        cv2.line(display, (x, 0), (x, MAP_SIZE), (30, 30, 30), 1)
    for y in range(0, MAP_SIZE, grid_spacing):
        cv2.line(display, (0, y), (MAP_SIZE, y), (30, 30, 30), 1)
 
    # Highlight 1m grid lines slightly brighter
    grid_1m = int(px_per_meter)
    for x in range(0, MAP_SIZE, grid_1m):
        cv2.line(display, (x, 0), (x, MAP_SIZE), (50, 50, 50), 1)
    for y in range(0, MAP_SIZE, grid_1m):
        cv2.line(display, (0, y), (MAP_SIZE, y), (50, 50, 50), 1)
 
    # HUD
    cv2.putText(
        display,
        f"Scan: {count}/{SCANS}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (180, 180, 180),
        1,
    )
    cv2.putText(
        display,
        "Q to stop",
        (10, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (100, 100, 100),
        1,
    )
 
    # Scale bar
    bar_px = int(px_per_meter * 0.25)  # 25cm bar
    bar_y = MAP_SIZE - 20
    cv2.line(display, (10, bar_y), (10 + bar_px, bar_y), (80, 80, 80), 2)
    cv2.putText(
        display,
        "25cm",
        (10 + bar_px + 5, bar_y + 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (80, 80, 80),
        1,
    )
 
    return display
