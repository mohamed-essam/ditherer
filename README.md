# Ditherer
Dithers an image into a given color palette (defaults to black and white)

##Usage

A POST request is sent to the server using the following parameters:

Key|Required|Value
---|--------|-----
file|required|An image file containing the image to be processed
algorithm|optional|An integer ranging from 0-7 to select the processing algorithm (Default: 0)
palette|optional|A JSON list containing colors to be used in the process (Default: [[0,0,0],[255,255,255]])

#Algorithms

[Sierra](http://i.imgur.com/DBz7XKR.png)
, [2-row Sierra](http://i.imgur.com/p7W1NrG.png)
, [Sierra Lite](http://i.imgur.com/0cPO46t.png)
, [Burkes](http://i.imgur.com/rNcBA7Q.png)
, [Atkinson](http://i.imgur.com/8FWK13D.png)
, [Stucki](http://i.imgur.com/2o8w15c.png)
, [Jarvis-Judice-Ninke](http://i.imgur.com/CDaYt82.png)
, [Floyd Steinberg](http://i.imgur.com/H3nlIxs.png)

# Example

This image was processed using a pallete of 8 colors and using the 3-row Sierra algorithm

![Original Image]
(http://imgur.com/LPIrTfq.png)

![Dithered Image]
(http://imgur.com/n7XDr6m.png)
