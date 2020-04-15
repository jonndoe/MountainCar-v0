import gym
import matplotlib.pyplot as plt
import numpy as np
from reinforce_keras import Agent
from keras.models import load_model
#from utils import plotLearning

import time


if __name__ == '__main__':
    agent = Agent(ALPHA=0.0005, input_dims=8, GAMMA=0.99, n_actions=4,layer1_size=64, layer2_size=64)
    agent.policy = load_model('reinforce.h5')

    env = gym.make('LunarLander-v2')

    done = False
    observation = env.reset()

    score = 0
    counter = 0
    while not done:
        counter += 1

        action = agent.choose_action(observation)

        observation_, reward, done, info = env.step(action)
        agent.store_transition(observation, action, reward)
        observation = observation_
        score += reward

        env.render()
        time.sleep(0.05)

    print('score %.1f' % score)
    print('counter', counter)