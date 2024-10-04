from enum import Enum
import math
from typing import Tuple

ASCII_CODE = 0
RGB_VALUE = 1

type RGB_TUPLE = Tuple[int,int,int]

class color_type(Enum):
    bit3 = 0
    bit4 = 1
    bit256 = 2

class color:
    BLACK           = 30
    RED             = 31
    GREEN           = 32
    YELLOW          = 33
    BLUE            = 34
    MAGENTA         = 35
    CYAN            = 36
    WHITE           = 37

    BLACK_RGB       = (0,0,0)
    RED_RGB         = (255,0,0)
    GREEN_RGB       = (0,255,0)
    YELLOW_RGB      = (255,255,0)
    BLUE_RGB        = (0,0,255)
    MAGENTA         = (128,0,128)
    CYAN_RGB        = (0, 255, 255)
    WHITE_RGB       = (255, 255, 255)

    # expand_ascii_color
    LIGHTBLACK_EX   = 90
    LIGHTRED_EX     = 91
    LIGHTGREEN_EX   = 92
    LIGHTYELLOW_EX  = 93
    LIGHTBLUE_EX    = 94
    LIGHTMAGENTA_EX = 95
    LIGHTCYAN_EX    = 96
    LIGHTWHITE_EX   = 97

    LIGHTBLACK_EX_RGB  = (128, 128, 128)
    LIGHTRED_EX_RGB    = (255, 85, 85)
    LIGHTGREEN_EX_RGB  = (85, 255, 85)
    LIGHTYELLOW_EX_RGB = (255, 255, 85)
    LIGHTBLUE_EX_RGB   = (85, 85, 255)
    LIGHTMAGENTA_EX    = (255, 85, 255)
    LIGHTCYAN_EX_RGB   = (85, 255, 255)
    LIGHTWHITE_EX_RGB  = (255, 255, 255)
    


class color_ctl:
    CSI = '\033['
    RST = '\033[0m'
    def __init__(self, mod:color_type,show_color = True) -> None:
        """control the color of the ascii pic

        Args:
            mod (color_type): color mod
            show_color (bool, optional): if False. the method will do nothing. Defaults to True.
        """
        if not show_color:
            self.rgb2ascii = lambda x,y : y
            return
        match mod:
            case color_type.bit3|color_type.bit4:
                self.init_color(mod)
            case color_type.bit256:
                self.rgb2ascii = lambda x,y : f"\033[38;2;{x[0]};{x[1]};{x[2]}m{y}\033[0m"
                self.rgb2rgb   = lambda x:x

    def init_color(self,mod) -> None:
        self.color_dict = {}
        self.color = color()
        self.color_name = []
        if mod == color_type.bit4:
            for name in dir(self.color):
                if name.endswith("_RGB"):
                    self.color_dict[name[:-4]] = (getattr(self.color,name[:-4]),getattr(self.color,name))
                    self.color_name.append(name[:-4])
        else:
            for name in dir(self.color):
                if name.endswith("_RGB") and not name.startswith("LIGHT"):
                    self.color_dict[name[:-4]] = (getattr(self.color,name[:-4]),getattr(self.color,name))
                    self.color_name.append(name[:-4])
    
 
    def tans_color(self,RGB:RGB_TUPLE) -> str:
        min_color = None
        min_dis = math.inf
        for color in self.color_name:
            dis = self.ColourDistance(RGB,self.color_dict[color][RGB_VALUE])
            if  dis < min_dis:
                min_color = color
                min_dis = dis
        assert(min_color)
        return min_color

    @staticmethod
    def ColourDistance(rgb_1:RGB_TUPLE, rgb_2:RGB_TUPLE) -> float:
        """look at https://www.compuphase.com/cmetric.htm change RGB color space to CIELAB color space

        Args:
            rgb_1 (Tuple[int,int,int]): one RGB value
            rgb_2 (Tuple[int,int,int]): another RGB value 

        Returns:
            float: the euclidean metric between two RGB
        """
        R_1,G_1,B_1 = rgb_1
        R_2,G_2,B_2 = rgb_2
        rmean = (R_1 +R_2 ) / 2
        R = R_1 - R_2
        G = G_1 -G_2
        B = B_1 - B_2
        return math.sqrt((2+rmean/256)*(R**2)+4*(G**2)+(2+(255-rmean)/256)*(B**2))
    @staticmethod
    def Rgb2L(rgb:RGB_TUPLE) -> int:
        R,G,B=rgb
        return int(0.212671*R+0.71516*G+0.072169*B)
    
    def rgb2ascii(self,RGB: RGB_TUPLE,c:str) -> str:
        color_code = self.color_dict[self.tans_color(RGB)][ASCII_CODE]
        return f"{self.CSI}{color_code}m{c}{self.RST}"

    def rgb2rgb(self,RGB: RGB_TUPLE) -> RGB_TUPLE:
        return self.color_dict[self.tans_color(RGB)][RGB_VALUE]

