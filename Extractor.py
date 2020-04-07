
import os
import sys
import zlib
extract_folder = str(input("Which Folder You Want To Extract To: "))
if not os.path.exists(extract_folder):
    os.system(f"mkdir {extract_folder}")

filename = str(input("Enter Your Path Of File: "))

def hex_upper_with_0x(f):
    f = "0x"+str(f)
    return f.upper()
NPKSIGNATURE = [0x4E, 0x58, 0x50, 0x4B]
all_bytes = open(filename, "rb").read()
if list(all_bytes[:4]) != NPKSIGNATURE:
    print("Failed to load file, bad signature")
    sys.exit()
def little_endian_to_int(f):
    f = int.from_bytes(f, "little")
    return f
print()
print("NeoX Package File: " + filename )
print("============================")
filecount = little_endian_to_int(all_bytes[4:6])
count = 0
listoffset = little_endian_to_int(all_bytes[0x14:0x18])
print("- Data Count: %d" % filecount)
print("- List Offset: " + hex_upper_with_0x(listoffset))
print("============================")
for i in range(listoffset, len(all_bytes), 28):
    filesign = all_bytes[i:i+4]
    fileoffset = little_endian_to_int(all_bytes[i+4:i+8])
    filelength = little_endian_to_int(all_bytes[i+8:i+12])
    fileoriginallength = little_endian_to_int(all_bytes[i+12:i+16])
    filehash = all_bytes[i+16:i+24]
    fileunknown = all_bytes[i+24:i+28]
    count += 1
    print("- File %.6d: " % count)
    print("-- Unknown: " + filesign.hex().upper())
    print("-- Offset: " + hex_upper_with_0x(fileoffset))
    print("-- Length: " + hex_upper_with_0x(filelength) + " (%d)" % filelength)
    print(
        "-- Original Length: " +
        hex_upper_with_0x(fileoriginallength) +
        " (%d)" % fileoriginallength
    )
    print("-- Hash: " + filehash.hex().upper())
    print("-- Unknown: " + fileunknown.hex().upper())
    
    filecontent = all_bytes[fileoffset:fileoffset + filelength]
    
    if True:
        print()
        print("-- = Start Extraction =")
        if filelength != fileoriginallength:
            filecontent = zlib.decompress(filecontent)
            print("\nDecompressed: ")
            
            extracttype = "txt"
            print()
        extractname = (
filesign.hex().lower() +
            "." + extracttype
        )
        extractpath = os.path.join(extract_folder, extractname)
        open(extractpath, "wb").write(filecontent)
        print("--- Saved as " + extractpath)
    print()