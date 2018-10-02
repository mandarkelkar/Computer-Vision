import cv2
import numpy as np
import copy
import sys

def euclidean(a, b):
	return np.linalg.norm(a-b)

image = cv2.imread(sys.argv[1], 0)
h, w = image.shape
n = int(sys.argv[2])

avg = cv2.blur(image, (n, n), -1)
cv2.imshow ('avg', avg)

#choose first two cluster means
#cluster_means = [[image_cluster1, image_cluster2],[average_cluster1, average_cluster2]]
cluster_means = np.random.randint(0, 255, (2,2))
# print "Original cluster_means", cluster_means
old_cluster_means = np.zeros((2, 2))

norm = euclidean(cluster_means, old_cluster_means)
# print "starting distance", norm

#stack the two matrices depthwise
image_data = np.dstack((image, avg))

#stores distances from matrix to each of the cluster means
dist_vec = np.zeros((2,2))

#used for finding new cluster mean
sum_of_cluster = np.zeros((2,2))
cluster_grouping = np.zeros((2,2))

#stores indices of minimum distances for image, average
index = np.zeros(2)

#Iterate until cluster means dont change
while norm > 0:
	#Iterate through all data points
	for i in range(h):
		for j in range(w):
			#cluster_means[i][j]: first value = image, second = average.
			for cluster_index, cluster in enumerate(cluster_means):
				for ind in range(2):
					dist_vec[cluster_index][ind] = euclidean(cluster[ind], image_data[i][j][cluster_index])
				#logic:
				# dist_vec[0][0] = euclidean(cluster[0], image_data[i][j][0])
				# dist_vec[0][1] = euclidean(cluster[1], image_data[i][j][0])
				# dist_vec[1][0] = euclidean(cluster[0], image_data[i][j][1])
				# dist_vec[1][1] = euclidean(cluster[1], image_data[i][j][1])

			#calculate closest distance for image as well as average
			for item in range(2):
				index[item] = np.argmin(dist_vec[item], axis = 0)

			#assign pixel to cluster
			for item in range(2):
				cluster_grouping[int(item)][int(index[int(item)])] += image_data[i][j][int(item)]
				sum_of_cluster[item] [int(index[item])] += 1
	
	old_cluster_means = copy.deepcopy(cluster_means)
	for i in range(2):
		for j in range(2):
			cluster_means[i][j] = cluster_grouping[i][j] / sum_of_cluster[i][j]

	# print "new cluster_means", cluster_means
	# print "old_cluster_means", old_cluster_means
	norm = euclidean(cluster_means, old_cluster_means)
	# print "difference", norm

# print "final cluster mean", cluster_means
threshold = np.mean(cluster_means, axis=1)
threshold = np.mean(threshold)
print 'Final Threshold:', threshold

output = copy.deepcopy(image)

#convert greyscale to binary using threshold
for value in np.nditer(output, op_flags=['readwrite']):
	if value[...] <= threshold:
		value[...] = 0;
	else:
		value[...] = 255


kernal2 = np.ones((3, 3), np.float32)/9
cv2.imshow("Output", output)
cv2.imwrite(sys.argv[3],output)
cv2.waitKey(0)