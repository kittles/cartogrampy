# Cartogrampy

## overview
meant for simplifying making Gastner-Newman cartograms. this little library
uses the command line tool [cart](http://www-personal.umich.edu/~mejn/cart/doc/). it expects that
`cart` command in bash will work. follow the instructions on cart's page for how to install it,
as well as `interp`, which comes with it when you download it.

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

![sample-cartogram](https://github.com/kittles/cartogrampy/blob/master/sample_cartogram.gif)

## todo
  - explain how to use
  - modularize
  - include tests
