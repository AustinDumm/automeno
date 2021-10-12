# Automeno

A randomized music generation builder in Python.

Contains a number of components which each take input (including musical data such as notes and collections of notes, and more traditional programming data such as files, characters, booleans, etc) and transform them into an output. Many of these components can also generate a random sequence of data to utilize in other components. The input and outputs for these components can be connected to each other and to special components that generate output notes in midi format. This machine of components is then run to output a midi file of a specified length.
