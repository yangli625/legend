import argparse
import struct # https://stackoverflow.com/questions/374318/conversion-of-unicode-string-in-python

# memory address of everything
# https://www.rxgl.net/html/wuxiazhoubian/2012-02/2168.html

parser = argparse.ArgumentParser()
parser.add_argument('dir', type=str, help='legend save data directory')
# parser.add_argument('-d','--save_dir', type=str, required=True, help='source data directory')

args = parser.parse_args()
dir = args.dir

### everything comes with 2 bytes, any 1 byte value, will followed by a '00'
self_moral = 512 + 436 # 1 byte, 100
self_talent = 512 + 444 # 1 byte, 99
self_kf = 512 + 450 # 1 byte
self_kf_level = 512 + 470 # 2 bytes, 999 (E7 03)

item_start = 36
item_end = 512 + 315 # THE last byte of item bag

with open(dir+'/R1.GRP', "rb") as fp, open(dir+'/R1_backup', "wb") as fp1:
    data = fp.read()
    fp1.write(data)
    data = list(data)

data[self_moral] = struct.pack("=B", 100)
data[self_talent] = struct.pack("=B", 99)
data[self_kf_level : self_kf_level + 2] = struct.pack("=H", 999)

# search item list
for i in range(item_start, item_end, 4):
    if ord(data[i]) == int('0xAE', 0): # money
        print('find money!')
        data[i+2 : i+4] = struct.pack("=H", 9999)
    if ord(data[i]) == int('0xFF', 0): # empty slots
        break

with open(dir+'/R1.GRP', "wb") as fp:
    data = ''.join(data)
    fp.write(data)

