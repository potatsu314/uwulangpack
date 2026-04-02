#!/bin/python

import argparse
import json
import os
import sys
import zipfile

from libuwuify import uwuify

parser = argparse.ArgumentParser(prog="uwuify", description="converts minecraft english translation to english but uwu")

parser.add_argument("-v", "--verbose", action="store_true", help="show some debug information")
parser.add_argument("-l", "--letters", action="store_true", help="TODO")
parser.add_argument("-k", "--kaomojis", action="store_true", help="use kaomojis at the end of strings")
parser.add_argument("-s", "--stutter", action="store_true", help="TODO")
parser.add_argument("-q", "--squiggly", action="store_true", help="TODO")
parser.add_argument("-c", "--vocab", action="store_true", help="TODO")
parser.add_argument("--pack-mcmeta", type=str, help="pack.mcmeta for a resource pack")
parser.add_argument("--pack-png", type=str, help="pack.png for a resource pack (pls make sure that it is a png)")
parser.add_argument("--input", type=str, required=True, nargs="+", help="path to your en_us.json (only for vanilla) or .jar files (mods or minecraft version) or .zip files (resourcepacks)")
parser.add_argument("--output", type=str, help="output path for resource pack", default="uwulang.zip")

args = parser.parse_args()

def parse_zip(ifp: str):
    f = zipfile.ZipFile(ifp, "r")
    files = f.namelist()
    
    fp = None
    for j in files:
        if j.endswith("lang/en_us.json"): # TODO: make it better or smth
            fp = j
            break
    
    if fp is None:
        if args.verbose: print(f"could not find en_us.json in {i}") 
        return None

    inp_lang = json.loads(f.read(fp).decode("utf-8"))
    inp_name = fp.removeprefix("assets/").removesuffix("/lang/en_us.json").strip()
    f.close()
    return (inp_lang, inp_name)

locales = {}

for i in args.input:
    if not os.path.exists(i):
        if args.verbose: print(f"invalid file path: {i}")
        continue

    inp_lang = None
    inp_name = None

    if i.endswith(".json"):
        inp_lang = json.load(open(args.input, "r"))
        inp_name = "minecraft"

    elif i.endswith(".jar") or i.endswith(".zip"):
        z = parse_zip(i)

        if z is None:
            continue

        inp_lang = z[0]
        inp_name = z[1]
    else:
        if args.verbose: print(f"unsupported file format: {i}")
        continue

    if inp_lang is None or inp_name is None:
        if args.verbose: print(f"couldn't parse file: {i}")
        continue

    out = {}

    for i in inp_lang.keys():
        out[i] = uwuify(inp_lang[i], use_letter_change=args.letters, use_kaomojis=args.kaomojis, use_squiggly_lines=args.squiggly, use_stutter=args.stutter, use_vocab=args.vocab)

    if len(out) > 0:
        locales[inp_name] = out

if len(locales) == 0:
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
f.close()
