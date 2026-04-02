import random
KAOMOJIS = [":3", "UwU", "OwO", ">w<", "~w~", "qwq", ">~<", ":3c", ">:3", ">:3c"]
VOCAB = {
    "love": "wuv",
    "friend": "fwiend",
    "good": "gud",
    "what": "wut"
}

def uwuify(inp: str, *args, use_letter_change: bool = True, use_kaomojis: bool = True, use_squiggly_lines: bool = True, use_stutter: bool = True, use_vocab: bool = True):
    if use_vocab:
        inp_tmp = inp.split(" ")

        for i in range(0, len(inp_tmp)):
            if inp_tmp[i].lower() in VOCAB:
                rep = VOCAB[inp_tmp[i].lower()]
                if inp_tmp[i][0].isupper():
                    rep = rep[0].upper() + rep[1:]
                inp_tmp[i] = rep
        
        inp = " ".join(inp_tmp)
        
        inp = " ".join(inp_tmp)
    if use_letter_change:
        inp = inp.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")
    if use_stutter:
        inp_tmp = inp.split(" ")

        for i in range(0, len(inp_tmp)):
            if inp_tmp[i].isalpha() and random.randint(0, 6) == 0:
                inp_tmp[i] = inp_tmp[i][0] + "-" + inp_tmp[i]
        
        inp = " ".join(inp_tmp)
    if use_squiggly_lines:
        inp_tmp = inp.split(" ")

        for i in range(0, len(inp_tmp)):
            if random.randint(0, 5) == 0:
                inp_tmp[i] += "~"

        inp = " ".join(inp_tmp)
    if use_kaomojis:
        inp = inp + " " + random.choice(KAOMOJIS)
    
    return inp

if __name__ == "__main__":
    print(uwuify("The quick brown fox jumps over the lazy dog. love and something yeah what good."))