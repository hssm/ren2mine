import re
import os
from pathlib import Path

lineRegex = re.compile(r'\s*(.*)\s*(".+")')
rubyRegex = re.compile(r'{rb}(.+?){/rb}\s*?{rt}(.+?){/rt}')

def cleanFile(infile, outfile):
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    out = open(outfile, "w+")
    script = open(infile)
    names = set()
    out.write("""
<!DOCTYPE html>
<html>
<head>
<style>
body { 
    background-color: #000;
    color: #a1caff;
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

        # Skip some non-dialogue lines that slip through.
        # No guarantee these cover every case
        if name.startswith("$") or name.startswith("play"):
            continue

        # Replace ruby tags with html versions
        line = rubyRegex.sub("<ruby>\g<1><rt>\g<2></rt></ruby>", line)

        if name is not None:
            names.add(name)
            out.writelines("<div>{} {}</div>"
                           .format(name, line))
        else:
            out.writelines("<div>{}</div>".format(line))

    out.write("</body>")
    out.write("</html>")

if __name__ == "__main__":
    source_dir = "/home/hssm/.local/share/Steam/steamapps/common/Sound of Drop - fall into poison -/"
    output_dir = "/home/hssm/mineme/"

    # Last part of path is assumed to be the game name
    parts = Path(source_dir).parts
    start_at = len(parts) - 1
    game = parts[start_at]

    for root, subdirs, files in os.walk(source_dir):
        subdirs = Path(root).parts[start_at:]
        for file in files:
            if file.endswith(".rpy"):
                current_subdir = "/".join(subdirs)
                outname = Path(file).stem + ".html"
                outfile = os.path.join(output_dir, current_subdir, outname)
                infile = os.path.join(root, file)
                cleanFile(infile, outfile)
