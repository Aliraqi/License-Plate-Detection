from skimage.io import imread
from skimage.filters import threshold_otsu
import matplotlib.pyplot as plt
from skimage.feature import match_template
import numpy as np
import sys

#filename = './video12.mp4'

#import cv2
#cap = cv2.VideoCapture(filename)
## cap = cv2.VideoCapture(0)
#count = 0
#while cap.isOpened():
#    ret,frame = cap.read()
#    if ret == True:
#        #cv2.imshow('window-name',frame)
#        cv2.imwrite("./output/frame%d.jpg" % count, frame)
#        count = count + 1
#        if cv2.waitKey(10) & 0xFF == ord('q'):
#            break
#    else:
#        break
#cap.release()
#cv2.destroyAllWindows()

# car image -> grayscale image -> binary image
#import imutils
#car_image = imread("./output/frame%d.jpg"%(count-1), as_gray=True)
#car_image = imutils.rotate(car_image, 270)
car_image = imread("./dataset/car.png", as_gray=True)
gray_car_image = car_image * 255
# it should be a 2 dimensional array
print(car_image.shape)

# detect A STOP SIGN AND TRAFFIC LIGHTS FIRST 
# IF THERE IS NO STOP SIGN OR TRAFFIC LIGHTS BREAK THE OPERATION
# IF THERE IS A STOP SIGN OR TRAFFIC LIGHTS CONTINUE AND DETECT LICENSE PLATE
stop_image = imread("./dataset/stop_template.jpg", as_gray=True)
gray_stop_image = stop_image * 255

trafficlight_image = imread("./dataset/trafficlight_template.jpg", as_gray=True)
gray_trafficlight_image = trafficlight_image * 255

result_stop = match_template(car_image, gray_stop_image)
max_stop = np.argmax(result_stop)

result_trafficlight = match_template(car_image, gray_trafficlight_image)
max_trafficlight = np.argmax(result_trafficlight)

stop_threshold = 2000
trafficlight_threshold = 15000

if max_stop <= stop_threshold:
    ij_stop = np.unravel_index(max_stop, result_stop.shape)
    x_stop, y_stop = ij_stop[::-1]

    
if max_trafficlight <= trafficlight_threshold:
    ij_trafficlight = np.unravel_index(max_trafficlight, result_trafficlight.shape)
    x_trafficlight, y_trafficlight = ij_trafficlight[::-1]



if ('ij_stop' in locals()) or('ij_trafficlight' in locals()):
    print('A Stop Sign or Traffic Light Detected')
    
else:
    print('No Stop Sign or Traffic Light Detected')
    sys.exit(1)
    


fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(gray_car_image, cmap="gray")
threshold_value = threshold_otsu(gray_car_image)
binary_car_image = gray_car_image > threshold_value
# print(binary_car_image)
ax2.imshow(binary_car_image, cmap="gray")
# ax2.imshow(gray_car_image, cmap="gray")
plt.show()

# CCA (finding connected regions) of binary image


from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# this gets all the connected regions and groups them together
label_image = measure.label(binary_car_image)

# print(label_image.shape[0]) #width of car img

# getting the maximum width, height and minimum width and height that a license plate can be
plate_dimensions = (0.03*label_image.shape[0], 0.08*label_image.shape[0], 0.15*label_image.shape[1], 0.3*label_image.shape[1])
plate_dimensions2 = (0.08*label_image.shape[0], 0.2*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
min_height, max_height, min_width, max_width = plate_dimensions
plate_objects_cordinates = []
plate_like_objects = []

fig, (ax1) = plt.subplots(1)
ax1.imshow(gray_car_image, cmap="gray")
flag =0
# regionprops creates a list of properties of all the labelled regions
for region in regionprops(label_image):
    # print(region)
    if region.area < 50:
        #if the region is so small then it's likely not a license plate
        continue
        # the bounding box coordinates
    min_row, min_col, max_row, max_col = region.bbox
    # print(min_row)
    # print(min_col)
    # print(max_row)
    # print(max_col)

    region_height = max_row - min_row
    region_width = max_col - min_col
    # print(region_height)
    # print(region_width)

    # ensuring that the region identified satisfies the condition of a typical license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        flag = 1
        plate_like_objects.append(binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                         max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                       linewidth=2, fill=False)
        ax1.add_patch(rectBorder)
        # let's draw a red rectangle over those regions
if(flag == 1):
    # print(plate_like_objects[0])
    plt.show()




if(flag==0):
    min_height, max_height, min_width, max_width = plate_dimensions2
    plate_objects_cordinates = []
    plate_like_objects = []

    fig, (ax1) = plt.subplots(1)
    ax1.imshow(gray_car_image, cmap="gray")

    # regionprops creates a list of properties of all the labelled regions
    for region in regionprops(label_image):
        if region.area < 50:
            #if the region is so small then it's likely not a license plate
            continue
            # the bounding box coordinates
        min_row, min_col, max_row, max_col = region.bbox
        # print(min_row)
        # print(min_col)
        # print(max_row)
        # print(max_col)

        region_height = max_row - min_row
        region_width = max_col - min_col
        # print(region_height)
        # print(region_width)

        # ensuring that the region identified satisfies the condition of a typical license plate
        if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
            # print("hello")
            plate_like_objects.append(binary_car_image[min_row:max_row,
                                      min_col:max_col])
            plate_objects_cordinates.append((min_row, min_col,
                                             max_row, max_col))
            rectBorder = patches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, edgecolor="red",
                                           linewidth=2, fill=False)
            ax1.add_patch(rectBorder)
            # let's draw a red rectangle over those regions
    # print(plate_like_objects[0])
    plt.show()