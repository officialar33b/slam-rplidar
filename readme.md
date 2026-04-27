# RPLidar 2D SLAM Mapper

A simple Python tool that drives an RPLidar sensor, accumulates scans into a 2D occupancy-style canvas, displays a live preview with OpenCV, and saves the final map as a PNG.

## Features

- Live visualization of LiDAR scans as they are collected
- Frame-by-frame accumulation into a single grayscale canvas
- Configurable scan count, motor speed, and output paths
- Early-exit support via the `Q` key or `Ctrl+C`
- Automatic creation of the `output/` directory and timestamp-friendly file naming

## Hardware Requirements

- An RPLidar unit (A1 / A2 / A3 / S-series) supported by [`pyrplidar`](https://pypi.org/project/pyrplidar/)
- A USB-to-serial adapter (typically included with the RPLidar)
- A host machine running Linux, macOS, or Windows

## Software Requirements

- Python 3.8+
- The following Python packages:
  - `opencv-python`
  - `numpy`
  - `pyrplidar`

Install them with:

```bash
pip install opencv-python numpy pyrplidar
```

On Linux, make sure your user has permission to access the serial port (e.g. add yourself to the `dialout` group):

```bash
sudo usermod -aG dialout $USER
```

Then log out and back in.

## Project Structure

```
.
├── main.py              # The script shown above (entry point)
├── constants.py         # Configuration constants
├── live_red_feed.py     # draw_frame + make_display helpers
├── output/              # Auto-created; PNG maps are saved here
└── README.md
```

### `constants.py`

Defines the runtime configuration. Expected variables:

| Constant      | Description                                                   | Example          |
| ------------- | ------------------------------------------------------------- | ---------------- |
| `PORT`        | Serial port the LiDAR is connected to                         | `/dev/ttyUSB0`   |
| `BAUDRATE`    | Baud rate for the LiDAR (depends on model, e.g. A1 = 115200)  | `115200`         |
| `MAP_SIZE`    | Size in pixels of the square SLAM canvas                      | `800`            |
| `SCANS`       | Number of full scans to collect before stopping               | `200`            |
| `MIN_SAMPLES` | Minimum points per scan before it is accepted                 | `100`            |
| `OUTPUT_FILE` | Base filename (without extension) for the saved PNG map       | `room_scan`      |

### `live_red_feed.py`

Provides two helpers used by the main loop:

- `draw_frame(canvas, scan)` — projects a single scan onto the persistent canvas and returns the updated canvas.
- `make_display(canvas, scan, scan_index)` — produces a colorized display image (canvas + current scan overlay + scan counter) for the OpenCV window.

## Configuration

Before running, edit `constants.py` to match your setup. The most common change is `PORT`:

- Linux: usually `/dev/ttyUSB0`
- macOS: usually `/dev/tty.SLAB_USBtoUART` or similar
- Windows: usually `COM3`, `COM4`, etc.

The motor PWM is set in code (`lidar.set_motor_pwm(660)`). Adjust this if your model needs a different value — consult Slamtec's datasheet for your specific unit.

## Usage

1. Connect the RPLidar via USB and confirm it spins up.
2. Update `PORT` in `constants.py`.
3. Run the script:

   ```bash
   python main.py
   ```

4. A window titled **"SLAM map"** will open showing the live canvas.
5. Walk or rotate the LiDAR slowly around the area you want to map.
6. The script stops automatically once `SCANS` scans have been collected, or you can stop it early.

### Controls

| Key / Action | Effect                                          |
| ------------ | ----------------------------------------------- |
| `Q`          | Stop collection early and save the current map  |
| `Ctrl+C`     | Interrupt the script (still saves and cleans up)|

## Output

When the run finishes, a PNG named `<OUTPUT_FILE>.png` is written to the `output/` directory:

```
output/room_scan.png
```

The console will print confirmation:

```
saved room_scan
```

## How It Works (Brief)

1. A blank grayscale canvas (`MAP_SIZE × MAP_SIZE`, filled with `127`) is created.
2. The LiDAR is connected and the motor is started with a fixed PWM.
3. `lidar.force_scan()` yields measurements continuously. The script buffers them until a `start_flag` marks the beginning of a new revolution.
4. Each completed revolution (with at least `MIN_SAMPLES` points) is drawn onto the canvas via `draw_frame`.
5. `make_display` overlays the most recent scan and a counter for the live preview.
6. After `SCANS` revolutions — or an early exit — the LiDAR is stopped, the motor cut, and the canvas saved as a PNG.

## Troubleshooting

- **`SerialException: could not open port`** — wrong `PORT` value, or another process (e.g. a previous run) still has it open. Unplug/replug the LiDAR, or kill stale Python processes.
- **Permission denied on the serial port (Linux)** — add your user to the `dialout` group (see Software Requirements).
- **The motor doesn't spin** — try a higher PWM value (e.g. `1000`) or check that the LiDAR is getting enough power; a powered USB hub can help.
- **Empty / mostly-gray output** — increase `SCANS`, lower `MIN_SAMPLES`, or move the sensor more so it sees varied geometry.
- **Window doesn't update** — make sure the OpenCV window is focused when pressing `Q`; otherwise the keypress isn't captured.

## License

This project is licensed under the **GNU General Public License v2.0 (GPL-2.0)**.

You are free to use, modify, and redistribute it under the terms of the license. Any redistributed or derivative work must also be licensed under GPL-2.0 and include the original copyright and license notice.

See the [`LICENSE`](LICENSE) file for the full text, or read it online at <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html>.
