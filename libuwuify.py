import random
KAOMOJIS = [":3", "UwU", "OwO", ">w<", "~w~", "qwq", ">~<", ":3c", ">:3", ">:3c"]
VOCAB = {
    "love": "wuv",
    "Love": "Wuv",
    "friend": "fwend",
    "Friend": "Fwend",
    "good": "gud",
    "Good": "Gud",
    "what": "wut",
    "What": "Wut",
    "hand": "paw",
    "hands": "paws",
    "Hand": "Paw",
    "Hands": "Paws",
    "feet": "paws",
    "Feet": "Paws"
}

def uwuify(inp: str, *args, random_seed: str | int | float | None = None, use_letter_change: bool = True, use_kaomojis: bool = True, use_squiggly_lines: bool = False, use_stutter: bool = True, use_vocab: bool = True, use_lower_case: bool = False):
    if len(inp) == 0: return ""

    r = None

    if random_seed is not None:
        r = random.Random(random_seed)
    else:
        r = random
    
    if use_vocab:
        for i in VOCAB.keys():
            inp = inp.replace(i, VOCAB[i])
    if use_lower_case:
        inp = inp.lower()
    if use_letter_change:
        inp = inp.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
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
        inp = inp + " " + r.choice(KAOMOJIS)
    
    return inp

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        for i in sys.argv[1].splitlines():
            print(uwuify(i))