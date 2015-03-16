# Some notes about Python and Gimp #

Python is a not the primary language to use Gimp, lisp (or Scheme) is - and it shows.  In addition the documentation for Gimp is not stellar, finding out what parameters to pass or what methods an object will accept is a hit or miss affair.

On the other hand, Gimp is pretty robust and often gives meaningful error messages, you can work out the kinks reasonably quickly.

To test your Python-Fu program copy it into ~/.gimp-2.x/plug-ins and start gimp with "gimp --verbose" at the command line.  If there was any problems compiling or loading your plug-in you should see a message then.  Afterwards, you normally do not need to restart Gimp to run your program again after modifying it, it reloads it automatically (yay).

Python "print" statements work and output to the console, and is useful for debugging.

If you find some Gimp code on the internet be careful that some functions are deprecated and should be used.  Usually the documentation mentions what **should** be used and it should be obvious how to modify the code to work.

In Python some methods begin with "gimp.", others with "pdb.". You should use "gimp." when possible, but there aren't many functions there, everything else will start with "pdb." which stands for "Procedure Database".

# Note #

These notes are mostly for me, but if you find them useful, that's great too.