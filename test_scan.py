from rplidar import RPLidar

lidar = RPLidar("/dev/ttyUSB0")
for scan in lidar.iter_scans():
    print(f"Points: {len(scan)}, sample: {scan[0]}")
    break
lidar.stop()
lidar.disconnect()
