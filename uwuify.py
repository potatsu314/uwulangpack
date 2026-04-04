#!python

import argparse
import json
import os
import sys
import zipfile
import re

import libuwuify.libuwuify as libuwuify

parser = argparse.ArgumentParser(prog="uwuify", description="converts minecraft localization to uwuified version")

parser.add_argument("-v", "--verbose", action="store_true", help="show some debug information")
parser.add_argument("-l", "--letters", action="store_true", help="change letters l, r to w")
parser.add_argument("-k", "--kaomojis", action="store_true", help="add kaomojis at the end of strings")
parser.add_argument("-s", "--stutter", action="store_true", help="add random stutters to words")
parser.add_argument("-q", "--squiggly", action="store_true", help="add random ~ to words")
parser.add_argument("-c", "--vocab", action="store_true", help="replace some words with predefined uwuified words")
parser.add_argument("-w", "--lowercase", action="store_true", help="change all letters to lowercase variants")
parser.add_argument("--texts", action="store_true", help="translate vanilla splash/end credits text too")
parser.add_argument("--pack-mcmeta", type=str, help="pack.mcmeta for a resource pack")
parser.add_argument("--pack-png", type=str, help="pack.png for a resource pack (pls make sure that it is a png)")
parser.add_argument("--language", type=str, help="language to translate from", default="en_us")
parser.add_argument("--asset-index", type=str, help="name of index.json in assets/indexes/ (29.json for example)")
parser.add_argument("--input", type=str, required=True, nargs="+", help="path to your en_us.json (only for vanilla) or .jar files (mods or minecraft version) or .zip files (resourcepacks) or assets folder in .minecraft")
parser.add_argument("--output", type=str, help="output path for resource pack", default="uwulang.zip")

args = parser.parse_args()

def parse_zip(path_archive: str) -> tuple[list[tuple[str, dict]], tuple[str | None, str | None]] | None:
    f = zipfile.ZipFile(path_archive, "r")
    files = f.namelist()
    
    ret = []

    for j in files:
        m = re.search(r"^assets/([^/]+)/lang/{}.json$".format(args.language), j)
        if m:
            try:
                j = json.loads(f.read(j).decode("utf-8"))
                ret.append((m.group(1), j))
            except Exception as e:
                if args.verbose: 
                    print(e)
                return None
    
    end = None
    splash = None
    if "assets/minecraft/texts/end.txt" in files:
        end = f.read("assets/minecraft/texts/end.txt").decode("utf-8")
    if "assets/minecraft/texts/splashes.txt" in files:
        splash = f.read("assets/minecraft/texts/splashes.txt").decode("utf-8")        

    f.close()
    return (ret, (end, splash))

def parse_assets(path: str, index_name: str) -> dict | None:
    index_file = json.load(open(os.path.join(path, "indexes", index_name), "r"))
    if f"minecraft/lang/{args.language}.json" not in index_file["objects"]:
        return None
    
    h = index_file["objects"][f"minecraft/lang/{args.language}.json"]["hash"]
    
    fp = os.path.join(path, "objects", h[0:2], h)

    return json.load(open(fp, "r"))

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

        if z is None:
            continue

        to_add.extend(z[0])

        if z[1][0] is not None:
            end = z[1][0]
        if z[1][1] is not None:
            splash = z[1][1]
    
    elif os.path.isdir(i) and os.path.exists(os.path.join(i, "indexes")) and os.path.exists(os.path.join(i, "objects")):
        a = parse_assets(i, args.asset_index)
        if a is not None:
            to_add.append(("minecraft", a))

    else:
        print(f"unsupported file format: {i}")
        continue

    for j in to_add:
        if j[0] not in locales:
            locales[j[0]] = {}
        
        locales[j[0]] |= j[1]

for i in locales.keys():
    for j in locales[i].keys():
        locales[i][j] = libuwuify.uwuify(locales[i][j], random_seed=j, lang_rules=libuwuify.LANG[args.language], use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab, use_lower_case=args.lowercase)

if len(locales) == 0:
    print("couldn't find any translation files")
    sys.exit()

f = zipfile.ZipFile(args.output, "w", zipfile.ZIP_DEFLATED, compresslevel=9)

if args.pack_mcmeta is not None:
    f.write(args.pack_mcmeta, "pack.mcmeta")
else:
    f.writestr("pack.mcmeta", json.dumps({
        "pack": {
            "pack_format": 15,
        },
        "language": {
            "en_us_uwu": {
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
    f.writestr(f"assets/{i}/lang/{args.language}_uwu.json", json.dumps(locales[i]))
if args.texts and (end is not None or splash is not None):
    def convert_multiline_string(inp: str) -> str:
        ret = []
        for i in inp.splitlines():
            if "PLAYERNAME" not in i:
                ret.append(libuwuify.uwuify(i, random_seed=i, use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab, use_lower_case=args.lowercase))
            else:
                s = i.split("PLAYERNAME")
                for i in range(len(s) - 1):
                    s[i] = libuwuify.uwuify(s[i], random_seed=s[i], use_letter_change=args.letters, use_kaomojis=False, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab, use_lower_case=args.lowercase)
                    
                s[-1] = libuwuify.uwuify(s[-1], random_seed=s[-1], use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab, use_lower_case=args.lowercase)
                ret.append("PLAYERNAME".join(s))
        return "\n".join(ret)
    
    f.mkdir("assets/minecraft/texts")
    if end is not None:
        f.writestr("assets/minecraft/texts/end.txt", convert_multiline_string(end))
    if splash is not None:
        f.writestr("assets/minecraft/texts/splashes.txt", convert_multiline_string(splash))
    
f.close()
