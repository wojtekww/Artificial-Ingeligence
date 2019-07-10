
import cv2
from matplotlib import pyplot as plt

img1 = cv2.imread('image11.jpg', 0)          # queryImage
img2 = cv2.imread('image12.jpg', 0)          # trainImage

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)
# BFMatcher with default params

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k=2)

# Apply ratio test
good = []
for m, n in matches:
    if m.distance < 0.65*n.distance:
        good.append([m])

#cv2.drawMatchesKnn expects list of lists as matches.

# img1=cv2.drawKeypoints(img1,kp1,img1)
# img2=cv2.drawKeypoints(img2,kp2,img2)
img1=cv2.drawKeypoints(img1,kp1,img1,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2=cv2.drawKeypoints(img2,kp2,img2,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img3 = cv2.drawMatchesKnn(img1, kp1, img2, kp2, good, None, flags=2)
# plt.imshow(img3)
# plt.show()

#img = cv2.imread('image12.jpg')
#gray= cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
#kp = sift.detect(gray,None)
#img1=cv2.drawKeypoints(img1,kp1,img1)
#img2=cv2.drawKeypoints(img2,kp2,img2)

# cv2.imwrite('sift_keypoints.jpg',img)

cv2.imwrite('wynik52.jpg',img3)
cv2.imwrite('punkty12.jpg',img1)
cv2.imwrite('punkty22.jpg',img2)