#!/usr/bin/env python3
import binascii

def is_ppm_colour(filename):
    """
        Takes in filename of PPM file and returns if it contains any colour
        pixels or not.  Designed for PPM files produced by "pdftoppm" and
        therefore does not handle comments in the PPM files.
    """
    with open(filename, "rb") as f:
        magic_number = f.readline().decode("UTF-8").split()[0]
        width, height = f.readline().decode("UTF-8").split()
        maxval = int(f.readline().decode("UTF-8").split()[0])

        num_bytes = 1 if maxval < 256 else 2
        # num_bytes=2

        bs = f.read(num_bytes*3)
        while bs:
            # Takes list of num_bytes*3 bytes and converts it into a list of
            # three components (one for each of RGB) each containing num_bytes
            # bytes
            if num_bytes == 1:
                colour_values = bs
            else:
                colour_values = [bs[x:x+num_bytes] for x in range(0,
                    num_bytes*3, num_bytes)]

            r,g,b = colour_values
            if not(r==g and g==b):
                return True # We encountered a colour pixel so page is colour

            bs = f.read(num_bytes*3)

        return False # No colour pixels were encoutered

def main():
    for i in range(0, 60):
        num = str(i+1).zfill(2)
        colour = is_ppm_colour("/tmp/pdf/report-{}.ppm".format(num))
        print("Page {} is{}colour".format(num, " " if colour else " not "))

if __name__ == "__main__":
    main()
