import sys

import cv2
import ezdxf
import numpy as np

# input_ = sys.argv[1]

# print(input_)

input_filename = sys.argv[1]
output_filename = sys.argv[2]

img = cv2.imread(input_filename, cv2.IMREAD_GRAYSCALE)
img = img.astype(np.unit8)

_, binary = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY_INV)

contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

doc = ezdxf.new()
msp = doc.modelspace()

for contour in contours:
    if len(contour) < 3:
        continue
    pts = [(int(p[0][0]), int(p[0][1])) for p in contour]
    msp.add_lwpolyline(pts, close=True)

doc.saveas(output_filename)
print(f"Exported {output_filename}")
