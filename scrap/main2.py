import gym
import time


env = gym.make("MountainCar-v0")
state = env.reset()

done = False
counter = 0
while not done:
    env.render()
    counter += 1
    time.sleep(0.01)
    action = 2  # always go right!
    new_state, reward, done, _ = env.step(action)
    print(reward, new_state)
    print(counter)
