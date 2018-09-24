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
groups = groupup(height, width, data_array)
print(len(groups))
groups = [group for group in groups if len(group) >= 500]
print(len(groups))


"""


#draw
fig, ax = plt.subplots()
ax.imshow(im)

rect = patches.Rectangle((450, 0), 100, 512, linewidth=3, edgecolor='r', facecolor='none')
ax.add_patch(rect)
plt.plot(255, 255, 'b+', linewidth=7, markersize=12)
#plt.tight_layout()
plt.axis('off')
plt.savefig('output/3.jpg')
im.close()

"""
