""" Without 'art', 'earth' is just 'eh' """

import random
from PIL import Image
import math
import numpy

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

    #Functions
    funcs = {
    "two_param":(lambda a,b: a*b , lambda a,b: 0.5*(a+b)),
    "one_param":(lambda a: numpy.cos(math.pi*a), lambda a: numpy.sin(math.pi*a),
    lambda a: a**2, lambda a: a**3),
    "end_param":(lambda a,b: a, lambda a,b: b)
    }
    functionTuple = funcs["one_param"] + funcs["two_param"] + funcs["end_param"]

    #Build
    depth = random.randint(min_depth, max_depth)
    if depth == 1: #Base case
        random_index = random.randint(0, len(funcs["end_param"]) -1)
        return funcs["end_param"][random_index] #Choses between end functions
    else:
        random_index = random.randint(0,len(functionTuple)-len(funcs["end_param"])) #Chose from non end functions
        if random_index > len(funcs["one_param"]) -1:
            func1 = build_random_function(depth-1,depth-1)
            func2 = build_random_function(depth-1,depth-1)
            return lambda x,y: functionTuple[random_index](func1(x,y),func2(x,y))
        else: #one_param
            func1 = build_random_function(depth-1,depth-1)
            return lambda x,y: functionTuple[random_index](func1(x,y))

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
    color_code = remap_interval(val, -1, 1, 0, 255)
    return color_code.astype('uint8') #For scalar

def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)
    # Create image and loop over all pixels
    x = numpy.tile(numpy.linspace(-1, 1, x_size), (y_size, 1)) #for X
    y = numpy.tile(numpy.linspace(-1, 1, y_size), (x_size, 1)).T #for Y
    r = red_function(x, y)
    g = green_function(x, y)
    b = blue_function(x, y)
    im = Image.fromarray(color_map(numpy.stack((r,g,b), axis=2)), "RGB") #Stacking all three channels into an image
    im.save(filename)


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()
    #doctest.run_docstring_examples(evaluate_random_function,     globals())
    generate_art("example1.png",800,800)
    generate_art("example2.png",1920,1080)
