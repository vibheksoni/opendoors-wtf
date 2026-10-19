"""Convert em dashes and clause commas to Vibhek's writing rules.

Skips fenced code blocks and inline code so only prose changes. Prints a count
per file so any silent miss shows up.
"""
import re
from pathlib import Path

BLOG = Path(__file__).resolve().parents[1] / "src" / "content" / "blog"
FILES = ["dma-hwid-spoofer.mdx", "ferrox-stealer-research.mdx"]


def split_code(text):
    """Return (prose_lines, code_flags) so code blocks are never rewritten."""
    flags = []
    inside = False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            flags.append(True)
            inside = not inside
            continue
        flags.append(inside)
    return flags


def fix_heading(line):
    """Join a heading that used an em dash as a separator."""
    match = re.match(r"^(#{1,6}) (.+?) — (.+)$", line)
    if not match:
        return line
    hashes, left, right = match.groups()
    return f"{hashes} {left} and {right[0].lower() + right[1:]}"


def fix_prose(line):
    """Turn label separators into periods and drop em dashes from prose."""
    line = re.sub(r"\*\*([^*]+?)\*\* — ", lambda m: f"**{m.group(1)}.** ", line)
    line = re.sub(r"^(\d+\. )(.+?) — ", lambda m: f"{m.group(1)}{m.group(2)}. ", line)
    line = re.sub(r"^(\t*)- (.+?) — ", lambda m: f"{m.group(1)}- {m.group(2)}. ", line)
    line = re.sub(r"(\w) — (\w)", lambda m: f"{m.group(1)}. {m.group(2).upper()}", line)
    line = re.sub(r"(\w)—(\w)", lambda m: f"{m.group(1)}. {m.group(2).upper()}", line)
    line = re.sub(r", (and|so|but|which) ", r" \1 ", line)
    return line


def process(path):
    """Rewrite one post and report the change count."""
    lines = path.read_text(encoding="utf-8").split("\n")
    code = split_code("\n".join(lines))
    changed = 0
    out = []
    for index, line in enumerate(lines):
        if code[index]:
            out.append(line)
            continue
        new = fix_heading(line)
        new = fix_prose(new)
        if new != line:
            changed += 1
        out.append(new)
    path.write_text("\n".join(out), encoding="utf-8")
    print(f"{path.name}: {changed} lines changed")


if __name__ == "__main__":
    for name in FILES:
        process(BLOG / name)
