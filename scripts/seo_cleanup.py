"""Final SEO cleanups: hreflang reciprocity, long descriptions and long alt text."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGES = ROOT / "src" / "pages"
BLOG = ROOT / "src" / "content" / "blog"
I18N = ROOT / "src" / "content" / "blog-i18n"

# 1. The English post list must point at every translation so the pairs are reciprocal.
path = PAGES / "blog" / "index.astro"
text = path.read_text(encoding="utf-8")
if "alternates=" not in text:
    anchor = "const description = `All ${posts.length} OpenDoors writeups by ${siteConfig.author.name}"
    assert anchor in text
    text = text.replace(
        anchor,
        "const alternates = [\n"
        "\t{ lang: 'en' as const, href: `${siteConfig.site}/blog/` },\n"
        "\t...(['es', 'pt', 'de', 'fr', 'ja'] as const).map((code) => ({\n"
        "\t\tlang: code,\n"
        "\t\thref: `${siteConfig.site}/${code}/blog/`,\n"
        "\t})),\n"
        "];\n" + anchor,
        1,
    )
    text = text.replace(
        '<BaseHead title="Blog" description={description} jsonLd={jsonLd} />',
        '<BaseHead title="Blog" description={description} alternates={alternates} jsonLd={jsonLd} />',
        1,
    )
    path.write_text(text, encoding="utf-8")
    print("blog index: alternates added")

# 2. Tag pages: a short description instead of every post title.
path = PAGES / "tags" / "[tag].astro"
text = path.read_text(encoding="utf-8")
old = (
    "const description = `${posts.length} ${posts.length === 1 ? 'writeup' : 'writeups'} "
    "on ${tag} by ${siteConfig.author.name}: ${posts.map((post) => post.data.title).join('; ')}.`;"
)
new = (
    "const description = `OpenDoors writeups on ${tag} by ${siteConfig.author.name}. "
    "${posts.length} ${posts.length === 1 ? 'post' : 'posts'} on reverse engineering, "
    "security research and backend engineering.`;"
)
if old in text:
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("tag pages: description shortened")

# 3. Only append the site name to a title when the result still fits a result snippet.
path = ROOT / "src" / "components" / "BaseHead.astro"
text = path.read_text(encoding="utf-8")
old = "const pageTitle = title === SITE_TITLE ? SITE_TITLE : `${title} | ${siteConfig.title}`;"
new = (
    "const brandedTitle = `${title} | ${siteConfig.title}`;\n"
    "const pageTitle = title === SITE_TITLE ? SITE_TITLE : brandedTitle.length <= 65 ? brandedTitle : title;"
)
if old in text:
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print("title template: trimmed when too long")

# 4. Keep alt text under 150 characters.
ALTS = {
    "stealth-browser-mcp.mdx": [
        (
            'alt="Diagram showing an AI agent talking to the stealth-browser-mcp FastMCP '
            'server over stdio JSON-RPC, which drives a real Chrome over CDP, with the stdout '
            'guard, trusted input, network tools and element cloning modules listed underneath"',
            'alt="Diagram of the agent to FastMCP server to real Chrome path over stdio and CDP, '
            'with the main modules underneath"',
        ),
        (
            'alt="Screenshot of the Augment Code hero section rebuilt as a clone, with the '
            'original headline, layout and styling reproduced in HTML"',
            'alt="The Augment Code hero rebuilt as a clone, with the original headline, '
            'layout and styling"',
        ),
    ],
    "unbuned-bun-executables.mdx": [
        (
            'alt="Diagram of the .bun section showing the length header, the JavaScript "'
            'modules, the embedded data, then the file table, the 32 byte Offsets struct '
            'and the trailer marker at the very end"',
            'alt="Layout of the .bun section from the length header through the modules '
            'and the file table to the trailer marker"',
        ),
        (
            'alt="Windows Explorer showing the droid modules folder unbuned wrote, with files '
            'named 0000-chunk-m0vzr57a.js through 0030-chunk-s3q890qc.js and 0008-droid.js"',
            'alt="Explorer showing the droid modules folder unbuned wrote, with the chunk '
            'files named from the module graph"',
        ),
    ],
    "security-risks-of-fully-ai-written-apps.mdx": [
        (
            'alt="Diagram of a five step review loop between a person and an AI agent. '
            'You ask, the AI drafts, you read the diff, you push back and the checks pass '
            'before it ships. A return arrow sends a rejected draft back to the AI to try again."',
            'alt="A five step review loop between a person and an AI agent, with a rejected '
            'draft going back for another try"',
        ),
    ],
}
for name, pairs in ALTS.items():
    path = BLOG / name
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
        else:
            print("alt not found in", name, old[:50])
    path.write_text(text, encoding="utf-8")
print("english alt text trimmed")

# Same for every translation, matched loosely on the long diagram alts.
count = 0
for path in I18N.glob("*/*.mdx"):
    text = path.read_text(encoding="utf-8")
    def shorten(match):
        inner = match.group(1)
        if len(inner) <= 150:
            return match.group(0)
        cut = inner[:147].rsplit(" ", 1)[0]
        return f'alt="{cut}"'
    new = re.sub(r'alt="([^"]*)"', shorten, text)
    if new != text:
        path.write_text(new, encoding="utf-8")
        count += 1
print("translation alt text trimmed in", count, "files")

# 5. Two descriptions were still long enough to be cut off in results.
LONG = {
    "ferrox-stealer-research.mdx": (
        "How Ferrox, a Rust Windows stealer, uses Hell's Gate syscalls, polymorphic builds "
        "and a Chrome App-Bound Encryption bypass. Analyzed in an isolated VM.",
        "How Ferrox, a Rust stealer, uses Hell's Gate syscalls, polymorphic builds and "
        "a Chrome App-Bound bypass. Analyzed in an isolated VM.",
    ),
    "dma-hwid-spoofer.mdx": (
        "How I reverse engineered Windows 11 kernel drivers in IDA Pro to build a DMA "
        "hardware ID spoofer in Rust, covering PatchGuard, DSE, SMBIOS and 12 spoofing modules.",
        "How I reversed Windows 11 kernel drivers in IDA Pro to build a DMA hardware ID "
        "spoofer in Rust, covering PatchGuard, DSE and SMBIOS.",
    ),
    "claude-code-webui-security.mdx": (
        "A security analysis of open-source web UIs for Claude Code. Finding unauthenticated "
        "RCE, path traversal, and client-side auth bypasses in community projects.",
        "A security analysis of open-source web UIs for Claude Code, with unauthenticated "
        "RCE, path traversal and client-side auth bypasses.",
    ),
}
for name, (old, new) in LONG.items():
    path = BLOG / name
    text = path.read_text(encoding="utf-8")
    if old in text:
        path.write_text(text.replace(old, new), encoding="utf-8")
        print("description shortened:", name)
