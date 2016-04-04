#!/usr/bin/env python3
import subprocess
from binascii import hexlify

def is_page_colour(pdf_filename, page_number, dpi=10):
    p = subprocess.Popen([
        "/usr/bin/pdftoppm",
        "-r", str(dpi),
        "-f", str(page_number),
        "-l", str(page_number),
        pdf_filename
    ], stdout=subprocess.PIPE)

    ppm, stderr = p.communicate()

    ppm = ppm.split(b"\n")
    magic_number = ppm[0].decode("UTF-8").split()[0]
    # TODO: Enforce that magic number is P6
    # width, height = ppm[1].decode("UTF-8").split()
    maxval = int(ppm[2].decode("UTF-8").split()[0])
    pixels = b''.join(ppm[3:])

    num_bytes = 1 if maxval < 256 else 2
    slice_size = num_bytes*3

    for i in range(0, len(pixels), slice_size):
        slice_pixels = pixels[i:i+slice_size]
        if num_bytes == 1:
            colour_values = slice_pixels
        else:
            colour_values = [slice_pixels[x:x+num_bytes] for x in range(0,
                slice_size, num_bytes)]

        r,g,b = colour_values
        if not(r==g and g==b):
            return True # We encountered a colour pixel so page is colour

    return False # No colour pixels were encoutered

def get_page_count(pdf_filename):
    lines = subprocess.check_output(["/usr/bin/pdfinfo", pdf_filename]).decode(
        "UTF-8").split("\n")
    for line in lines:
        if line.startswith("Pages:"):
            return int(line.split()[1].strip())

def detect_pages(pdf_filename, num_pages):
    colour_pages = []
    mono_pages = []

    for i in range(1, num_pages+1):
        if is_page_colour(pdf_filename, i):
            colour_pages.append(i)
        else:
            mono_pages.append(i)

    return (colour_pages, mono_pages)

def move_pages(num_pages, colour_pages, mono_pages, duplex, stackable):
    if duplex:
        duplex_colour_pages = []
        duplex_mono_pages = []
        # If either side of a page is colour, put both sides into the colour
        # list
        for i in range(1, num_pages+1, 2):
            if i in colour_pages or i+1 in colour_pages:
                duplex_colour_pages += [i, i+1]
            else:
                duplex_mono_pages += [i, i+1]
    else:
        duplex_colour_pages = colour_pages
        duplex_mono_pages = mono_pages

    return (duplex_colour_pages, duplex_mono_pages)


def main():
    pdf_filename = "/tmp/pdf/final_report.pdf"
    num_pages = get_page_count(pdf_filename)

    colour, mono = detect_pages(pdf_filename, num_pages)
    print((colour, mono))
    print(move_pages(num_pages, colour, mono, True, True))
    # for i in range(1, 62):
    #     colour = is_page_colour("/tmp/pdf/final_report.pdf", i)
    #     print("Page {} is{}colour".format(i, " " if colour else " not "))

if __name__ == "__main__":
    main()
