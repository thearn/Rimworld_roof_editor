import numpy as np
import base64, shutil, zlib
from PIL import Image

bytes2sky_type = {}
bytes2sky_type['\x00\x00'] = 3 # empty sky
bytes2sky_type['+\x1a'] = 2 # thin rock
bytes2sky_type['\r\x14'] = 1 # constructed
bytes2sky_type['D*'] = 0 #overhead mountain

type2bytes = {}
for name in bytes2sky_type:
    type2bytes[bytes2sky_type[name]] = name

class RimMapRoof(object):
    mapsize = None
    pre_roof = None
    roof_code = None
    post_roof = None
    fname = None
    roof_array = None

    def __init__(self, fn):
        self.fname = fn
        self.name = self.fname.split(".")[0]
        backup_name = fn + "_backup"
        shutil.copy(fn, backup_name)

        self.load()

    def load(self):
        code = []
        save = False
        before = True
        pre, post = '', '\r\n</roofs>\r\n'
        with open(self.fname, 'rb') as f:
            for line in f:
                if 'initialMapSize' in line:
                    step = line.split('(')
                    step = step[1].split(")")[0]
                    m,_,n = step.split(",")
                    self.mapsize = (int(m), int(n))

                if 'roofGrid' in line:
                    save = not save
                    before = False
                if save:
                    #print line.split(" ")
                    code.append(line.strip())
                else:
                    if before:
                        pre += line
                    else:
                        post += line
        pre += '\t\t\t\t<roofGrid>\r\n\t\t\t\t\t<roofs>\r\n'


        self.roof_array = np.zeros(self.mapsize).flatten()
        self.pre_roof = pre
        self.post_roof = post

        if code[1] == '<roofsDeflate>':
          codes = zlib.decompress(''.join(code[2:-1]).decode('base64'), -zlib.MAX_WBITS)
          cells = [codes[k:k+2] for k in range(0,len(codes),2)]
          idx = 0
          for cell in cells:
            self.roof_array[idx] = bytes2sky_type[cell]
            idx += 1
        else: 
          code = code[2:-1]
          top = ''.join(code)

          chunks, chunk_size = len(top), 8
          codes = [ top[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]

          idx = 0
          for c in codes:
              c = base64.b64decode(c)
              cells = [c[k:k+2] for k in range(0,len(c),2)]

              for cell in cells:
                  self.roof_array[idx] = bytes2sky_type[cell]
                  idx += 1
        self.roof_array = self.roof_array.reshape(self.mapsize)

    def array2code(self):
        roof_array = self.roof_array.flatten()
        hexcodes = [type2bytes[i] for i in roof_array]
        codes = [hexcodes[i:i+3] for i in range(0, len(hexcodes), 3)]

        s = ''
        for code in codes:
            s += base64.b64encode(''.join(code))
        ss = s[1:]

        self.roof_code = self.pre_roof + s[0] + '\r\n' + '\r\n'.join([ss[i:i+100] for i in range(0, len(ss), 100)]) + self.post_roof

    def save(self, fn):
        self.array2code()

        with open(fn, 'wb') as f:
            f.write(self.roof_code)

    def write_image(self, fn=None):
        if not fn:
            fn = self.name + ".bmp"
        self.array2code()
        data = self.roof_array[::-1] / 3.0 * 255
        data = data.astype(np.uint8)
        im = Image.fromarray(data, mode='L')
        im.save(fn)

    def read_image(self, fn):
        im = Image.open(fn)
        im = im.convert('L')

        data = np.fromiter(iter(im.getdata()), np.float32)
        data.resize(self.mapsize[0], self.mapsize[1])

        data = data[::-1]/255. * 3

        data = data.astype(np.uint8)

        self.roof_array = data


if __name__ == '__main__':
    fn = 'Pottstown.rws'

    rm = RimMapRoof(fn)
    #rm.read_image('Untitled.bmp')

