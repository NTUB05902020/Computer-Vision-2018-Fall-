from PIL import Image
import numpy
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def overlap(seg1, seg2, connect='4'):
	if connect == '4':  #4-connected
		return False if seg1[1] < seg2[0] or seg2[1] < seg1[0] else True
	else:               #8-connected
		return False if seg1[1] < (seg2[0]-1) or seg2[1] < (seg1[0]-1) else True

def groupup(row, col, data):
	segments, find_group, groups = [list() for i in range(row)], dict(), []
	for i in range(row):
		j = 0
		while j<col:
			while j<col and data[i][j]==0: j+=1
			if j==col: break
			head = j
			while j<col and data[i][j]==255: j+=1
			segments[i] += [(head, j-1, i)]
	#print(segments)
	#to right-down
	for seg in segments[0]:
		#print(groups)
		new_set = set()
		new_set.add(seg)
		groups, find_group[seg] = groups + [new_set], new_set
	for i in range(1, row):
		for now_idx, now in enumerate(segments[i]):
			found_group = False
			for last_idx, last in enumerate(segments[i-1]):
				#print(i, now_idx, last_idx)
				#print(groups)
				if overlap(now, last):
					found_group = True
					if now not in find_group:
						lgroup = find_group[last]
						find_group[now] = lgroup
						lgroup.add(now)
					else:
						ngroup, lgroup = find_group[now], find_group[last]
						if ngroup is not lgroup:
							lgroup |= ngroup
							for seg in ngroup: find_group[seg] = lgroup
							groups.remove(ngroup)
			if not found_group:
				new_set = set()
				new_set.add(now)
				find_group[now], groups = new_set, groups + [new_set]
	#to left-up
	for i in range(row-2, -1, -1):
		for now_idx, now in enumerate(reversed(segments[i])):
			for last_idx, last in enumerate(reversed(segments[i+1])):
				#print(i, now_idx, last_idx)
				#print(groups)
				if overlap(now, last):
					ngroup, lgroup = find_group[now], find_group[last]
					if ngroup is not lgroup:
						lgroup |= ngroup
						for seg in ngroup: find_group[seg] = lgroup
						groups.remove(ngroup)
	return groups




#Main Program
im = Image.open('output/binarized.bmp')
(width, height), data_array = im.size, numpy.array(im)
groups = [group for group in groupup(height, width, data_array) if len(group) >= 500]

#drawing
plt.figure(figsize=(5,5))
fig, ax = plt.subplots()
ax.imshow(im)

for group in groups:
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
