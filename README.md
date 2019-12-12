# LicensePlateDetector
Detects license plate of car and recognizes its characters

1.	Introduction 
There is a need for intelligent traffic management systems in order to cope with the constantly increasing traffic on today’s roads. Video based traffic surveillance is one of the key parts of such installations. Beside detection and tracking of vehicles, identification by license plate recognition is important for a variety of applications like access-control, security or traffic monitoring. One of the most crucial cases is identifying the license plate of cars in traffic lights and/or cars beside stop signs.

2.	Problem Statement 
In general, this system consists of two separate parts. First, stop sign and traffic lights detected and second, license plate detection and segmentation are applied on the cars in the frame. The required output of this project is to get the license plate number after checking if there is a traffic light or a stop sign in the picture or in the video.

3.	Parts of the analysis 
Traffic light and stop sign detection:
Detection of stop – sign and traffic light which is performed by template matching method.  In the method, two templates used namely one image of stop sign and one image of traffic light. By performing template matching on the image, the region with max match score extracted and by using a threshold a decision made. If any stop – sign or traffic light found in the image, license plate detection algorithm applied. 
License plate detection and segmentation:
License plate recognition usually contains three steps, namely license plate detection/localization, character segmentation and character recognition:
•	Detect License Plate
The approach used to segment the images is Connected Component Analysis. Connected regions will imply that all the connected pixels belong to the same object. A pixel is said to be connected to another if they both have the same value and are adjacent to each other.
(Assumptions made: width of the license plate region to the full image ranges between 15% and 40% and height of the license plate region to the full image is between 8% & 20%)

•	Perform segmentation of characters
Output of first step is a license plate image detected in a car image. This is provided as input to step 2 and Connected Component Analysis is applied on this image to bound the characters in plate. Each character identified is appended into a list.

•	Train a ML model to predict characters
Model is trained using SVC (4 cross fold validation) with dataset present in directory train20X20. The model is saved as finalized_model.sav which is then loaded to predict each character.

•	Prediction of characters in License Plate
Once the characters of plate obtained and model is trained, the model loaded in order to predict each character.

