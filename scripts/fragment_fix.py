"""Repair the sentence fragments the em dash conversion left behind."""
from pathlib import Path

BLOG = Path(__file__).resolve().parents[1] / "src" / "content" / "blog"

FIXES = {
    "dma-hwid-spoofer.mdx": [
        (
            "Covering PatchGuard, DSE, SMBIOS and 12 spoofing modules.",
            "It covers PatchGuard, DSE, SMBIOS and 12 spoofing modules.",
        ),
        (
            "Supporting other builds would require extracting their offsets. Which is why the project is open-source.",
            "Supporting other builds would require extracting their offsets so that is why the project is open-source.",
        ),
        ("### Disk Serials and nVME, RAID, CLASSPNP", "### Disk Serials From NVMe, RAID and CLASSPNP"),
        (
            "The DXGKRNL approach required reversing how the display kernel caches EDID blocks. Finding the adapter objects and their associated EDID buffers in memory.",
            "The DXGKRNL approach required reversing how the display kernel caches EDID blocks so I had to find the adapter objects and their associated EDID buffers in memory.",
        ),
        (
            "without allocating new pages. Which would be suspicious. Instead, it finds",
            "without allocating new pages because a fresh allocation would be suspicious. Instead it finds",
        ),
        (
            "- **Tooling.** `cargo` just works. Building, dependency management, cross-compilation. it's all smoother than wrestling with CMake or Visual Studio project files.",
            "- **Tooling.** `cargo` just works. Building, dependency management and cross-compilation are all smoother than wrestling with CMake or Visual Studio project files.",
        ),
    ],
}

for name, pairs in FIXES.items():
    path = BLOG / name
    text = path.read_text(encoding="utf-8")
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
        else:
            print("NOT FOUND", old[:70])
    path.write_text(text, encoding="utf-8")
print("done")
