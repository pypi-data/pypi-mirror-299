# pic2asc

A tool to print picture on your terminal or into file


## install
```
pip install pic2asc
```
require python 3.12+, beacuse I use `type`
## Usage

### use in cmd
```
usage: pic2asc [-h] [--size WIDTH HEIGHT] [--no-color] [--mode {3bit,4bit,256bit}] [--file FILE] [--replace-str REPLACE_STR] path

positional arguments:
  path                  pictrue path

options:
  -h, --help            show this help message and exit
  --size WIDTH HEIGHT   size of asciipic. like --size 50 50. defalut is your terminal witdh/2, it is because two char with eque one char height
  --no-color            print no color ascii picture
  --mod {3bit,4bit,256bit}
                        3bit 4bit or regular RGB mod
  --file FILE           print ascii into file
  --replace-str REPLACE_STR
                        the chr you wang to show on the ascii pic, the string will be mapped to 0-255 in order
```
### use as module
```python
from pic2asc import pic2asc, color_type

p = pic2asc("path",show_color=False,mod = color_type.bit4)

p.pic2ascii(size=(50,50))
```
## Example

picture:

![karby](karby.jfif)

1. `color_type.bit3`
 
   ![Karby-3bit](./karby-3bit.png)
2. `color_type.bit4`
 
   ![Karby-3bit](./karby-4bit.png)
3. `color_type.bit256(default)`
 
   ![Karby-3bit](./karby-256bit.png)
