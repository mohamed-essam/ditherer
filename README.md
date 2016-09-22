# Ditherer
Dithers an image into a given color palette (defaults to black and white)

##Usage

A POST request is sent to the server using the following parameters:

Key|Required|Value
---|--------|-----
file|required|An image file containing the image to be processed, link to image can be provided instead
link|optional|Direct link to image file, to be processed, if file is present this option is ignored
algorithm|optional|An integer ranging from 0-7 to select the processing algorithm (Default: 0)
palette|optional|A JSON list containing colors to be used in the process (Default: [[0,0,0],[255,255,255]])

Value|Algorithm|Value|Algorithm
-----|---------|-----|---------
0|3-row Sierra|1|2-row Sierra
2|Sierra Lite|3|Burkes
4|Atkinson|5|Stucki
6|Jarvice-Judice-Ninke|7|Floyd Steinberg

#Algorithms

![Approve](http://i.imgur.com/Ihvw0lL.jpg)

# Example

This image was processed using a pallete of 8 colors and using the 3-row Sierra algorithm

![Original vs Dithered]
(http://i.imgur.com/g7mOuuZ.jpg)

# Demo
[Heroku Demo](http://young-island-22764.herokuapp.com)
![Heroku Demo Screenshot](http://i.imgur.com/Hu1oYaz.png)
