# Zoomferous

<p align="center">
  <img width="215" height="225" src="https://user-images.githubusercontent.com/66778010/121997682-5baab700-cdc8-11eb-9647-0f9eed096d69.png">
</p>

We bring to you a software which emulates blackboard writing, "Zoomferous". With no extra hardware this software uses the webcam of the device to read the content of paper/board/workspace and applies filters before presenting the masked content.

The user brings the workspace which can be a notebook page, board, A4 paper in the view of a webcam. Next, the four corner points of the workspace are selected to crop the required portion. 2D perspective and affine transformation transforms the quadrilateral workspace region to a square window.

The transformed frame is now fed into an optimizer which enhances and removes the noise from the frame. Then we apply a dynamic filter which abstracts the given image into a binary mask making the data appear such that it would be on a black board to the student. The filter removes the noise from the image and the result is a clean blackboard-like view. 

## Demo video

https://user-images.githubusercontent.com/66778010/122145451-e647f080-ce72-11eb-8662-d1dd66b7f2b9.mp4

What the full demo video [here](https://www.youtube.com/watch?v=xKsz5qfVB2A).

#### Select Page corners:
Single click Left mouse button on **Zoomferous** window.

#### Switch back to corner points selctiong:
Press key 'q' once.

#### Quit
Press key 'q' twice
