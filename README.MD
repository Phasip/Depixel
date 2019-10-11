Depixling urls from chrome
========
Saw a pixeled url in a presentation. I attempted
to read it by brute-forcing different options and seeing
which one matches best.

With some brain power one can figure out the correct one given
the results - but - it is bad at identifying "." so it won't
give the right value.

Use create_t1.py to "train" (i.e match the font size, color, image size etc) against
the given pixeled image (assuming the image starts with known text: "https://").

Then put the result in variable i of bf_t1.py and brute force the rest.

Note: This is a POC and horribly slow. It works if used correctly.
Note: No AI here, only bruteforce with some measurments to identify if it's going the right direction.

## Lessons learned ##
* Don't pixel urls, just put a black box over them!
* Dont use python for things that need some speed

