"""Translate OpenDoors posts into other languages with the Claude Code CLI.

usage: python scripts/translate.py [--langs es,pt,de,fr,ja] [--only slug] [--force] [--jobs 3]

Writes src/content/blog-i18n/<lang>/<slug>.mdx. Skips files that already exist
unless --force. Every result is checked so code blocks, imports, headings and
JSX tags survive unchanged before it is written.
"""
import argparse
import concurrent.futures
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "content" / "blog"
OUT = ROOT / "src" / "content" / "blog-i18n"
LANGS = {"es": "Spanish", "pt": "Brazilian Portuguese", "de": "German", "fr": "French", "ja": "Japanese"}

PROMPT = """Translate the MDX blog post below from English to {language}.

Rules:
- Output only the complete translated MDX file. No commentary and no code fence around the whole file.
- Keep the frontmatter block. Translate only the values of title and description. Copy every other frontmatter line exactly.
- Never change fenced code blocks, inline code in backticks, import lines, URLs, file paths, command line flags, numbers or byte values.
- Keep JSX and HTML tags exactly as they are, except translate the text inside alt="..." attributes.
- Keep product and project names in English: Bun, unbuned, Droid, Factory, Cline, Amp, Freebuff, JavaScriptCore, Claude Code, Ollama, LM Studio, OpenCode, Chrome, Rust, Python, IDA Pro, PatchGuard and similar.
- Keep the Markdown structure identical: same headings, lists, tables, bold and links. Translate link text but not link targets.
- Write natural, plain technical {language} the way a developer would write it. Keep the first person voice.

POST:
"""


def fences(text):
    return re.findall(r"```[\s\S]*?```", text)


def check(source, result):
    problems = []
    if not result.startswith("---"):
        problems.append("no frontmatter at start")
    if fences(source) != fences(result):
        problems.append("code blocks changed")
    src_imports = re.findall(r"^import .+$", source, re.M)
    if src_imports != re.findall(r"^import .+$", result, re.M):
        problems.append("imports changed")
    for level in ("## ", "### "):
        a = len(re.findall(rf"^{level}", source, re.M))
        b = len(re.findall(rf"^{level}", result, re.M))
        if a != b:
            problems.append(f"{level.strip()} count {a} vs {b}")
    if len(re.findall(r"<Image ", source)) != len(re.findall(r"<Image ", result)):
        problems.append("Image tags changed")
    for key in ("pubDate:", "tags:"):
        line = re.search(rf"^{key}.*$", source, re.M)
        if line and line.group(0) not in result:
            problems.append(f"{key} line changed")
    return problems


def finalize(result, lang, slug):
    result = result.strip() + "\n"
    result = result.replace("from '../../assets/", "from '../../../assets/")
    head, sep, body = result[3:].partition("\n---")
    head = head.rstrip("\n") + f"\nlang: {lang}\nsource: {slug}\n"
    return "---" + head + "---" + body


def translate(path, lang, force):
    slug = path.stem
    target = OUT / lang / f"{slug}.mdx"
    if target.exists() and not force:
        return f"skip {lang}/{slug}"
    source = path.read_text(encoding="utf-8")
    prompt = PROMPT.format(language=LANGS[lang]) + source
    for attempt in range(2):
        proc = subprocess.run(
            ["claude", "-p", "--model", "sonnet", "--output-format", "text"],
            input=prompt, capture_output=True, text=True, encoding="utf-8", timeout=900,
        )
        result = proc.stdout.strip()
        if result.startswith("```"):
            result = re.sub(r"^```[a-z]*\n|\n```$", "", result)
        problems = check(source, result) if proc.returncode == 0 else [f"exit {proc.returncode}: {proc.stderr[:200]}"]
        if not problems:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(finalize(result, lang, slug), encoding="utf-8")
            return f"ok   {lang}/{slug}"
    return f"FAIL {lang}/{slug}: {'; '.join(problems)}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default=",".join(LANGS))
    ap.add_argument("--only")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--jobs", type=int, default=3)
    args = ap.parse_args()
    posts = sorted(SRC.glob("*.mdx"))
    if args.only:
        posts = [p for p in posts if p.stem == args.only]
    tasks = [(p, lang) for p in posts for lang in args.langs.split(",")]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        for line in pool.map(lambda t: translate(t[0], t[1], args.force), tasks):
            print(line, flush=True)


if __name__ == "__main__":
    sys.exit(main())
