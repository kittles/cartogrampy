# Cartogrampy
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
