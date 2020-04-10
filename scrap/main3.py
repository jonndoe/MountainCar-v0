import gym
import time
import random

import numpy as np

env = gym.make("MountainCar-v0")

print(env.action_space.n)

print(env.reset()) # print the current state of the agent in the environment

print(env.observation_space.high)
print(env.observation_space.low)

DISCRETE_OS_SIZE = [20, 20] # split our observation space for 20 parts
discrete_os_win_size = (env.observation_space.high - env.observation_space.low)/DISCRETE_OS_SIZE # the size of one bucket of os

print(discrete_os_win_size)

q_table = np.random.uniform(low=-2, high=0, size=DISCRETE_OS_SIZE + [env.action_space.n])

print(len(q_table))
print(q_table)

counter1 = 0
for row in q_table:
    for cell in row:
        print(cell)
        counter1 +=1

print('counter cell: ', counter1)

done = False
counter = 0
while not done:
    counter += 1
    print(counter)
    #time.sleep(0.01)
    #time.sleep(random.randint(0, 8)*0.01)
    action = random.randint(0,2)
    new_state, reward, done, _ = env.step(action)
    #print(env.step(action))
    print('new_state : ', new_state, 'reward: ', reward, 'done: ', done, _)
    env.render()



