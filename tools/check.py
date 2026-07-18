#!/usr/bin/env python3
"""
Ding Lab website checks.

    python3 tools/check.py

Prints what's wrong in plain English and exits non-zero if anything is broken.
Runs automatically on every push (see .github/workflows/check.yml).

Why this exists: the site is hand-written HTML with a few invariants that would
otherwise break *silently* — the page would still load, it would just be wrong.
You do not need to remember these rules; this script remembers them for you.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
errors = []


def err(msg):
    errors.append(msg)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def pages():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))


def exists_exact(rel):
    """Case-sensitive existence check.

    macOS filesystems ignore case, but GitHub Pages serves from Linux where case
    matters — so `foo.JPG` referenced as `foo.jpg` works locally and 404s in
    production. This catches that before it ships.
    """
    cur = ROOT
    for part in rel.split("/"):
        try:
            if part not in os.listdir(cur):
                return False
        except (FileNotFoundError, NotADirectoryError):
            return False
        cur = os.path.join(cur, part)
    return True


def shared_block(html, name):
    m = re.search(
        r"<!-- =+ SHARED %s.*?-->(.*?)<!-- =+ /SHARED %s =+ -->" % (name, name),
        html,
        re.S,
    )
    return m.group(1) if m else None


# ---------------------------------------------------------------- checks

def check_shared_chrome():
    """Header/footer are copy-pasted onto every page and must stay identical."""
    for name in ("HEADER", "FOOTER"):
        seen = {}
        for p in pages():
            blk = shared_block(read(p), name)
            if blk is None:
                err(f"{p}: no SHARED {name} block found (did the marker comment get deleted?)")
                continue
            # aria-current legitimately differs per page; ignore it when comparing
            norm = re.sub(r'\s*aria-current="page"', "", blk)
            seen.setdefault(norm, []).append(p)
        if len(seen) > 1:
            groups = [", ".join(v) for v in seen.values()]
            err(
                f"The shared {name} is not identical across pages. Variants:\n"
                + "\n".join(f"      group {i+1}: {g}" for i, g in enumerate(groups))
                + f"\n      -> Pick the correct {name.lower()} and copy it into every page."
            )


def check_aria_current():
    """Exactly one nav link per page marks itself as the current page."""
    for p in pages():
        blk = shared_block(read(p), "HEADER") or ""
        marks = re.findall(r'<a href="([^"]+)"\s+aria-current="page">', blk)
        if len(marks) == 0:
            err(f'{p}: no nav link marked aria-current="page" (the active tab won\'t be shown).')
        elif len(marks) > 1:
            err(f'{p}: {len(marks)} nav links marked aria-current="page"; there must be exactly one.')
        elif marks[0] != p:
            err(f'{p}: aria-current="page" is on "{marks[0]}" but should be on "{p}".')


def check_internal_links():
    for p in pages():
        for target in sorted(set(re.findall(r'href="([A-Za-z0-9._-]+\.html)"', read(p)))):
            if not exists_exact(target):
                err(f"{p}: links to {target}, which does not exist.")


def check_images_exist():
    refs = {}
    for p in pages():
        for src in re.findall(r'src="(assets/img/[^"]+)"', read(p)):
            refs.setdefault(src, set()).add(p)
    css = "assets/css/style.css"
    for u in re.findall(r'url\("\.\./img/([^"]+)"\)', read(css)):
        refs.setdefault("assets/img/" + u, set()).add(css)
    for ref, where in sorted(refs.items()):
        if not exists_exact(ref):
            err(
                f"{ref} is referenced by {', '.join(sorted(where))} but no such file exists "
                f"(check spelling AND capitalisation — .JPG is not .jpg on GitHub Pages)."
            )


def check_asset_links():
    """Any href into assets/ (e.g. the CV download) must point at a real file."""
    for p in pages():
        for href in sorted(set(re.findall(r'href="(assets/[^"#?]+)"', read(p)))):
            if not exists_exact(href):
                err(
                    f"{p}: links to {href}, which does not exist "
                    f"(check spelling and capitalisation)."
                )


def check_img_alt():
    for p in pages():
        for tag in re.findall(r"<img\s[^>]*>", read(p)):
            if "alt=" not in tag:
                err(f"{p}: an <img> has no alt attribute -> {tag[:70]}...")


def check_marquee_sets():
    """The rolling gallery holds two identical photo sets; the loop jumps if they differ."""
    html = read("index.html")
    track = re.search(r'<div class="marquee-track">(.*?)\n    </div>', html, re.S)
    if not track:
        return  # gallery removed; nothing to check
    sets = re.findall(r'<div class="marquee-set"[^>]*>(.*?)</div>', track.group(1), re.S)
    if len(sets) != 2:
        err(f"index.html: rolling gallery has {len(sets)} .marquee-set block(s); expected exactly 2.")
        return

    def norm(s):
        s = re.sub(r"<!--.*?-->", "", s, flags=re.S)   # comments may differ
        s = re.sub(r'alt="[^"]*"', 'alt=""', s)        # 2nd set is decorative (empty alt)
        return re.findall(r'(?:src="([^"]*)"|<figcaption>([^<]*)</figcaption>)', s)

    if norm(sets[0]) != norm(sets[1]):
        err(
            "index.html: the two rolling-gallery sets differ, so the loop will visibly jump.\n"
            "      -> Every <figure> must appear in BOTH .marquee-set blocks, in the same order."
        )


# ------------------------------------------------------------------ main

def main():
    for fn in (
        check_shared_chrome,
        check_aria_current,
        check_internal_links,
        check_images_exist,
        check_asset_links,
        check_img_alt,
        check_marquee_sets,
    ):
        fn()

    n = len(pages())
    if errors:
        print(f"\n  {len(errors)} problem(s) found across {n} pages:\n")
        for e in errors:
            print(f"  ✗ {e}")
        print("\n  Nothing was changed. Fix the above and run again.\n")
        return 1

    print(f"\n  All checks passed ({n} pages).")
    print("  header/footer in sync · active nav correct · links & images resolve ·")
    print("  every image has alt text · gallery loop intact\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
