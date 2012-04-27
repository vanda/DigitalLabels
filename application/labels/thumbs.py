"""
Sorl Thumbnail Engine that accepts background color
---------------------------------------------------

Created on Sunday, February 2012 by Yuji Tomita
"""
from math import floor
from PIL import Image, ImageColor
from sorl.thumbnail.engines.pil_engine import Engine


class PadEngine(Engine):

    def create(self, image, geometry, options):
        image = super(PadEngine, self).create(image, geometry, options)
        image = self.pad(image, geometry, options)
        return image

    def pad(self, image, geometry, options):
        """
        Adds padding around the image to match the requested_size
        """
        if "pad" in options and image.size != geometry:
            canvas = Image.new("RGB", geometry, (255, 255, 255))

            left = int(floor((geometry[0] - image.size[0]) / 2))
            top = int(floor((geometry[1] - image.size[1]) / 2))

            canvas.paste(image, (left, top))

            image = canvas

        return image
