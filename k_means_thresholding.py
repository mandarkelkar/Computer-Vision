import cv2
import numpy as np
import copy
import sys

#calculate closest distance from point to the two cluster means
def euclidean(a, b):
	return np.linalg.norm(a-b)


image = cv2.imread(sys.argv[1], 0)

#determine first two cluster means
cluster_means = np.random.randint(0, 255, 2)
# print "Original cluster_means", cluster_means

old_cluster_means = np.zeros(2)

norm = euclidean(cluster_means, old_cluster_means)
# print "starting distance", norm


dist_vec = np.zeros(2)
sum_of_cluster = np.zeros(2)
cluster_grouping = np.zeros(2)

#Iterate until cluster means dont change
while norm > 0:
	#Iterate through all data points
	for column in np.nditer(image):

		for cluster_index, cluster in enumerate(cluster_means):
			#calculate distance to each cluster
			dist_vec[cluster_index] = euclidean(cluster, column)

		#determine which one is closer
		index = np.argmin(dist_vec, axis = 0)
		sum_of_cluster[index] += 1
		#assign pixel to a cluster
		cluster_grouping[index] += column
			
	old_cluster_means = copy.deepcopy(cluster_means)

	for i in range(2):
		cluster_means[i] = cluster_grouping[i] / sum_of_cluster[i]

	# print "new cluster_means", cluster_means, "old_cluster_means", old_cluster_means
	norm = euclidean(cluster_means, old_cluster_means)
	# print "difference", norm

# print "final cluster mean", cluster_means
threshold = np.mean(cluster_means)
print 'Threshold:', threshold

output = copy.deepcopy(image)

#convert greyscale to binary using threshold
for value in np.nditer(output, op_flags=['readwrite']):
	if value[...] <= threshold:
		value[...] = 0;
	else:
		value[...] = 255

print image
print output

cv2.imshow("Output", output)

cv2.imwrite(sys.argv[2],output)
cv2.waitKey(0)