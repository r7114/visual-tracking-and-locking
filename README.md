# visual-tracking-and-locking


How to use:

1. Upload the ino file in './arduino_pwm' to an arduino
2. Connect the signal of the x and y axis servo to pin 11 and 10 respectively
3. Create a conda envirnment from './vt_env.yml'
4. Change some configurations in './movement.py', comments in the file would help you to do so
5. Connect the arduino and the webcam to the computer and run './movement_server.py' and './ui.py' (line 44) with the python in the conda envirnment
6. Run the cells in './main.ipnb' and wait for a pygame window to popup
7. Key Y should toggle AI detection and key E should toggle tracking
8. By enabling tracking and disabling AI, you can move the camera by mouse
9. By enabling bothe tracking and AI, the camera should track automatically



Note:
yolo code taken from https://github.com/theAIGuysCode/tensorflow-yolov4-tflite
