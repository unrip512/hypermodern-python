# IO-related
import imageio.v2 as imageio
from PIL import Image

# image processing
import numpy as np
import cv2
import click
import os

from . import __version__


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
            for j in range((-1) * r, r + 1):
                if np.rint(((abs(i)) ** 2 + (abs(j)) ** 2) ** 0.5) == r:
                    pattern[i + r, j + r] = 1

        return pattern

    def make_circle(self, arr, i, j):

        r = self.r
        height, width = np.shape(arr)

        if (
            (i - r) >= 0
            and (i + r + 1) < height
            and (j - r) >= 0
            and (j + r + 1) < width
        ):
            arr[i - r : i + r + 1, j - r : j + r + 1] += self.pattern
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
        self.coef_space = (self.coef_space - min_val) / (max_val - min_val)

        self.res_circle_coord = self.coef_space > 0.8

    def draw_circle(self):

        height, width = np.shape(self.coef_space)

        for i in range(height):
            for j in range(width):
                if self.res_circle_coord[i, j]:
                    r = self.r

                    if (
                        (i - r) >= 0
                        and (i + r + 1) < height
                        and (j - r) >= 0
                        and (j + r + 1) < width
                    ):

                        self.image[i - r : i + r + 1, j - r : j + r + 1][
                            self.pattern.astype(bool)
                        ] = [255, 0, 0]


@click.command()
@click.version_option(version=__version__)
@click.argument("args", nargs=2)
def main(args):

    picture_name = args[0]
    radius = args[1]

    click.echo(f"Picture {picture_name} has accepted. ")
    click.echo(f"Search for circles with a radius of {radius} . . .")
    path_to_save = f"./results/{picture_name}"
    os.makedirs(path_to_save, exist_ok=True)

    im1 = imageio.imread(f"images/{picture_name}")
    hough1 = Hough_round(int(radius))
    hough1.fit(im1)
    hough1.draw_circle()

    click.echo("The algorithm has completed.")

    edge_image = view(hough1.edge)
    coef_space_image = view(hough1.coef_space)
    result_image = view(hough1.image)

    edge_image.save(f"{path_to_save}/edges.jpg")
    coef_space_image.save(f"{path_to_save}/coef_space_{radius}.jpg")
    result_image.save(f"{path_to_save}/result_{radius}.jpg")

    click.echo(f"Results saved in {path_to_save}")
