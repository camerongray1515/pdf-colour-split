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

def main():
    for i in range(1, 61):
        colour = is_page_colour("/tmp/pdf/final_report.pdf", i)
        print("Page {} is{}colour".format(i, " " if colour else " not "))

if __name__ == "__main__":
    main()
