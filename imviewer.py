# from skimage.viewer import ImageViewer
# from skimage.io import imread
# img = imread('C:/Users/dbstn/Desktop/snow.png') #이미지를 어떤걸 선택할지 여러가지 필요하다 랜덤선택
# view = ImageViewer(img)
# view.show()

import numpy as np
import cv2
import screeninfo

screen_id = 0

# get the size of the screen
screen = screeninfo.get_monitors()[screen_id]
width, height = screen.width, screen.height

image = cv2.imread('C:/Users/dbstn/Desktop/snow.png')

window_name = 'projector'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                      cv2.WINDOW_FULLSCREEN)
cv2.imshow(window_name, image)
cv2.waitKey()
cv2.destroyAllWindows()