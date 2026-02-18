## Chess Blitz ELO Display

A compact, transparent desktop widget that shows your **Chess.com blitz rating** plus a **chess piece icon** that changes with your rating range.

### Features

- **Live Chess.com rating**: Fetches your latest blitz rating from the public Chess.com API.
- **Rating-based piece icon**:
  - \<1000: no piece
  - 1000–1199: pawn ♟
  - 1200–1399: bishop ♝
  - 1400–1599: knight ♞
  - 1600–1799: rook ♜
  - 1800–1999: queen ♛
  - 2000+: king ♚
- **Transparent, borderless window** that floats on your desktop.
- **Draggable**: Click and drag to reposition.
- **Auto-refresh**: Periodically re-fetches the rating.
- **Visual style**: Uses the same Mars-themed colors and font logic as the desktop clock widget.

### Requirements

- **OS**: Windows.
- **Python**: 3.x with Tkinter available.
- **Network**: Internet access to reach `api.chess.com`.

No external pip packages are required; this uses only the Python standard library (`tkinter`, `urllib`, `json`, `threading`).

### Project files

- **`main.py`**: Main Tkinter script for the widget.
  - Configuration section near the top:
    - `USERNAME = "eleegee"` – Chess.com username to query.
    - `REFRESH_SECONDS = 100` – How often to re-fetch the rating.
    - `BLITZ_KEY = "blitz"` – Chess.com stats section key (normally you don’t need to change this).
- **`run_elo.vbs`**: Windows Script Host launcher that runs `pythonw main.py` with **no console window**.

### Configuration

Open `main.py` and adjust:

- **`USERNAME`** to your Chess.com username, for example:

  ```python
  USERNAME = "your_chess_com_username"
  ```

- **`REFRESH_SECONDS`** to control how frequently the widget polls the API.

Save the file after making changes.

### Running the widget

- **Typical usage (no console window)**  
  Double‑click `run_elo.vbs` in Explorer.  
  This:
  - Sets the working directory to the script folder.
  - Runs `pythonw main.py` without opening a terminal window.

- **Debug / development mode (with console)**  
  From a terminal in `chess-blitz-elo-display`:

  ```bash
  python main.py
  ```

### Interaction and layout

- **Default position**: Small widget near the top-right of the primary screen.
- **Dragging**: Click and hold on the widget, then drag to move it.
- **Display**:
  - Left: chess piece icon representing your current rating tier.
  - Right: numeric blitz rating (or a dimmed placeholder when unavailable).

