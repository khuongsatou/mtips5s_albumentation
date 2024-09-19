import cv2
from matplotlib import pyplot as plt
import numpy as np
MAX_FEATURES = 500
GOOD_MATCH_PERCENT = 0.15
img_template = cv2.imread('images/invoice/alignment.jpg')
img_need_aligned = cv2.imread('images/invoice/alignmented.jpg')


def visualize(image):
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(image)
    plt.show()

def visualize_v2(img_form,img_scan):
    # Hiển thị ảnh.
    plt.figure(figsize = [20, 10])
    plt.subplot(121); plt.axis('off'); plt.imshow(img_form[:, :, ::-1]); plt.title("Ảnh mẫu")
    plt.subplot(122); plt.axis('off'); plt.imshow(img_scan[:, :, ::-1]); plt.title("Ảnh cần xử lý")
    plt.show()

def gray(image):
    im1Gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return im1Gray

def create_orb(im1Gray):
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1Gray, None)
    # keypoints2, descriptors2 = orb.detectAndCompute(im2Gray, None)
    return keypoints1, descriptors1

def match_feature(im1,im2,im1Gray,im2Gray):
    keypoints1, descriptors1 = create_orb(im1Gray)
    keypoints2, descriptors2 = create_orb(im2Gray)
    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    
    matches = matcher.match(descriptors1, descriptors2, None)
    # print("In File: read_img.py, Line: 31",matches)
    # Sort matches by score
    # matches.sort(key=lambda x: x.distance, reverse=False)
    matches = sorted(matches,key=lambda x: x.distance, reverse=False)
    
    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]
    
    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)
    
    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)
    
    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt


def find_homography(image,points1,points2):
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

def wraping_image(im1, im2,h):
    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

img_template_gray = gray(img_template)
img_need_aligned_gray = gray(img_need_aligned)
match_feature(img_template,img_need_aligned,img_template_gray,img_need_aligned_gray)
# keypoints1,descriptors1 = create_orb(img_template)
# print("In File: read_img.py, Line: 27",keypoints1)
# print("In File: read_img.py, Line: 28",descriptors1)

# visualize(img_template)
visualize_v2(img_template,img_need_aligned)
