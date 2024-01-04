ThinkAlpha Technical Task 
Developer: Aidan Gray


Docker
- Docker container has caused some issues with development. Mainly testing. Could not resolve the issue
on my device. To continue developing the program I had to change the way you would write the code to run
it outside of the container. Because of this the ability to run the unit_tests using pytest while also 
writing the code that will pull and store the data was not possible. When running the tests they have to be
in the proper format to run outside of the container. But to be able to run the individual files to pull and 
store the data you have to change the way in which you reference othre files. As a result changing of the
code is neccessary prior to running the tests. 