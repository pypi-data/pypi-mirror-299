import io
import zipfile

_ZIP_HEADER = b"PK\x03\x04"
_JAR_MANIFEST = "META-INF/MANIFEST.MF"


class JarNotFound(Exception):
    pass


def jar_find(sfx: io.BufferedReader) -> tuple[int, int]:
    """
    Finds JAR file in BufferedReader object.

    Returns tuple of JAR's offset and size.
    """

    filesize = sfx.seek(0, io.SEEK_END)

    for offset in range(0, filesize, 256):
        sfx.seek(offset, io.SEEK_SET)

        if not sfx.peek(4).startswith(_ZIP_HEADER):
            continue

        zip = zipfile.ZipFile(sfx)

        try:
            zip.testzip()
            zip.getinfo(_JAR_MANIFEST)

        except (zipfile.BadZipFile, KeyError):
            continue

        return sfx.seek(offset, io.SEEK_SET), filesize - offset

    raise JarNotFound()


def jar_extract(input: str, output: str) -> tuple[int, int]:
    """
    Extracts JAR file from input to output file.

    Returns tuple of JAR's offset and size.
    """

    with open(input, "rb") as sfx:
        result = jar_find(sfx)

        with open(output, "wb") as jar:
            while data := sfx.read():
                jar.write(data)

    return result
