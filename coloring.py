from output import output
import sys
sys.stdout.write = output


def color(text):
    for tag in text.tag_names():
        text.tag_delete(tag)
    inp = text.get("1.0", "end-1 chars")
    count = 0
    start = 0
    end = 0
    while True:
        try:
            start = inp.index('"', end)
            end = inp.index('"', start + 1) + 1
        except ValueError:
            break
        else:
            text.tag_add(str(count), f"1.0+{str(start)} chars", f"1.0+{str(end)} chars")
            text.tag_config(str(count), foreground="green")

    start = 0
    end = 0
    while True:
        try:
            start = inp.index("'", end)
            end = inp.index("'", start + 1) + 1
        except ValueError:
            break
        else:
            text.tag_add(str(count), f"1.0+{str(start)} chars", f"1.0+{str(end)} chars")
            text.tag_config(str(count), foreground="green")
    print(str(start) + " " + str(end))
