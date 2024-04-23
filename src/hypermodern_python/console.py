# IO-related
import imageio 
from PIL import Image

# image processing
import numpy as np
import cv2
import click

from . import __version__
import argparse
import sys

def view(img):
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    return Image.fromarray(img)


class Hough_round:

    image = None
    edge = None
    pattern = None
    r = None
    coef_space = None
    res_circle_coord = None

    def __init__(self, r):

        self.r = r
        self.pattern = self.make_circle_pattern(r)


    def make_circle_pattern(self, r):

        pattern = np.zeros((2 * r + 1, 2 * r + 1))

        for i in range((-1) * r, r + 1):
            for j in range((-1)*r, r + 1):
                if np.rint(((abs(i))**2 + (abs(j))**2)**0.5) == r:
                    pattern[i + r, j + r] = 1

        return pattern

    def make_circle(self, arr, i, j):

        r = self.r
        height, width = np.shape(arr)

        if (i-r)>=0 and (i+r+1)< height and (j-r)>=0 and (j+r+1)<width:
            arr[i-r:i+r+1, j-r:j+r+1] += self.pattern
        return arr

    def fit(self, im):



        t_lower = 100
        t_upper = 400
        edge = cv2.Canny(im, t_lower, t_upper)

        self.coef_space = np.zeros(np.shape(edge))
        self.image = im
        self.edge = edge


        height, width = np.shape(edge)

        for i in range(height):
            for j in range(width):
                if edge[i, j]:
                    self.coef_space = self.make_circle(self.coef_space, i, j)

        min_val = np.min(self.coef_space)
        max_val = np.max(self.coef_space)
        self.coef_space = (self.coef_space - min_val)/(max_val-min_val)

        self.res_circle_coord = self.coef_space > 0.8

    def draw_circle(self):

        height, width = np.shape(self.coef_space)

        for i in range(height):
            for j in range(width):
                if self.res_circle_coord[i, j]:
                    r = self.r

                    if (i-r)>=0 and (i+r+1)< height and (j-r)>=0 and (j+r+1)<width:

                        self.image[i-r:i+r+1, j-r:j+r+1][self.pattern.astype(bool)] = [255, 0, 0]



@click.command()
@click.version_option(version=__version__)
def main(args=sys.argv):
    '''

    parser = argparse.ArgumentParser(description='I need full name of the picture.')
    parser.add_argument("--pn", dest='pn', type=str, help="name of picture in format picture.jpg")
    name = parser.parse_args().pn
    click.echo(name)

    '''
    for arg in args:
        click.echo(arg)


    im1 = imageio.imread('images/coins.jpg')
    hough1 = Hough_round(60)
    hough1.fit(im1)
    hough1.draw_circle()


    edge_image = Image.fromarray(hough1.edge) 
    coef_space_image = Image.fromarray(np.uint8(hough1.coef_space * 255), 'L')
    result_image = Image.fromarray(hough1.image)

    edge_image.save("results/edges.jpg")
    coef_space_image.save("results/coef_space.jpg")
    result_image.save("results/result.jpg")
    
    #args = sys.argv[1:]

    click.echo("Hello world!")

