import tkinter as tk
from tkinter import font as tkfont
import urllib.request
import json
import threading

# ── CONFIG ──────────────────────────────────────────────────────────────────
USERNAME = "eleegee"   # ← Change this!
REFRESH_SECONDS = 100  # Auto-refresh interval
# ────────────────────────────────────────────────────────────────────────────

# Color scheme (matching desktop-clock-and-date/clock_widget.py)
MARS = "#c1440e"
MARS_BRIGHT = "#e85d1a"
DUST = "#d4835a"
PANEL = "#080a12"      # used as transparent key color
TEXT = "#f0ddd0"
TEXT_DIM = "#b8a89a"

BLITZ_KEY = "blitz"

def fetch_elo(username: str) -> dict:
    url = f"https://api.chess.com/pub/player/{username}/stats"
    req = urllib.request.Request(url, headers={"User-Agent": "ChessEloWidget/1.0"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())

    section = data.get(f"chess_{BLITZ_KEY}") or data.get(BLITZ_KEY)
    if section and "last" in section and "rating" in section["last"]:
        return int(section["last"]["rating"])
    raise ValueError("No blitz rating found.")


class ChessEloWidget(tk.Tk):
    def __init__(self):
        super().__init__()

        # Load fonts similarly to desktop-clock-and-date/clock_widget.py
        self.load_fonts()

        # Minimal transparent window: only pawn + rating
        self.title("Chess Blitz ELO")
        self.overrideredirect(True)
        self.configure(bg=PANEL)
        self.attributes("-transparentcolor", PANEL)
        self.resizable(False, False)

        # Default placement (top-right)
        window_width = 160
        window_height = 70
        screen_width = self.winfo_screenwidth()
        x_position = screen_width - window_width - 10
        y_position = 380
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Drag support
        self.offset_x = 0
        self.offset_y = 0
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)

        # UI: pawn + rating only
        self.rating_var = tk.StringVar(value="—")

        container = tk.Frame(self, bg=PANEL, highlightthickness=0)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.pawn_label = tk.Label(
            container,
            text="♚",
            font=(self.time_font, 28, "normal"),
            fg=MARS_BRIGHT,
            bg=PANEL
        )
        self.pawn_label.pack(side="left")

        self.rating_label = tk.Label(
            container,
            textvariable=self.rating_var,
            font=(self.time_font, 22, "normal"),
            fg=TEXT,
            bg=PANEL
        )
        self.rating_label.pack(side="left", padx=(10, 0))

        self.start_fetch()

    def load_fonts(self):
        """Load or find appropriate fonts for the widget (mirrors clock_widget.py)"""
        available_fonts = list(tkfont.families())

        # Try Orbitron first, then fall back
        if "Orbitron" in available_fonts:
            self.time_font = "Orbitron"
        else:
            orbitron_alternatives = ["Cascadia Mono", "Consolas", "Ubuntu Mono", "Courier New"]
            self.time_font = "Consolas"
            for font_name in orbitron_alternatives:
                if font_name in available_fonts:
                    self.time_font = font_name
                    break

    # ── Fetch in background thread ───────────────────────────────
    def start_fetch(self):
        threading.Thread(target=self._fetch_thread, daemon=True).start()

    def _fetch_thread(self):
        try:
            rating = fetch_elo(USERNAME)
            self.after(0, self._update_ui, rating, None)
        except Exception as e:
            self.after(0, self._update_ui, None, str(e))

    # ── Update UI on main thread ─────────────────────────────────
    def _update_ui(self, rating, error):
        if error or rating is None:
            self.rating_var.set("—")
            self.rating_label.config(fg=TEXT_DIM)
            # Default to pawn when no rating
            self.pawn_label.config(text="♟")
        else:
            self.rating_var.set(str(rating))
            self.rating_label.config(fg=TEXT)

            # Piece selection based on rating:
            # Pawn:   1000-1199
            # Bishop: 1200-1399
            # Knight: 1400-1599
            # Rook:   1600-1799
            # Queen:  1800-1999
            # King:   2000+
            if rating < 1000:
                piece = ""
            elif rating < 1200:
                piece = "♟"
            elif rating < 1400:
                piece = "♝"
            elif rating < 1600:
                piece = "♞"
            elif rating < 1800:
                piece = "♜"
            elif rating < 2000:
                piece = "♛"
            else:
                piece = "♚"

            self.pawn_label.config(text=piece)

        # Schedule next auto-refresh
        self.after(REFRESH_SECONDS * 1000, self.start_fetch)

    def start_drag(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def do_drag(self, event):
        x = self.winfo_x() + event.x - self.offset_x
        y = self.winfo_y() + event.y - self.offset_y
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = ChessEloWidget()
    app.mainloop()