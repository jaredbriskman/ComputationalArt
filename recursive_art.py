""" Without 'art', 'earth' is just 'eh' """

import random
from PIL import Image
import math


#Functions
two_param = [lambda a,b: a*b , lambda a,b: 0.5*(a+b)]
one_param  = [lambda a: math.cos(math.pi*a), lambda a: math.sin(math.pi*a),
lambda a: a**2, lambda a: a**3]
end_param  = [lambda a,b: a, lambda a,b: b]
functionList = one_param + two_param + end_param

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """

    depth = random.randint(min_depth, max_depth)
    if depth == 1:
        random_index = random.randint(-2,-1)
        return functionList[random_index]
    else:
        random_index = random.randint(0,len(functionList)-len(end_param))
        if random_index > len(one_param) -1:
            func1 = build_random_function(depth-1,depth-1)
            func2 = build_random_function(depth-1,depth-1)
            return lambda x,y: functionList[random_index](func1(x,y),func2(x,y))
        else:
            func1 = build_random_function(depth-1,depth-1)
            return lambda x,y: functionList[random_index](func1(x,y))

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    diff = (val - input_interval_start) / float((input_interval_end - input_interval_start)) #ratio
    return ((output_interval_end - output_interval_start) * diff) + output_interval_start

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!

    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    #red_function = ["x"]
    #green_function = ["y"]
    #blue_function = ["x"]
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(red_function(x, y)),
                    color_map(green_function(x, y)),
                    color_map(blue_function(x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    #doctest.run_docstring_examples(evaluate_random_function,     globals())
    generate_art("example1.png",800,800)
    generate_art("example2.png",1920,1080)
