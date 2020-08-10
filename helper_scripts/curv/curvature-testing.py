import math
import os
import json
import time

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from selfdrive.config import Conversions as CV
from sklearn.cluster import KMeans


os.chdir(os.getcwd())

data = []
for fi in os.listdir():
  print(fi)
  if not fi.endswith('.py'):
    with open(fi) as f:
      for line in f.read().split('\n')[:-1]:
        line = line.replace('array([', '[').replace('])', ']')  # formats dpoly's np array
        line = line.replace("'", '"')  # for json
        try:
          data.append(json.loads(line))
        except:
          print('error: {}'.format(line))

print('\nsamples before filtering: {}'.format(len(data)))
round_to = 6
min_angle = 1.
max_angle = 45.
TR = 0.9
data_filtered = []


for line in data:
  if line['v_ego'] < 15 * CV.MPH_TO_MS:
    continue
  if min_angle <= abs(line['angle_steers']) <= max_angle:
    dist = line['v_ego'] * TR
    line['d_poly'][3] = 0  # want curvature of road from start of path not car
    lat_pos = abs(np.polyval(line['d_poly'], dist))  # lateral position in meters at TR seconds
    line['lat_pos'] = lat_pos
    line['d_poly_0'] = line['d_poly'][0]
    data_filtered.append(line)
print('samples after filtering: {}'.format(len(data_filtered)))
data = data_filtered

use_data_y = 'angle_steers'

plt.figure(0)
sns.distplot([line['v_ego'] for line in data], bins=75)
plt.title('speed (m/s)')
plt.show()

plt.figure(1)
sns.distplot([abs(line[use_data_y]) for line in data], bins=100)
plt.title(use_data_y)
plt.show()

# plt.figure(2)
# plt.scatter([line['v_ego'] for line in data], [abs(line[use_data_y]) for line in data], marker='o')
# plt.show()
n_clusters = 15
kmeans = KMeans(n_clusters=n_clusters, max_iter=750)
x = np.array([[line['v_ego'] for line in data], [abs(line[use_data_y]) for line in data]]).T
print(x.shape)
kmeans.fit(x)

plt.figure(3)
pred_y = kmeans.fit_predict(x)
# plt.scatter(x[:,0], x[:,1], s=0.6)

cluster_coords = kmeans.cluster_centers_

def find_distance(pt1, pt2):
  x1, x2 = pt1[0], pt2[0]
  y1, y2 = pt1[1], pt2[1]
  dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
  return dist

t = time.time()
clusters = [[] for _ in range(n_clusters)]
for line in data:
  dists = [find_distance([line['v_ego'], abs(line[use_data_y])], clstr_coord) for clstr_coord in cluster_coords]
  # print(dists)
  closest = min(range(len(dists)), key=dists.__getitem__)
  clusters[closest].append([line['v_ego'], abs(line[use_data_y])])
print(time.time() - t)

colors = ['g', 'r', 'b', 'o', 'g', 'r', 'b', 'o', 'g', 'r']
for clr, cluster in zip(colors, clusters):
  if len(cluster):
    d1, d2 = np.array(cluster).T
    plt.scatter(d1, d2, s=2)
plt.xlabel('speed (m/s)')
plt.ylabel(use_data_y)

plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=150, c='red')
plt.show()
