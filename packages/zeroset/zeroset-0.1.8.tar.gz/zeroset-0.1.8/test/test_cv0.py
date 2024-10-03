from zeroset import cv0
import cv2
from zeroset import py0
from zeroset import viz0

files = cv0.glob("../data/", ["*.jpg", "*.png"])
images = cv0.imreads(files)

cv0.imshow(images, mode=cv0.IMSHOW.TK).waitESC()
# print(*dir(list()), sep="\n")

print("Hello")
