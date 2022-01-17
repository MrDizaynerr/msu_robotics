import cv2
from PIL import Image
import numpy as np

############### Tracker Types #####################

#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()


full_map = np.zeros((12000, 12000), np.uint8)
cv2.imwrite('full.png', full_map)
full_map = cv2.imread('full.png')
ukaz = (6000, 6000)
def plus(a,b): 
	return (int(a[0]+b[0]), int(a[1]+b[1]))


cap = cv2.VideoCapture('aaaa.mp4')
success, frame = cap.read()
height, width = frame.shape[0], frame.shape[1]
print(height)
print(width)

speed = 1
change_vec = (0, 0)
old_vec = (0, 0)
new_vec = (0, 0)

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


def find_new(frm):
	pass
success = True
tmr = 0
while True:
	#tracker = cv2.TrackerMOSSE_create()
	tracker = cv2.TrackerCSRT_create()
	#tracker = cv2.TrackerBoosting_create()
	#tracker = cv2.TrackerMIL_create()
	#tracker = cv2.TrackerKCF_create()
	#tracker = cv2.TrackerTLD_create()
	#tracker = cv2.TrackerMedianFlow_create()
	success, frame = cap.read()
	height, width = frame.shape[0], frame.shape[1]
	bbox = cv2.selectROI("Tracking",frame, False)
	try:
		tracker.init(frame, bbox)
	except:
		cv2.imwrite('full.png', full_map)
		exit()

	cv2.imwrite('full.png', full_map)
	old_vec = (bbox[0], bbox[1])

	while success:
	    timer = cv2.getTickCount()
	    success, img = cap.read()
	    success, bbox = tracker.update(img)

	    tmr+=1
	    if success and tmr==speed:
	    	print(bbox)
	    	tmr = 0
	    	new_vec = (bbox[0], bbox[1])
	    	change_vec = (int(old_vec[1]-new_vec[1]), int(old_vec[0]-new_vec[0]))
	    	old_vec = new_vec
	    	print(change_vec)
	    	try:
	    		ukaz = plus(ukaz, change_vec)
	    		full_map[ukaz[0]:ukaz[0]+img.shape[0], ukaz[1]:ukaz[1]+img.shape[1],] = img
	    	except:
	    		cv2.imwrite('res.png', full_map)

	    if success:
	        drawBox(img,bbox)
	        #print(bbox)
	    else:
	    	cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
	    	break

	    cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
	    cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
	    cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);


	    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
	    if fps>60: myColor = (20,230,20)
	    elif fps>20: myColor = (230,20,20)
	    else: myColor = (20,20,230)
	    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);

	    cv2.imshow("Tracking", img)

	    """if bbox[0]>(width-width//10) or bbox[1]>(height-height//10) or bbox[0]<width//20 or bbox[1]<height//20:
	    	print('This moment!')
	    	delta_x = width//6
	    	delta_y = height//6
	    	success = False
	    	while not success:
	    		success, img = cap.read()
	    		tracker = cv2.TrackerCSRT_create()
	    		tracker.init(frame, bbox)
	    		success, _ = tracker.update(img)
	    		print(success)"""
	    if bbox[0]>(width-width//100) or bbox[1]>(height-height//8) or bbox[0]<width//100 or bbox[1]<height//10:
	    	break

	    if cv2.waitKey(1) & 0xff == ord('q'):
	    	cv2.imwrite('full.png', full_map)
	    	exit()