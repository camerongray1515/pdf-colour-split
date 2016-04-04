#!/usr/bin/env python3
import subprocess

def split_colour(filename, force_ps=False):
    """
        Takes in the filename of a PDF, returns a tuple containing a list of all
        colour page numbers and a list containing all monochrome page numbers.

        If force_ps is true, the PDF will be converted to PS before being passed
        to gs.  This is useful for some PDF files which cause gs to segfault.
    """

    gs_args = ("-q -sDEVICE=pbmraw -o nul: -dUseFastColor=true "
        "-dGrayDetection=true -c \"<</EndPage {exch pop 2 ne dup {mark "
        "currentdevice //null .getdeviceparams .dicttomark exch pop "
        "/pageneutralcolor get = flush} if} bind>> setpagedevice\" -f"
    )

    command = "pdf2ps {0} - | gs {1} -" if force_ps else "gs {1} {0}"

    output = subprocess.check_output(command.format(filename, gs_args), shell=True).decode("UTF-8")

    for line in output.split("\n"):
        print(line)

def main():
    try:
        split_colour("/tmp/twitter.pdf")
    except Exception:
        split_colour("/tmp/twitter.pdf", force_ps=True)

if __name__ == "__main__":
    main()
