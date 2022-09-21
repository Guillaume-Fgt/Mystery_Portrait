Generate a mystery image from an image file. 

![Example](/images_readme/Vador.jpg)

A mystery image is composed of squares, numbered zero to ten. Each number matches a specific shape.
![Shapes](/images_readme/shapes.png)

Drawing those shapes will reveal the subject of the image. A celebrity, a famous monument etc. It's up to you.

To run the package:
clone the repo
change the configuration in the config.json file. The parameters are:
- **"width_mm"**: float = desired dimension in mm
- **"height_mm"**: float = desired dimension in mm
- **"dpi"**: int = Dot Per Inch. It is the resolution of the image (how many pixel per inch). If you want to print it, 300 is advised
- **"image_path"**: str = the path of the image you want to transform
- **"grid_size_mm"**: float = the size of a square of the grid
- **"grid_color"**: str = color of the grid
- **"num_color"**: str = color of the numbers
- **"bw_threshold"**: int = threshold used to convert the image in black and white. The bigger, the more pixel will be converted to white
- **"border_color"**: str = color of the border
- **"border_thickness"**: int = thickness of the border, in px
- **"solution"**: boolean = weither generate the mystery image with shapes drawned or not. true or false, **without quotes**

With your python env in the folder of the config file, run:
python -m mystery_image



Dependencies:
Pillow, Imagehash, pytest, pytest-cov, black, flake8, six
