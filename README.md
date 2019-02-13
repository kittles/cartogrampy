# Cartogrampy

## overview
. 

`cart` and `interp` generate a grid of point displacements, which are then used with PIL to
create a transformation mesh, which renders the final cartogram. probably worth tweaking the
interpolation methods to see what looks best depending on the case.


the absolute and relative scale and differences within the data that governs the cartogram
seems to matter, and i encountered some weird artifacts when the max data > 6x the min. also,
it seems to help to add a small baseline amount to all the data.

## sample output
here is an example of a 500x500 image, with a single square region where the input variable
is higher than everywhere else. it varies from 2 to 99 as the gif goes from start to finish.
the red square represents the original area, and the green is the resulting area from the 
cartogram. its good that the green square gets bigger, while retaining some squarelike properties
as it grows. its bad that it starts to generate weird artifacts about halfway through. in this
example, ive colored the entire image with points that vary their rgb values so as to make the 
overall effect on all points easier to see.




# CartogramPy

CartogramPy is meant for simplifying making Gastner-Newman cartograms using python.
![sample-cartogram](https://github.com/kittles/cartogrampy/blob/master/sample_cartogram.gif)

## Getting Started

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
