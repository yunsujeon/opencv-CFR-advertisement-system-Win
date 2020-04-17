from skimage.viewer import ImageViewer
from skimage.io import imread
img = imread('C:/Users/dbstn/Desktop/snow.png') #path to IMG
view = ImageViewer(img)
view.show()