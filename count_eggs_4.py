import cv2
import numpy as np
import copy
import sys

def find(v):
    if v != parent[int(v)]:
        parent[int(v)] = find(parent[int(v)])
    return parent[int(v)]

def union( x, y):
    x_root = find(x)
    y_root = find(y)
    parent[int(x_root)] = y_root

image = cv2.imread(sys.argv[1], 0)
# 0 = black, 255 = white!!

cv2.imshow('original', image)

(h, w) = image.shape
# print image

# labels matrix replicates original image
labels = np.zeros((h, w))
value = 1

#parents array stores the relationship between labels
parent = np.zeros(h*w)

count = 0
for i in range(h):
	for j in range(w):
		count += 1
		#ignore if background
		if image[i][j] == 255:
			continue

		# set pixels to 0 if not background (to remove edge cases)
		if image[i][j] != 0:
			image[i][j] = 0
			
		#check if left is undefined or background
		if j == 0 or image[i][j-1] == 255:
			#check if top is undef or background
			if i == 0 or image[i-1][j] == 255:
				#new region found
				labels[i][j] = value
				parent[value] = value
				value += 1
			
			else:
				labels[i][j] = labels[i-1][j]
		else:
			#check if top is undefined
			if i == 0 or image[i-1][j] == 255:
				labels[i][j] = labels[i][j-1]
			else:
				#find min of two, set larger label as child of smaller label
				if (labels[i-1][j] - labels[i][j-1]) > 0:
					labels[i][j] = labels[i][j-1]
					union(labels[i-1][j], labels[i][j-1])

				else:
					labels[i][j] = labels[i-1][j]
					union(labels[i][j-1], labels[i-1][j])

# print 'image', image
# print 'labels', labels
# print 'parent', parent, len(parent)

#second pass, clean up image by combining adjacent labels
for i in range(h):
	for j in range(w):
		if image[i][j] == 255:
			continue
		labels[i][j] = find(labels[i][j])

# print 'final lBL', labels

#count number of different labels corresponding to different areas
areas = {}
for i in range(h):
	for j in range(w):
		#default label for background is 0
		if labels[i][j] == 0:
			continue

		if labels[i][j] not in areas:
			areas[labels[i][j]] = 1
		else:
			areas[labels[i][j]] += 1

# print areas
count = 0
for a in areas:
	# print areas[a], sys.argv[2]
	#check if area > n
	if int (areas[a]) > int (sys.argv[2]):
		count += 1
	else:
		#find all labels with value a and set them to 0
		np.place(labels, labels == a, 0)

# print labels
print 'Number of eggs counted:', count
# cv2.waitKey(0)

#RGB matrix
output = np.zeros((h, w, 3))
#dictionary to store label and colour relationship
colours_used = {}
for i in range(h):
	for j in range(w):
		if labels[i][j] != 0:
			if labels[i][j] not in colours_used:
				#choosing a new random colour (avoiding to choose white)
				colours_used[labels[i][j]] = [np.random.randint(0, 255), np.random.randint(0, 255), np.random.randint(0, 254)]
			output[i][j] = colours_used[labels[i][j]]

		#default background color set to white
		else:
			output[i][j] = [255, 255, 255]

# cv2.imshow("final output", output)
# cv2.waitKey(0)
cv2.imwrite(sys.argv[3], output)