# CrappySkype

This will implament a crapy version of skype that will send and display video to peers.
A couple different compression algorithuims will be used to reduced network resoucres.
These will be compared to at the end and presented on.

run with:
      ./videoTest.py [local ip address of peer] for connecting to a peer
   or ./videoTest.py for a local loop back

This utilizes openCV 3 and is organized in two threads: the video recorder, and the video displayer.
Each thread starts life by listening to a socket (port 5002) or connecting to one. 

Capture thread: 
      This thread reads data from the the VideoCapture object and gradually formats an image into a string of bytes. To do
      this the image is first flipped on the Y-axis to give us the correct oritation of the image when viewed on a screen 
      facing the user. Now the data has to be reformatted in the numpy framework I'm using. Numpy allows faster computation of 
      huge datasets than the native python comands through use of c bindings instead of pure python. This reduces the amount 
      'crap' the interprater has to go through. Due to the images size of is then sent row by row (to allow high cache hits)
      to the peer as a string of bytes.
      
Display thread:
      This thread reads bytes in from the network, stiches them together again, reformats the string of bytes of a picture and
      dispalys it. To kill the program simply hit 'q' while on foucus of the display


