"""Generate OpenDoors post diagrams as SVG files in src/assets/diagrams/.

usage: python scripts/diagrams.py

All diagrams share one style: near-black panel, thin borders, orange for the
part that matters and mono labels.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parents[1] / "src" / "assets" / "diagrams"

BG = "#0b0b0c"
PANEL = "#141416"
BORDER = "#2b2b30"
TEXT = "#ededed"
MUTED = "#a1a1aa"
DIM = "#8a8a93"
ACCENT = "#f97316"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"


class Svg:
    """One SVG document builder with a shared visual style."""

    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.parts = []

    def rect(self, x, y, w, h, fill=PANEL, stroke=BORDER, rx=10, sw=1.5):
        """Draw a rounded panel."""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def text(self, x, y, value, size=18, color=TEXT, font=SANS, weight=400, anchor="start"):
        """Draw one line of text."""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}">{escape(value)}</text>'
        )

    def box(self, x, y, w, h, title, lines=(), stroke=BORDER, title_color=TEXT):
        """Draw a panel with a centered title and mono detail lines."""
        self.rect(x, y, w, h, stroke=stroke)
        self.text(x + w / 2, y + 34, title, size=19, color=title_color, weight=600, anchor="middle")
        for index, line in enumerate(lines):
            self.text(x + w / 2, y + 62 + index * 23, line, size=14, color=MUTED, font=MONO, anchor="middle")

    def arrow(self, x1, y1, x2, y2, label="", color=MUTED, label_dy=-10):
        """Draw an arrow with an optional label at its midpoint."""
        marker = "arrow-accent" if color == ACCENT else "arrow"
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#{marker})"/>'
        )
        if label:
            self.text((x1 + x2) / 2, (y1 + y2) / 2 + label_dy, label, size=13, color=DIM, font=MONO, anchor="middle")

    def render(self):
        """Return the finished SVG document."""
        markers = "".join(
            f'<marker id="{name}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>'
            for name, color in (("arrow", MUTED), ("arrow-accent", ACCENT))
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
            f'viewBox="0 0 {self.width} {self.height}" role="img" aria-label="{escape(self.title)}">'
            f"<title>{escape(self.title)}</title><defs>{markers}</defs>"
            f'<rect width="100%" height="100%" rx="14" fill="{BG}"/>'
            + "".join(self.parts)
            + "</svg>\n"
        )


def stealth_browser_architecture():
    """Draw the agent to server to browser path and the four main subsystems."""
    s = Svg(1200, 520, "How stealth-browser-mcp connects an AI agent to a real Chrome browser")
    s.text(40, 52, "How a tool call reaches the browser", size=24, weight=700)
    s.text(40, 82, "stealth-browser-mcp sits between your MCP client and a real Chrome, Edge or Chromium", size=15, color=MUTED)

    s.box(40, 130, 230, 150, "AI agent", ["Claude Code", "Cursor or Codex", "any MCP client"])
    s.box(420, 130, 330, 150, "stealth-browser-mcp", ["FastMCP server", "101 tools in 11 sections", "or 21 with --minimal"], stroke=ACCENT, title_color=ACCENT)
    s.box(880, 130, 280, 150, "Real browser", ["Chrome, Edge or Chromium", "launched through nodriver", "driven over CDP"])

    s.arrow(272, 190, 418, 190, "stdio JSON-RPC")
    s.arrow(418, 232, 274, 232, "tool results", label_dy=22)
    s.arrow(752, 190, 878, 190, "CDP commands")
    s.arrow(878, 232, 754, 232, "page events", label_dy=22)

    modules = [
        ("stdout guard", "keeps JSON-RPC clean"),
        ("trusted input", "real mouse and key events"),
        ("network tools", "requests, responses, hooks"),
        ("element cloning", "styles, DOM and assets"),
    ]
    for index, (name, note) in enumerate(modules):
        x = 40 + index * 285
        s.rect(x, 340, 265, 110)
        s.text(x + 20, 380, name, size=17, weight=600)
        s.text(x + 20, 410, note, size=14, color=MUTED, font=MONO)
    s.text(40, 490, "Every tool runs inside the server process so the agent only ever sends and receives JSON", size=14, color=DIM)
    return s


def unbuned_section_layout():
    """Draw the .bun section order and the three steps that read it backwards."""
    s = Svg(1200, 430, "Layout of the .bun section inside a Bun executable")
    s.text(40, 52, "Inside the .bun section", size=24, weight=700)
    s.text(40, 82, "Bun writes the app first and a table describing it at the very end", size=15, color=MUTED)

    top = 260
    blocks = [
        (40, 70, "len", "8 B", BORDER),
        (110, 360, "JavaScript modules", "// @bun headers, NUL separated", BORDER),
        (470, 250, "Embedded data", "source maps, bytecode, assets", BORDER),
        (720, 200, "File table", "52 B per file", ACCENT),
        (920, 120, "Offsets", "32 B", ACCENT),
        (1040, 120, "Trailer", "16 B", ACCENT),
    ]
    for x, w, title, note, stroke in blocks:
        s.rect(x, top, w, 100, stroke=stroke)
        color = ACCENT if stroke == ACCENT else TEXT
        s.text(x + w / 2, top + 44, title, size=17 if w > 100 else 15, weight=600, anchor="middle", color=color)
        s.text(x + w / 2, top + 72, note, size=13, color=MUTED, font=MONO, anchor="middle")

    def arc(x1, x2, height, label):
        """Draw one labelled arc from a block to the block it points at."""
        mid = (x1 + x2) / 2
        s.parts.append(
            f'<path d="M {x1} {top - 4} Q {mid} {top - 4 - height * 2} {x2} {top - 6}" fill="none" '
            f'stroke="{ACCENT}" stroke-width="2" marker-end="url(#arrow-accent)"/>'
        )
        s.text(mid, top - 10 - height, label, size=13, color=TEXT, font=MONO, anchor="middle")

    arc(1100, 985, 22, "1. step back 32 B")
    arc(960, 830, 52, "2. Offsets points at the table")
    arc(800, 290, 90, "3. every record points at a module and its real name")
    s.text(1100, top + 128, r'"\n---- Bun! ----\n"', size=13, color=ACCENT, font=MONO, anchor="middle")
    s.text(40, top + 128, "read it backwards: trailer, then Offsets, then the file table", size=14, color=DIM)
    return s


def ai_review_loop():
    """Draw the five step loop a person and an AI agent run before shipping."""
    s = Svg(1200, 430, "A review loop for working with an AI coding agent")
    s.text(40, 52, "You stay the lead engineer", size=24, weight=700)
    s.text(40, 82, "The AI writes fast. Nothing ships until a person has read it and the checks pass", size=15, color=MUTED)

    steps = [
        ("1", "You ask", ["clear task", "known limits"]),
        ("2", "AI drafts", ["code and", "a short plan"]),
        ("3", "You read the diff", ["what changed", "what got removed"]),
        ("4", "You push back", ["ask why", "ask for a fix"]),
        ("5", "Checks pass", ["tests, auth", "input validation"]),
    ]
    width, gap, top = 196, 40, 140
    for index, (num, title, lines) in enumerate(steps):
        x = 40 + index * (width + gap)
        stroke = ACCENT if index in (2, 3) else BORDER
        s.rect(x, top, width, 160, stroke=stroke)
        s.text(x + 20, top + 36, num, size=15, color=ACCENT, font=MONO, weight=700)
        s.text(x + width / 2, top + 72, title, size=18, weight=600, anchor="middle")
        for line_index, line in enumerate(lines):
            s.text(x + width / 2, top + 104 + line_index * 23, line, size=14, color=MUTED, font=MONO, anchor="middle")
        if index < len(steps) - 1:
            s.arrow(x + width + 2, top + 80, x + width + gap - 2, top + 80)

    s.parts.append(
        f'<path d="M 866 302 C 866 370, 394 370, 394 304" fill="none" stroke="{ACCENT}" stroke-width="2" marker-end="url(#arrow-accent)"/>'
    )
    s.text(630, 392, "not good enough yet, the AI tries again", size=14, color=ACCENT, font=MONO, anchor="middle")
    s.text(1160, 392, "then it ships", size=14, color=MUTED, font=MONO, anchor="end")
    return s


def main():
    """Write every diagram to src/assets/diagrams."""
    OUT.mkdir(parents=True, exist_ok=True)
    diagrams = {
        "stealth-browser-architecture.svg": stealth_browser_architecture(),
        "unbuned-section-layout.svg": unbuned_section_layout(),
        "ai-review-loop.svg": ai_review_loop(),
    }
    for name, svg in diagrams.items():
        (OUT / name).write_text(svg.render(), encoding="utf-8")
        print("wrote", name)


if __name__ == "__main__":
    main()
