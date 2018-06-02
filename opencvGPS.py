print("~Sciengit Codecell~")

import serial
import cv2
import numpy as np
from numpy import *

def main():
	# serial connection
	data = serial.Serial('com3', 57600) # change this according to your port
	# data streaming
	k = data.readline()
	print(k)

	# opencv stuff
	cap = cv2.VideoCapture(0)
	min_area = 100**2

	while (cap.isOpened()):
		_, image = cap.read()
		#image = cv2.resize(image, (0,0), fx=0.5, fy=0.5)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
		#cv2.imshow('image', image)
		#cv2.imshow('gray', gray)
		#cv2.imshow('hsv', hsv)
		lower_red = np.array([80,140,0])
		upper_red = np.array([192,255,200])
		#lower_red = np.array([158,65,0])
		#upper_red = np.array([175,255,256])    
        
		mask = cv2.inRange(hsv, lower_red, upper_red) 
		result = cv2.bitwise_and(image, image, mask=mask)
		result = cv2.GaussianBlur(result, (15,15), 0)
		res_gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
        
		#cv2.imshow('result', result)
		#canny = cv2.Canny(gray, 50, 150)
		#cv2.imshow('canny', canny)
        
		########################################################################
		_, threshold = cv2.threshold(res_gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		_,cnts,_ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
		for contour in cnts:
			area = cv2.contourArea(contour)
			if area>min_area:
				# print GPS data
				k = data.readline()
				try:
					print(k)
				except:
					print("GPS FAILED TO UPDATE")
				#endtry
				# calculating the centroid
				moment = cv2.moments(contour)
				cx = int(moment['m10']/moment['m00'])
				cy = int(moment['m01']/moment['m00'])
				# make a rectangle bounding the contour
				[x, y, w, h] = cv2.boundingRect(contour)
				cv2.rectangle(image, (x, y), (w+x, h+y), (0,255,0), 2)
				#cv2.circle(image, (cx,cy), 5, (255,255,0), 2)
				cropped =image[y:y+h, x:x+w]
				cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
			#endif
		#endfor

		cv2.imshow('image', image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		#endif

	#endwhile
	cv2.destroyAllWindows()
	cap.release()
	return
#enddef

if __name__ == '__main__':
	main()
