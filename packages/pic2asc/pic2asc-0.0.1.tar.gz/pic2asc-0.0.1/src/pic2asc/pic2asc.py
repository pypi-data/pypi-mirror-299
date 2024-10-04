from typing import Tuple
from PIL import Image
from os import get_terminal_size
from .color import color_ctl,color_type

type Size_Tuple = Tuple[int,int]



class pic2asc:

    CHRS = "   ...',:;clodxkO0KXNWMMMM"

    def __init__(self,path: str,chr_ls: str = "",show_color = True,mod:color_type = color_type.bit256) -> None:
        """pic2ascii

        Args:
            path (str): pic path
            chr_ls (str, optional): the chr you wang to show on the ascii pic, the string will be mapped to 0-255 in order. Defaults to "".
            show_color (bool, optional): wither to show color. if not only show ascii. Defaults to True.
            mod (color_type, optional): see color_type, only support 3-bit(bit3) 4-bit(bit4) and 256 bit(bit256), see https://en.wikipedia.org/wiki/ANSI_escape_code#Colors for more detile. Defaults to color_type.bit256.
        """
        self.chr_ls = chr_ls
        self.show_color = show_color
        self.color = color_ctl(mod=mod,show_color=show_color)
        self.img = Image.open(path)

    def pic2ascii(self,size:Size_Tuple = (0,0),file:str = None) -> None:
        """change pic 2 ascii

        Args:
            size (Size_Tuple, optional): the size of ascii picture. (0,0) mean use get_terminal_size() to determine the width. Defaults to (0,0).
            file (str, optional): if not None. the ascii pic will print into file. Defaults to None.
        """
        ascii_pic = []
        if size == (0,0):
            w,h = self.img.size
            terminal_w = get_terminal_size()[0]
            size = (terminal_w//2,int((terminal_w//2/w)*h))
        if self.chr_ls:
            chrs = self.chr_ls
        else:
            chrs = self.CHRS
        chrs_len = len(chrs)
        img = self.img.resize(size)
        pixls = img.load()
        pic_line = []
        for y in range(size[1]):
            for x in range(size[0]):
                c = chrs[int(self.color.Rgb2L(pixls[x,y])/256*chrs_len)]
                pic_line.append(self.color.rgb2ascii(pixls[x,y],f"{c}{c}"))
            ascii_pic.append(pic_line)
            pic_line = []
        if file:
            with open(file,'w',encoding='utf8') as f:
                f.write("\n".join([''.join(i) for i in ascii_pic]))
        else:
            for i in ascii_pic:
                print(''.join(i))



# 绿色文本

