tikzGUI
=======

A super-minimal GUI for generating simple tikz figures from drawings; This isn't intended to be a comprehensive GUI for tikz; it was intended to be easy to use while taking live notes in LaTeX. Thus, it only draws the most common shapes and allows for some formatting. I don't intend to develop this much; it's mostly for my own convenience.

Written entirely in Python, using Tkinter and ttk. 

##Drawing##

Fairly intuitive. You can draw using the tools given as follows:

####Line tool####
Click on initial point, release at end point

####Rectangle tool####
Click at initial point, release at diagonal point

####Circle tool####
centered

####Generating tikz code####
Click "Show tikz" to generate tikz figure code from drawing. You can edit coordinates and update the figure by clicking "Compile tikz".

Formatting does not show on the preview, but will work when compiled in LaTeX.

TODO: Add formatting preview in the application