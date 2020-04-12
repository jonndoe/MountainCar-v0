import gym

env = gym.make("MountainCarContinuous-v0")
state = env.reset()
print(env.action_space.sample())

print(env.observation_space.high)
print(env.observation_space.low)


for _ in range(100):
    env.render()
    new_state, reward, done, _ = env.step(env.action_space.sample()) # take a random action
    print(reward, new_state)
#env.close()


done = False
while not done:
    action = env.action_space.sample()
    new_state, reward, done, _ = env.step(action)
    print(reward, new_state)



