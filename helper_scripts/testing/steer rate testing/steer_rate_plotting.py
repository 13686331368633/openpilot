import os
import numpy as np
import json
import matplotlib.pyplot as plt

os.chdir('C:/Git/steer fault exploration')

MPH_TO_MS = 1 / 2.2369

data = []
for _f in os.listdir():
  if 'steer_fault_data' in _f:
    print('loading: {}'.format(_f))
    with open(_f, 'r') as f:
      raw = f.read().split('\n')[:-1]
    for line in raw:
      if 'nan' in line:
        continue
      data.append(json.loads(line.replace("'", '"').replace('False', 'false').replace('True', 'true')))  # json loads faster than ast
  if '2' in _f:
    break

steer_angle = [line['steering_angle'] for line in data]
steer_fault = [line['fault'] * 800 for line in data]
new_steer = [line['new_steer'] for line in data]
apply_steer = [line['apply_steer'] for line in data]
plt.clf()
plt.plot(steer_angle, label='Steering angle')
plt.plot(steer_fault, label='Steer fault')
plt.plot(new_steer, label='new_steer')
plt.plot(apply_steer, label='apply_steer')
plt.legend()
plt.show()


# faults = []
# for idx, line in enumerate(data):
#   if idx == 0:
#     continue
#   # more 'realistic' data above 10 mph, and remove random faults that occurred on straight roads
#   if line['fault'] and line['v_ego'] > 10 * MPH_TO_MS and abs(line['steering_rate']) > 5:
#     if not data[idx - 1]['fault']:  # only include first fault, skip rest of concurrent falts
#       faults.append(line)
#
# print('Total faults: {}'.format(len(faults)))
# faults_steer_rate = [line['steering_rate'] for line in faults]
# print('Avg. fault steer rate: {}'.format(np.mean(np.abs(faults_steer_rate))))
# print('Std. fault steer rate: {}'.format(np.std(np.abs(faults_steer_rate))))
# print('Max fault steer rate: {}'.format(max(np.abs(faults_steer_rate))))
# print('Min fault steer rate: {}'.format(min(np.abs(faults_steer_rate))))
# faults_towards_center = [line for line in faults if (line['steering_angle'] < 0 and line['steering_rate'] > 0) or (line['steering_angle'] > 0 and line['steering_rate'] < 0)]
# faults_away_from_center = [line for line in faults if (line['steering_angle'] < 0 and line['steering_rate'] < 0) or (line['steering_angle'] > 0 and line['steering_rate'] > 0)]
# print('---')
# faults_steer_rate_towards_center = [line['steering_rate'] for line in faults_towards_center]
# faults_steer_rate_away_from_center = [line['steering_rate'] for line in faults_away_from_center]
# print('Avg. towards center fault steer rate: {}'.format(np.mean(np.abs(faults_steer_rate_towards_center))))
# print('Std. towards center fault steer rate: {}'.format(np.std(np.abs(faults_steer_rate_towards_center))))
# print('Max towards center fault steer rate: {}'.format(max(np.abs(faults_steer_rate_towards_center))))
# print('Min towards center fault steer rate: {}'.format(min(np.abs(faults_steer_rate_towards_center))))
# print()
# print('Avg. away from center fault steer rate: {}'.format(np.mean(np.abs(faults_steer_rate_away_from_center))))
# print('Std. away from towards center fault steer rate: {}'.format(np.std(np.abs(faults_steer_rate_away_from_center))))
# print('Max away from center fault steer rate: {}'.format(max(np.abs(faults_steer_rate_away_from_center))))
# print('Min away from center fault steer rate: {}'.format(min(np.abs(faults_steer_rate_away_from_center))))
# print('---')
#
# print('Faults occuring when moving towards center: {}'.format(len(faults_towards_center)))
# print('Faults occuring when moving away from center: {}'.format(len(faults_away_from_center)))
# print('Percentage of faults moving towards center: {}%'.format(round(len(faults_towards_center) / len(faults) * 100, 2)))
