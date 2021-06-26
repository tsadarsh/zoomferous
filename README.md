# Zoomferous

<p align="center">
  <img width="215" height="225" src="https://user-images.githubusercontent.com/66778010/121997682-5baab700-cdc8-11eb-9647-0f9eed096d69.png">
  <img width="225" height="225" src="https://user-images.githubusercontent.com/66778010/123508061-be366980-d68a-11eb-90e4-3283fa6cb681.png">
</p>

Zoomferous emulates blackboard writing, "Zoomferous". With no extra hardware this software uses the webcam of the device to read the content of paper/board/workspace and applies filters before presenting the masked content.

The user brings the workspace which can be a notebook page, board, A4 paper in the view of a webcam. Next, the four corner points of the workspace are selected to crop the required portion. 2D perspective and affine transformation transforms the quadrilateral workspace region to a square window.

The transformed frame is now fed into an optimizer which enhances and removes the noise from the frame. Then we apply a dynamic filter which abstracts the given image into a binary mask making the data appear such that it would be on a black board to the student. The filter removes the noise from the image and the result is a clean blackboard-like view. 

## Demo video

https://user-images.githubusercontent.com/66778010/123508551-bd530700-d68d-11eb-9e78-20cd865800bc.mp4

Watch the full video in [YouTube](https://www.youtube.com/watch?v=_3xY4cEWazU)

## User manual
 - #### Select Page corners:
      Single click Left mouse button on **Zoomferous** window.

 - #### Switch back to corner points selctiong:
      Press key 'q' once.

 - #### Change ink color:
      'w' - (default) white
      'b' - blue
      'r' - red
      'g' - green

 - #### Quit
      Press key 'q' twice

## Requirements
 - Python 3.6 or above
 - OpenCV
 - Sckit-image
 - Webcam
