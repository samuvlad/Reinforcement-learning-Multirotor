
import airsim


import cv2
import time
import sys


class OnlyImage:

    def __init__(self, args=()):
        super().__init__()

        self.client = args[0]
        self.action = args[1]

        def printUsage():
            print("Usage: python camera.py [depth|segmentation|scene]")

        self.cameraType = "depth"

        for arg in sys.argv[1:]:
            self.cameraType = arg.lower()

        self.cameraTypeMap = {
            "depth": airsim.ImageType.DepthVis,
            "segmentation": airsim.ImageType.Segmentation,
            "seg": airsim.ImageType.Segmentation,
            "scene": airsim.ImageType.Scene,
            "disparity": airsim.ImageType.DisparityNormalized,
            "normals": airsim.ImageType.SurfaceNormals
        }

        if (not self.cameraType in self.cameraTypeMap):
            printUsage()
            sys.exit(0)

        print(self.cameraTypeMap[self.cameraType])



        self.fontFace = cv2.FONT_HERSHEY_SIMPLEX
        self.fontScale = 0.5
        self.thickness = 2
        self.textSize, baseline = cv2.getTextSize("FPS", self.fontFace, self.fontScale, self.thickness)
        print(self.textSize)
        self.textOrg = (10, 10 + self.textSize[1])
        self.frameCount = 0
        self.startTime = time.clock()
        self.fps = 0

    def takePhoto(self):

        # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
        rawImage = self.client.simGetImage("0", self.cameraTypeMap[self.cameraType])
        if (rawImage == None):
            print("Camera is not returning image, please check airsim for error messages")
            sys.exit(0)
        else:
            png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
            cv2.putText(png, 'FPS ' + str(self.fps), self.textOrg, self.fontFace, self.fontScale, (255, 0, 255), self.thickness)
            cv2.imshow("Depth", png)


            return png




