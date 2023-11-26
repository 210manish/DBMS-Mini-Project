import cv2
# from cv2 import MSER_create
from model import fingerprint_feature_extractor
import fingerprint_enhancer								# Load the library
import urllib.request
import numpy as np

def compare_func(img1,img2):
    # img1 = img1.decode()
    # print(img1)
    # img1 = cv2.imread(img1,0)  # read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library

    img1 = fingerprint_enhancer.enhance_Fingerprint(img1)
    # cv2.imshow('enhanced_image_1', img1);
    # cv2.waitKey(0)

    FeaturesTerminations1, FeaturesBifurcations1 = fingerprint_feature_extractor.extract_minutiae_features(img1,
                                                                                                           spuriousMinutiaeThresh=10,
                                                                                                           invertImage=False,
                                                                                                           showResult=True,
                                                                                                           saveResult=True)

    # URL of the image to be read
    url = img2

    # Read the image from the URL using urllib
    with urllib.request.urlopen(url) as url_response:
        img_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
        img2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # img2 = cv2.imread(img2, 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
    img2 = fingerprint_enhancer.enhance_Fingerprint(img2)
    # cv2.imshow('enhanced_image_2', img2);
    # cv2.waitKey(0)

    FeaturesTerminations2, FeaturesBifurcations2 = fingerprint_feature_extractor.extract_minutiae_features(img2,
                                                                                                           spuriousMinutiaeThresh=10,
                                                                                                           invertImage=False,
                                                                                                           showResult=True,
                                                                                                           saveResult=True)
    if ((FeaturesTerminations1 == FeaturesTerminations2 and FeaturesBifurcations1 == FeaturesBifurcations2) or (
            img1.data == img2.data)):
        print("Fingerprints match!!")
        return 1
    else:
        print("Fingerprints DO NOT match!!")
        return 0

#
# if __name__ == '__main__':
#     img1 = cv2.imread('1.jpg', 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
#     img1 = fingerprint_enhancer.enhance_Fingerprint(img1)
#     cv2.imshow('enhanced_image_1', img1);
#     cv2.waitKey(0)
#
#     FeaturesTerminations1, FeaturesBifurcations1 = fingerprint_feature_extractor.extract_minutiae_features(img1, spuriousMinutiaeThresh=10, invertImage = False, showResult=True, saveResult = True)
#
#     # URL of the image to be read
#     url = 'https://i.ibb.co/dDjg86g/1-jpg.jpg'
#
#     # Read the image from the URL using urllib
#     with urllib.request.urlopen(url) as url_response:
#         img_array = np.asarray(bytearray(url_response.read()), dtype=np.uint8)
#         img2 = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
#
#     # img2 = cv2.imread(img2, 0)				# read the input image --> You can enhance the fingerprint image using the "fingerprint_enhancer" library
#     img2 = fingerprint_enhancer.enhance_Fingerprint(img2)
#     cv2.imshow('enhanced_image_2', img2);
#     cv2.waitKey(0)
#
#     FeaturesTerminations2, FeaturesBifurcations2 = fingerprint_feature_extractor.extract_minutiae_features(img2, spuriousMinutiaeThresh=10, invertImage = False, showResult=True, saveResult = True)
#     if ((FeaturesTerminations1 == FeaturesTerminations2 and FeaturesBifurcations1 == FeaturesBifurcations2) or (img1.data == img2.data)):
#         print("Fingerprints match!!")
#     else:
#         print("Fingerprints DO NOT match!!")