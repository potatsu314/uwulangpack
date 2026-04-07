import random
import typing
import os
import json

class LangRules(typing.TypedDict):
    vocab: dict[str, str]
    letter_replacements: dict[str, str]
    kaomojis: list[str]

class Lang:
    def __init__(self) -> None:
        self.s: dict[str, LangRules] = {}

        for i in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang-rules")):
            if os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang-rules", i)):
                self.s[i.removesuffix(".json")] = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang-rules", i), "r"))
    
    def __getitem__(self, key: str) -> LangRules:
        if key not in self.s:
            return self.s["en_us"]
        return self.s[key]

LANG = Lang()

def uwuify(inp: str, *args, random_seed: str | int | float | None = None, lang_rules: LangRules = LANG["en_us"], use_letter_change: bool = True, use_kaomojis: bool = True, use_squiggly_lines: bool = False, use_stutter: bool = True, use_vocab: bool = True, use_lower_case: bool = False):
    if len(inp) == 0: return ""

    r = None

    if random_seed is not None:
        r = random.Random(random_seed)
    else:
        r = random
    
    if use_vocab:
        for i in lang_rules["vocab"].keys():
            inp = inp.replace(i, lang_rules["vocab"][i])
    if use_lower_case:
        inp = inp.lower()
    if use_letter_change:
        for i in lang_rules["letter_replacements"].keys():
            inp = inp.replace(i, lang_rules["letter_replacements"][i])
    if use_stutter:
        inp_tmp = inp.split(" ")

        for i in range(0, len(inp_tmp)):
            if inp_tmp[i].isalpha() and r.randint(0, 6) == 0:
                inp_tmp[i] = inp_tmp[i][0] + "-" + inp_tmp[i]
        
        inp = " ".join(inp_tmp)
    if use_squiggly_lines:
        inp_tmp = inp.split(" ")

        for i in range(0, len(inp_tmp)):
            if r.randint(0, 5) == 0:
                inp_tmp[i] += "~"

        inp = " ".join(inp_tmp)
    if use_kaomojis:
        inp = inp + " " + r.choice(lang_rules["kaomojis"])
    
    return inp

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        for i in sys.argv[1].splitlines():
            print(uwuify(i, lang_rules=LANG[sys.argv[2]]))