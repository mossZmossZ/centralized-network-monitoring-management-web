import subprocess

try:
    output = subprocess.check_output(["pdflatex", "--version"])
    print(output.decode("utf-8"))
except FileNotFoundError:
    print("pdflatex not found")