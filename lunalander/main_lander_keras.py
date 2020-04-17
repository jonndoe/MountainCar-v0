import gym
import matplotlib.pyplot as plt
import numpy as np
from reinforce_keras import Agent
#from utils import plotLearning
import time


if __name__ == '__main__':
    agent = Agent(ALPHA=0.0005, input_dims=8, GAMMA=0.99, n_actions=4,
                  layer1_size=64, layer2_size=64)
    env = gym.make('LunarLander-v2')
    score_history = []

    agent.load_model_json()

    print(agent.policy.summary())


    n_episodes = 400

    for i in range(n_episodes):
        print('entered for loop...')
        done = False
        score = 0
        observation = env.reset()
        while not done:
            print('entered while loop....')
            action = agent.choose_action(observation)
            observation_, reward, done, info = env.step(action)
            agent.store_transition(observation, action, reward)
            observation = observation_
            score += reward
        print('while loop completed...')
        score_history.append(score)

        print('start agent.learn()')
        agent.learn()

        print('episode ', i, 'score %.1f' % score,
              'average_score %.1f' % np.mean(score_history[-100:]))


    agent.save_model_json()

