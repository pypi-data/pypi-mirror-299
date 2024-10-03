import argparse

from .extract import JarNotFound, jar_extract

parser = argparse.ArgumentParser("jarextract", description="JAR/ZIP Extraction Utility")
parser.add_argument("input", help="input file")
parser.add_argument("output", help="output file")
args = parser.parse_args()

try:
    offset, size = jar_extract(args.input, args.output)
    print(f"JAR successfully extracted: offset: 0x{offset:X}, size: {size} bytes. Bye.")

except JarNotFound:
    print("JAR not found. Bye.")
