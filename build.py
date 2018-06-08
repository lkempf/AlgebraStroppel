import glob
import subprocess
import os.path

for f in glob.glob("*.tex"):
    print("Building file '{}'".format(f))
    date = subprocess.run(["git", "log", "-1", "--format=\"%ai\"", f], stdout=subprocess.PIPE)
    date = date.stdout.decode("utf-8").split(" ")[0][1:]

    lines = []
    with open(f, encoding="utf-8") as infile:
        for line in infile:
            lines.append(line.replace("\\lastcompiled", "zuletzt geändert: \\printdate{{{}}}".format(date)))
    with open(f, "w", encoding="utf-8") as outfile:
        for line in lines:
            outfile.write(line)

    code = subprocess.run(["latexmk", "-pdf", "-outdir=out", "-halt-on-error", f]).returncode
    if code != 0 or not os.path.isfile("out/{}.pdf".format(f[:-4])): 
        print("Error building file '{}'".format(f))
        exit(1)
    print()