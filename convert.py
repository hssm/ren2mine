import re

input = "/home/hssm/.local/share/Steam/steamapps/common/Sound of Drop - fall into poison -/game/scenario/0-01.rpy"
output = "/home/hssm/out.html"

lineRegex = re.compile(r'\s*(.+) (".+")')
rubyRegex = re.compile(r'{rb}(.+?){/rb}\s*?{rt}(.+?){/rt}')

def cleanFile(script, out):
    out.write("""
<!DOCTYPE html>
<html>
<head>
<style>
body { 
    background-color: #000;
    color: #fff;
    font-size: 18px;
}
</style>
</head>
<body>
""")
    for line in script:
        m = lineRegex.search(line)
        if not m:
            continue
        name = m.group(1)
        line = m.group(2)

        # Replace ruby tags with html versions
        line = rubyRegex.sub("<ruby>\g<1><rt>\g<2></rt></ruby>", line)

        if name is not None:
            out.writelines("<div>{} {}</div>".format(name, line))
        else:
            out.writelines("<div>{}</div>".format(line))

    out.write("""
</body>
</html>
""")



def getColor(s):
    h = hash(s)
    r = (h & 0xFF0000) >> 16
    g = (h & 0x00FF00) >> 8
    b = h & 0x0000FF
    print ("rgb({},{},{})".format(r, g, b))


if __name__ == "__main__":
    cleanFile(open(input), open(output, "w+"))
