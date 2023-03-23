from keyword import kwlist
import builtins


def findOccurrences(s, lst: list = None, word: bool = True):
    if lst is None:
        lst = []
    end = 0
    out = []
    if word:
        for i in lst:
            end = 0
            while True:
                start = s.find(i, end)
                end = start + len(i)
                if start == -1:
                    break
                else:
                    checks = []
                    if start != 0:
                        checks.append(s[start - 1].isidentifier() or s[start - 1].isnumeric())
                    if end != len(s):
                        checks.append(s[end].isidentifier())
                    if True not in checks:
                        out.append((start, end))
    else:
        for j in s:
            if j in lst:
                end = s.index(j, end) + 1
                out.append((end - 1, end))
    return out


findFirstWordstop = lambda s: len(s.split(" ")[0].split("(")[0].split(")")[0].split("#")[0].split(":")[0])


def color(text):
    for tag in text.tag_names():
        text.tag_delete(tag)

    inp = text.get("1.0", "end-1c")
    count = 0

    # numbers
    lst = findOccurrences(inp, ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"], word=False)
    for i in lst:
        text.tag_add(str(count), f"1.0+{i[0]}c", f"1.0+{i[1]}c")
        text.tag_config(str(count), foreground="blue")
        count += 1

    # comments
    lst = findOccurrences(inp, ["#"], word=False)
    for i in lst:
        text.tag_add(str(count), f"1.0+{i[0]}c", f"1.0+{i[1]}c lineend")
        text.tag_config(str(count), foreground="grey", font="arial 11 italic")
        count += 1
        if "TODO" in text.get(f"1.0+{i[1]}c", f"1.0+{i[1]}c lineend"):
            text.tag_add(str(count), f"1.0+{inp.index('TODO', i[1])}c", f"1.0+{inp.index('TODO', i[1])}c lineend")
            text.tag_config(str(count), foreground="#55AAFF")
            count += 1

    # builtin keywords
    lst = findOccurrences(inp, list(kwlist))
    for j in lst:
        text.tag_add(str(count), f"1.0+{j[0]}c", f"1.0+{j[1]}c")
        text.tag_config(str(count), foreground="#cb0", font="arial 11 bold")
        count += 1

    # builtin functions
    lst = findOccurrences(inp, dir(builtins))
    for j in lst:
        text.tag_add(str(count), f"1.0+{j[0]}c", f"1.0+{j[1]}c")
        text.tag_config(str(count), foreground="#cb0", font="arial 11 bold")
        count += 1

    # strings option 1
    lst = findOccurrences(inp, ['"'], word=False)
    while not len(lst) < 1:
        if len(lst) == 1:
            text.tag_add(str(count), f"1.0+{lst[0][0]}c", f"1.0+{lst[0][1]}c lineend")
            text.tag_config(str(count), foreground="green", font="arial 11")
            del lst[0]
        else:
            text.tag_add(str(count), f"1.0+{lst[0][0]}c", f"1.0+{lst[1][1]}c")
            text.tag_config(str(count), foreground="green", font="arial 11")
            del lst[0], lst[0]
        count += 1

    # strings option 2
    lst = findOccurrences(inp, ["'"], word=False)
    while not len(lst) <= 1:
        text.tag_add(str(count), f"1.0+{lst[0][0]}c", f"1.0+{lst[1][1]}c")
        text.tag_config(str(count), foreground="green", font="arial 11")
        del lst[0], lst[0]
        count += 1

    # names of function and class definition
    lst = findOccurrences(inp, ["def", "class"])
    for i in lst:
        line = text.get(f"1.0+{i[1]}c", f"1.0+{i[1]}c lineend").split(" ")
        for j in line:
            if len(j) > 0:
                if j[0].isalpha() or j[0] == "_":
                    text.tag_add(str(count), f"1.0+{inp.index(j, i[1])}c", f"1.0+{inp.index(j, i[1])+len(j[0:findFirstWordstop(j)])}c")
                    text.tag_config(str(count), foreground="#f77")
                    count += 1
                break

    # ()
    if text.get("insert" + "-1c", "insert") == "(":
        opening = inp.find("(", len(text.get("1.0", "insert")) - 1)
        closing = inp.find(")", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert" + "-1c", "insert") == ")":
        closing = inp.find(")", len(text.get("1.0", "insert")) - 1)
        opening = inp.rfind("(", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == "(":
        opening = inp.find("(", len(text.get("1.0", "insert")))
        closing = inp.find(")", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == ")":
        closing = inp.find(")", len(text.get("1.0", "insert")))
        opening = inp.rfind("(", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    # []
    if text.get("insert" + "-1c", "insert") == "[":
        opening = inp.find("[", len(text.get("1.0", "insert")) - 1)
        closing = inp.find("]", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert" + "-1c", "insert") == "]":
        closing = inp.find("]", len(text.get("1.0", "insert")) - 1)
        opening = inp.rfind("[", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == "[":
        opening = inp.find("[", len(text.get("1.0", "insert")))
        closing = inp.find("]", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == "]":
        closing = inp.find("]", len(text.get("1.0", "insert")))
        opening = inp.rfind("[", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    # {}
    if text.get("insert" + "-1c", "insert") == "{":
        opening = inp.find("{", len(text.get("1.0", "insert")) - 1)
        closing = inp.find("}", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert" + "-1c", "insert") == "}":
        closing = inp.find("}", len(text.get("1.0", "insert")) - 1)
        opening = inp.rfind("{", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == "{":
        opening = inp.find("{", len(text.get("1.0", "insert")))
        closing = inp.find("}", opening)
        if closing != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")

    elif text.get("insert", "insert" + "+1c") == "}":
        closing = inp.find("}", len(text.get("1.0", "insert")))
        opening = inp.rfind("{", 0, closing)
        if opening != -1:
            text.tag_add("opening bracket", f"1.0+{opening}c", f"1.0+{opening + 1}c")
            text.tag_add("closing bracket", f"1.0+{closing}c", f"1.0+{closing + 1}c")
            text.tag_config("opening bracket", background="#acf")
            text.tag_config("closing bracket", background="#acf")
