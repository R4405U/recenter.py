#!/bin/python3
import sys
import argparse
from PIL import Image
from typing import Union,Tuple


COLOR_MAP = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}


ColorInput = Union[str, Tuple[int,int,int]]


def process_color(color: ColorInput) -> Tuple[int, int, int]:
    if isinstance(color,str):
        color_name = color.lower()
        if color_name in COLOR_MAP:
            return COLOR_MAP[color_name]
        else:
            raise ValueError(f"Unknown color name {color}, supported colors are {list(COLOR_MAP.keys())}")
    elif isinstance(color,tuple):
        if len(color) != 3 or not all(0 <= c <= 255 for c in color):
            raise ValueError(
                f"Invalid RGB tuple format: {color}, Must be a tuple of 3 integers (0-255)"
            )
        return color
    else:
        raise TypeError(f"Invalid color type. Expected str or tuple, got {type(color).__name__}")


def convert_image_geometry(input_path: str,
                           output_path: str,
                           width: int,
                           height: int,
                           color: ColorInput):

    try:
        source_img = Image.open(input_path).convert("RGBA")

        size = (width, height)
        
        # Ensure color is an RGB tuple if it was a string name, 
        # or use the string if process_color wasn't called (e.g., "black" default).
        final_color = process_color(color) if isinstance(color, str) else color

        background = Image.new("RGB", size, final_color)
        
        src_w, src_h = source_img.size
        offset_x     = (width - src_w) // 2
        offset_h     = (height - src_h) // 2

        background.paste(source_img,(offset_x, offset_h), source_img)

        background.save(output_path)
        print(output_path)
    except FileNotFoundError:
        print(f"Input file not found at {input_path}",file=sys.stderr)
    except Exception as e:
        print(e, file=sys.stderr)
    

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="input image path", type=str, required=True)
    parser.add_argument("-o", "--output", help="output image path", type=str, required=True)
    parser.add_argument("-w", "--width", help="output image width", type=int, required=True)
    parser.add_argument("-hi", "--height", help="output image height", type=int, required=True)
    
    parser.add_argument("-bg", "--background", 
                        help="Output image background color name (e.g., 'red'). Overrides -R, -G, -B.", 
                        type=str)
                        
    parser.add_argument("-R", help="'R' value (0-255) for background color", type=int)
    parser.add_argument("-G", help="'G' value (0-255) for background color", type=int)
    parser.add_argument("-B", help="'B' value (0-255) for background color", type=int)
    
    args = parser.parse_args()
    
    color = "black"

    if args.background:
        color = args.background
        
    elif args.R is not None or args.G is not None or args.B is not None:
        R = args.R if args.R is not None else 0
        G = args.G if args.G is not None else 0
        B = args.B if args.B is not None else 0
        
        color = (R, G, B)
        

    convert_image_geometry(
        input_path=args.input,
        output_path=args.output,
        width=args.width,
        height=args.height,
        color=color
    )


if __name__ == "__main__":
    main()
