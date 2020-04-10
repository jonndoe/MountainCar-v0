import gym  # open ai gym
import pybulletgym  # register PyBullet enviroments with open ai gym
import time



env = gym.make('Walker2DPyBulletEnv-v0')


action = 2

while True:
    time.sleep(0.2)

    env.render() # call this before env.reset, if you want a window showing the environment
    env.reset()  # should return a state vector if everything worked

    print(env.reset())