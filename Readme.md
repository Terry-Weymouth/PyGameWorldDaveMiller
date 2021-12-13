# An evolution-world model

This project is a transliteration of the Dave Miller's biosim4
into Python using PyGame is an underlying simulation engine.
In this first pass, I attempt to reinterpret a workable subset
of the function of biosim4, focusing on the neural-network, evolution,
simulation of each generation, and visualization of same. Details, especially
in flexibility of configuraton and tracking/recording have been
neglected or glossed over.

See: http://www.millermattson.com/dave/?p=429
And: https://github.com/davidrmiller/biosim4

**Currently, under development, and not working yet. See tests in 
'tests' folder, and main.py in the src folder.**

In an effort to get something up and running that visually matches
David's video presentations, I am assuming that all genes are 4 bytes
in length and that all genomes for a particular simulation
are of equal and fixed length. David's code allows for verying
length genes.

Also, in this early implementation, I am not simulating sexual
reproduction in any way. Reproducion just copies the genes of
the serviving "bugs". Single bit mutations (usually at a small
probability) are supported. See David's video on You Tube.

https://www.youtube.com/watch?v=N3tRFayqVtk
