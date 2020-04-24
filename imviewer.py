from skimage.viewer import ImageViewer
from skimage.io import imread
img = imread('C:/Users/dbstn/Desktop/snow.png') #이미지를 어떤걸 선택할지 여러가지 필요하다 랜덤선택
view = ImageViewer(img)
view.show()