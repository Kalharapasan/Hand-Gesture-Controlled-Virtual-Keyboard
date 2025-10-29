# Hand-Gesture-Controlled-Virtual-Keyboard

A simple project demonstrating a virtual keyboard controlled by hand gestures using MediaPipe and OpenCV.

## Features

- Real-time hand landmark detection via MediaPipe
- Virtual keyboard input (on-screen) controlled by finger gestures
- Designed to work with a standard webcam

## Requirements

- Python 3.10+
- See `requirements.txt` for pinned dependency versions. The repository includes a `venv_fixed/` example environment with many packages already installed.

## Quick setup (PowerShell)

```powershell
# Create a virtual environment (if you don't have one)
python -m venv venv
# Activate it in PowerShell
& .\venv\Scripts\Activate.ps1
# Install pinned dependencies
pip install -r requirements.txt
```

## Run

From the project root (with the virtualenv activated):

```powershell
python main.py
```

The application will open a webcam window and show hand landmarks; use the configured gestures to type using the virtual keyboard overlay.

## Notes

- `requirements.txt` in this repo contains pinned versions observed in `venv_fixed/Lib/site-packages`. If you need a different TensorFlow or OpenCV package (for GPU support or other reasons), adjust `requirements.txt` accordingly.
- If your camera is not detected, try changing the camera index in `main.py` or check permissions.

## License

This project is provided under the MIT License. Feel free to reuse and adapt the code.

## Contact

If you have questions or want to contribute, open an issue or pull request on the repository.

## How it works

Briefly, the project uses MediaPipe to detect hand landmarks (21 points per hand). The landmark coordinates are used to determine finger positions and simple gestures (for example: index-finger pointing to select keys, thumb/index pinch or distance threshold for "press" events). The overlayed keyboard is drawn with OpenCV and mapped to on-screen coordinates; when a press gesture is detected over a key, the project emits a virtual key press using the configured input method.

## Configuration

Common configuration options you may want to change (look for these in `main.py` or a config file if present):

- camera_index: integer (0 is usually the default webcam)
- detection_confidence: MediaPipe detection confidence threshold (float 0.0-1.0)
- tracking_confidence: MediaPipe tracking confidence threshold (float 0.0-1.0)
- keyboard_layout: list/array describing the on-screen keys and their positions
- press_distance_threshold: physical distance or normalized distance between landmarks used to detect a key press
- debounce_ms: how long to ignore repeated presses for a key (milliseconds)
- show_fps: toggle overlay FPS counter

If you add a small config object or JSON file, document keys and defaults so users can customise without editing source code.

## Example keyboard mapping

This project uses an on-screen grid of keys. A basic mapping might look like this (row-wise):

- Row 1: Q W E R T Y U I O P
- Row 2: A S D F G H J K L
- Row 3: Z X C V B N M
- Special keys: Backspace, Space, Enter

Modify the layout to suit your needs — larger keys or fewer keys make gesture typing easier.

## Troubleshooting

- No camera detected: ensure the camera is free (close other apps), check permissions, or try a different `camera_index`.
- Landmarks not detected reliably: increase lighting, move camera closer/further, or increase `detection_confidence`.
- Keys mis-triggering: tune `press_distance_threshold` and `debounce_ms`, or increase key sizes on-screen.
- Installation errors: create a fresh virtual environment and run `pip install -r requirements.txt`. If a package fails to install on Windows, check that you have an appropriate wheel for your Python version.

## Development

If you plan to modify the code:

1. Create and activate a virtualenv (see Quick setup above).
2. Install dev dependencies if any (none listed by default).
3. Run `main.py` and iterate.

Suggested small improvements to add as separate PRs:

- Unit tests for utility functions (gesture detection math, key mapping)
- Modularize the gesture recognition into a testable class
- Add a small GUI to change keyboard layout and thresholds at runtime

## Contributing

Contributions are welcome. Please:

1. Open an issue to discuss larger changes.
2. Fork the repository and create a branch for your work.
3. Keep changes small and focused; include tests where appropriate.
4. Send a pull request and reference the issue.

## Credits

- MediaPipe (hand landmark detection)
- OpenCV (video capture and drawing)
- Any third-party snippets or tutorials you've incorporated — please cite them in PRs.
