from .pic2asc import pic2asc
from .color import color_type

VERSION = "0.0.2"

__all__ = ["pic2asc","color_type"]


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("path", type=str, help="pictrue path")
    parser.add_argument("--size", type=int, nargs=2, default=[0,0],metavar=('WIDTH', 'HEIGHT'),help="size of asciipic. like --size 50 50. defalut is your terminal witdh/2, it is because two char with eque one char height")
    parser.add_argument("--no-color", action='store_false', help="print no color ascii picture")
    parser.add_argument("--mod", choices=['3bit','4bit','256bit'],default='256bit',help="3bit 4bit or regular RGB mod")
    parser.add_argument("--file", type=str,help="print ascii into file")
    parser.add_argument("--replace-str",type=str,help="the chr you wang to show on the ascii pic, the string will be mapped to 0-255 in order")


    
    args = parser.parse_args()
    match args.mode:
        case "3bit":
            mod = color_type.bit3
        case "4bit":
            mod = color_type.bit4
        case _:
            mod = color_type.bit256
    p = pic2asc(args.path,args.replace_str,args.no_color,mod)

    p.pic2ascii(tuple(args.size),args.file)
    