ThinkAlpha Technical Task 
Developer: Aidan Gray

This was initially developed to be run as a container. Due to unforeseen issues docker did not allow
for the building of the daemon. Because of this the way in which the code is written in here, so i can 
ensure it compiles, does not work for running individual files as well pytest simulatneously. Because of
this to write the unit tests and run them you have to change how you reference files and occasionally
other imports. As a result the code is not easy to pick up where I left off, but I can explain what is
occuring where and why. 