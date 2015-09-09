# kicad-teardrops
KiCAD PCBNEW script to generate teardrops

![Teardrops](https://pbs.twimg.com/media/Brp7OYHIEAA-imY.png)

Run it from the python console (`import teardrops`). To undo, delete all drawings in the copper layers. To re-apply, type `reload(teardrops)`.

This script has no idea about DRC, so it is not a very good tool for production boards. 

If you feel that teardrops is an important feature for you, 
[please vote for it here](https://bugs.launchpad.net/kicad/+bug/593972). Also see [this patch](http://blog.elphel.com/2015/04/trying-out-kicad/) by Mikhail Karpenko.
