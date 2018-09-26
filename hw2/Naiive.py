from PIL import Image
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def overlap(seg1, seg2, connect='4'):
	if connect == '4':  #4-connected
		return False if seg1[1] < seg2[0] or seg2[1] < seg1[0] else True
	else:               #8-connected
		return False if seg1[1] < (seg2[0]-1) or seg2[1] < (seg1[0]-1) else True

def getsegments(row, col, data):
	segments = [list() for i in range(row)]
	for i in range(row):
		j = 0
		while j<col:
			while j<col and data[i][j]==0: j+=1
			if j==col: break
			head = j
			while j<col and data[i][j]==255: j+=1
			segments[i] += [(head, j-1, i)]
	return segments

def groupup(segments, row):
	segNum, flag, belong, index, flattened = 0, True, list(), list(), list()
	for i, segList in enumerate(segments):
		index.append(segNum)
		num = len(segList)
		segNum += num
		for j in range(num):
			belong.append(index[i] + j)
			flattened.append(segments[i][j])
	while flag:
		flag = False
		for i in range(1, row):
			for nowX, now in enumerate(segments[i]):
				for lastX, last in enumerate(segments[i-1]):
					last_index, now_index = lastX + index[i-1], nowX + index[i]
					if overlap(last, now) and belong[last_index] != belong[now_index]:
						if belong[last_index] < belong[now_index]: belong[now_index], flag = belong[last_index], True
						else: belong[last_index], flag = belong[now_index], True
		if not flag: break
		for i in range(row-2, -1, -1):
			for nowX, now in enumerate(segments[i]):
				for lastX, last in enumerate(segments[i+1]):
					last_index, now_index = lastX + index[i+1], nowX + index[i]
					if overlap(last, now) and belong[last_index] != belong[now_index]:
						if belong[last_index] < belong[now_index]: belong[now_index], flag = belong[last_index], True
						else: belong[last_index], flag = belong[now_index], True
	groupLen, groupKey, groups = 0, dict(), []
	for i in range(segNum):
		if belong[i] not in groupKey:
			groupKey[belong[i]] = groupLen
			groups.append([flattened[i]])
			groupLen += 1
		else: groups[groupKey[belong[i]]].append(flattened[i])
	return groups


#Main Program
im = Image.open('output/binarized.bmp')
(width, height), data_array = im.size, numpy.array(im)
#get groups
segments = getsegments(height, width, data_array)
groups = groupup(segments, height)
print(len(groups))
new_groups = [group for group in groups if len(group) >= 500]
print(len(new_groups))

#drawing
plt.figure(figsize=(5,5))
fig, ax = plt.subplots()
ax.imshow(im)

for group in new_groups:
	xmin, ymin, xmax, ymax, xavg, yavg, count = width, height, -1, -1, 0, 0, 0
	for seg in group:
		xmin, ymin, xmax, ymax = min(xmin, seg[0]), min(ymin, seg[2]), max(xmax, seg[1]), max(ymax, seg[2])
		xavg, yavg, count = xavg + (seg[1]+seg[0])*(seg[1]-seg[0]+1)/2, yavg + seg[2]*(seg[1]-seg[0]+1), count + (seg[1]-seg[0]+1)
	xavg, yavg = xavg // count, yavg // count
	ax.add_patch(patches.Rectangle((xmin, ymin), xmax-xmin, ymax-ymin, linewidth=3, edgecolor='r', facecolor='none')) #draw box
	plt.plot(xavg, yavg, 'b+', linewidth=28, markersize=20) #draw cross

plt.axis('off')
plt.savefig('output/connected_marked.jpg')
im.close()
