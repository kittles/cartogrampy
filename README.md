# CartogramPy

CartogramPy is meant for simplifying making Gastner-Newman cartograms using python.
![sample-cartogram](https://github.com/kittles/cartogrampy/blob/master/sample_cartogram.gif)
^^ sample output as density grows inside the green regions

## Getting Started

to generate a cartogram, you need to give the `generate.cartogram` function a 2d input variable matrix, and an image to transform. something like `generate.cartogram(im, z)` where `im` is your image, and `z` is your variable matrix that govern the cartogram.

here is a more in depth example:

```
import numpy as np                                                              
from PIL import Image, ImageDraw                                                
import generate                                                                 
                                                                                
# the image that you will distort into a cartogram                              
#im = Image.open('path/to/image.png')                                           
# for simple test, just use numpy array                                         
w,h = 500,500                                                                   
im = Image.fromarray(np.zeros((w,h)), mode='RGB')                               
d = ImageDraw.Draw(im)                                                          
                                                                                
# the data that will determine the distortion- if you were doing population, say, the points of this 2d a
# the population of whichever region that point falls in.                       
z = np.zeros((w, h)) # or whatever                                              
z += 1 # add a baseline... this seems to help cartograms from distorting        
# as an example, add some square regions with higher "density"                  
squares = [                                                                     
    [100,100,200,200],                                                          
    [250,250,400,400],                                                          
    [100,400,200,450],                                                          
]                                                                               
for square in squares:                                                          
    x1, y1, x2, y2 = square                                                     
    # draw boxes in green. these will get distorted by the transformation                                
    d.line([(x1,y1), (x1,y2), (x2,y2), (x2,y1), (x1,y1)], fill=(0,255,0)) # outline them
    z[y1:y2,x1:x2] += 3 # density is 4 times the baseline of 1                  
im = generate.cartogram(im, z)                                                  
d = ImageDraw.Draw(im)                                                          
# show initial boxes in red for referrence                                      
for square in squares:                                                          
    x1, y1, x2, y2 = square                                                     
    d.line([(x1,y1), (x1,y2), (x2,y2), (x2,y1), (x1,y1)], fill=(255,0,0))       
im.show() 
```

### Prerequisites

This little library requires the command line tool [cart](http://www-personal.umich.edu/~mejn/cart/doc/). It expects that
`cart` command in bash will work. Follow the instructions on cart's page [here](http://www-personal.umich.edu/~mejn/cart/doc/) for how to install it,
as well as `interp`, which comes with it when you download it.

you will also need some good old python library standbys: `numpy` and `PIL`

## Contributing

ill look at any pull request.

## Author

**Patrick Brooks** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to `cart` author
* accidentally developed as a filed attempt to help map carbon emissions
