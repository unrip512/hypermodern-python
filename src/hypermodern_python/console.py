"""The algorithm of Haugh transmission for circles."""

# IO-related
import imageio.v2 as imageio
from PIL import Image

# image processing
import numpy as np
import cv2
import click
import os

from . import __version__


def view(img: np.ndarray) -> Image.Image:
    """Convert an array to an Image type image."""
    if img.dtype != np.uint8:
        img = (img * 255).astype(np.uint8)
    return Image.fromarray(img)


class Hough_round:
    """Contain all the attributes and functions for implementing the Hough algorithm."""

    image: np.ndarray
    edge: np.ndarray
    pattern: np.ndarray
    r: int
    coef_space: np.ndarray
    res_circle_coord: np.ndarray

    def __init__(self, r: int) -> None:
        """Initialize an object of the class. Defines the radius of the desired circles.

        Args:
            r: the radius of the circles that we are looking for in the image.
        """
        self.r = r
        self.pattern = self.make_circle_pattern(r)

    def make_circle_pattern(self: "Hough_round", r: int) -> np.ndarray:
        """Create a circle template.

        Creates a two-dimensional array of 0 and 1,
        in which a circle is drawn using the numbers 1.

        Args:
            r: the radius of the circle in pixels.

        Returns:
            A two-dimensional np.ndarray array of size r*r.

        """
        pattern = np.zeros((2 * r + 1, 2 * r + 1))

        for i in range((-1) * r, r + 1):
            for j in range((-1) * r, r + 1):
                if np.rint(((abs(i)) ** 2 + (abs(j)) ** 2) ** 0.5) == r:
                    pattern[i + r, j + r] = 1

        return pattern

    def make_circle(self: "Hough_round", arr: np.ndarray, i: int, j: int) -> np.ndarray:
        """Draw a singe circle centered at a point (i,j) on the image arr.

        Args:
            arr: a twoyfh
            i: the coordinate of the center of the circle (axis = 0).
            j: the coordinate of the center of the circle (axis = 1).

        Returns:
            A two-dimensional array is an image of the coefficient space
            with a drawn circle.
        """
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

    def fit(self: "Hough_round", im: np.ndarray) -> None:
        """Сreates an image of the coefficient space using the original image.

        Args:
            im: image in the np.ndarray format
        """
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

    def draw_circle(self: "Hough_round") -> None:
        """Draw a red circle on the image.

        Applies the circle pattern obtained in function "make_circle_pattern"
        to the image and turns the pixel red at the points of the circle.
        """
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
@click.argument("picture_path_name", nargs=1)
@click.argument("cir_radius", nargs=1)
def main(picture_path_name: str, cir_radius: int) -> None:
    """Find and draw circles of a given radius on the image.

    Saves the image with the drawn found circles to the results folder.

    Args:
        picture_path_name: full path to the image.
        cir_radius: radius of the circle in pixels.
    """
    picture_name: str = picture_path_name
    radius: int = cir_radius

    click.echo(f"Picture {picture_name} has accepted. ")
    click.echo(f"Search for circles with a radius of {radius} . . .")
    path_to_save: str = f"./results/{picture_name}"
    os.makedirs(path_to_save, exist_ok=True)

    im1: np.ndarray = imageio.imread(f"images/{picture_name}")
    hough1: Hough_round = Hough_round(int(radius))
    hough1.fit(im1)
    hough1.draw_circle()

    click.echo("The algorithm has completed.")

    edge_image: Image.Image = view(hough1.edge)
    coef_space_image: Image.Image = view(hough1.coef_space)
    result_image: Image.Image = view(hough1.image)

    edge_image.save(f"{path_to_save}/edges.jpg")
    coef_space_image.save(f"{path_to_save}/coef_space_{radius}.jpg")
    result_image.save(f"{path_to_save}/result_{radius}.jpg")

    click.echo(f"Results saved in {path_to_save}")
