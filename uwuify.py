#!python

import argparse
import json
import os
import sys
import zipfile
import re

from libuwuify import uwuify

parser = argparse.ArgumentParser(prog="uwuify", description="converts minecraft english translation to english but uwu")

parser.add_argument("-v", "--verbose", action="store_true", help="show some debug information")
parser.add_argument("-l", "--letters", action="store_true", help="change letters l, r to w")
parser.add_argument("-k", "--kaomojis", action="store_true", help="add kaomojis at the end of strings")
parser.add_argument("-s", "--stutter", action="store_true", help="add random stutters to words")
parser.add_argument("-q", "--squiggly", action="store_true", help="add random ~ to words")
parser.add_argument("-c", "--vocab", action="store_true", help="replace some words with predefined uwuified words")
parser.add_argument("--texts", action="store_true", help="translate vanilla splash/end credits text too")
parser.add_argument("--pack-mcmeta", type=str, help="pack.mcmeta for a resource pack")
parser.add_argument("--pack-png", type=str, help="pack.png for a resource pack (pls make sure that it is a png)")
parser.add_argument("--input", type=str, required=True, nargs="+", help="path to your en_us.json (only for vanilla) or .jar files (mods or minecraft version) or .zip files (resourcepacks)")
parser.add_argument("--output", type=str, help="output path for resource pack", default="uwulang.zip")

args = parser.parse_args()

def parse_zip(ifp: str) -> tuple[list[tuple[str, dict]], tuple[str | None, str | None]]:
    f = zipfile.ZipFile(ifp, "r")
    files = f.namelist()
    
    ret = []
    alr = []

    for j in files:
        m = re.search(r"^assets/([^/]+)/lang/en_\w+.json$", j)
        if m and m.group(1) not in alr:
            alr.append(m.group(1))
            ret.append((m.group(1), json.loads(f.read(j).decode("utf-8"))))
    
    end = None
    splash = None
    if "assets/minecraft/texts/end.txt" in files:
        end = f.read("assets/minecraft/texts/end.txt").decode("utf-8")
    if "assets/minecraft/texts/splashes.txt" in files:
        splash = f.read("assets/minecraft/texts/splashes.txt").decode("utf-8")        

    f.close()
    return (ret, (end, splash))

locales = {}
end = None
splash = None

for i in args.input:
    if args.verbose: print(f"parsing {i}")
    if not os.path.exists(i):
        print(f"invalid file path: {i}")
        continue

    to_add = []

    if i.endswith(".json"):
        to_add.append(("minecraft", json.load(open(args.input, "r"))))

    elif i.endswith(".jar") or i.endswith(".zip"):
        z = parse_zip(i)
        to_add.extend(z[0])

        if z[1][0] is not None:
            end = z[1][0]
        if z[1][1] is not None:
            splash = z[1][1]

    else:
        print(f"unsupported file format: {i}")
        continue

    for j in to_add:
        if j[0] not in locales:
            locales[j[0]] = {}
        
        locales[j[0]] |= j[1]

for i in locales.keys():
    for j in locales[i].keys():
        locales[i][j] = uwuify(locales[i][j], random_seed=j, use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab)

if len(locales) == 0:
    print("couldn't find any translation files")
    sys.exit()

f = zipfile.ZipFile(args.output, "w")

if args.pack_mcmeta is not None:
    f.write(args.pack_mcmeta, "pack.mcmeta")
else:
    f.writestr("pack.mcmeta", json.dumps({
        "pack": {
            "pack_format": 15,
        },
        "language": {
            "en_uwu": {
                "name": "Engwish~ :3",
                "region": "Furry",
                "bidirectional": False
            }
        }
    }, indent=2))

if args.pack_png is not None:
    f.write(args.pack_png, "pack.png")

f.mkdir("assets")
for i in locales.keys():
    f.mkdir(f"assets/{i}")
    f.mkdir(f"assets/{i}/lang")
    f.writestr(f"assets/{i}/lang/en_uwu.json", json.dumps(locales[i]))
if args.texts and (end is not None or splash is not None):
    def convert_multiline_string(inp: str) -> str:
        return "\n".join([uwuify(x, random_seed=x, use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab) for x in inp.splitlines()])
    
    f.mkdir("assets/minecraft/texts")
    if end is not None:
        f.writestr("assets/minecraft/texts/end.txt", convert_multiline_string(end))
    if splash is not None:
        f.writestr("assets/minecraft/texts/splashes.txt", convert_multiline_string(splash))
    
f.close()
