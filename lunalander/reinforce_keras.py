from keras.layers import Dense, Activation, Input
from keras.models import Model, load_model
from keras.optimizers import Adam
import keras.backend as K
import numpy as np

from keras.models import model_from_json


class Agent(object):
    def __init__(self,
                 ALPHA,
                 GAMMA=0.99,
                 n_actions=4,
                 layer1_size=16,
                 layer2_size=16,
                 input_dims=128,
                 fname='reinforce.h5'
                 ):
        self.gamma = GAMMA
        self.lr = ALPHA
        self.G = 0
        self.input_dims = input_dims
        self.fc1_dims = layer1_size
        self.fc2_dims = layer2_size
        self.n_actions = n_actions
        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []

        self.policy, self.predict = self.build_policy_network()
        self.action_space = [i for i in range(n_actions)]
        self.model_file = fname



    def build_policy_network(self):
        input = Input(shape=(self.input_dims,))
        advantages = Input(shape=[1])
        dense1 = Dense(self.fc1_dims, activation='relu')(input)
        dense2 = Dense(self.fc2_dims, activation='relu')(dense1)
        probs = Dense(self.n_actions, activation='softmax')(dense2)

        def custom_loss(y_true, y_pred):
            out = K.clip(y_pred, 1e-8, 1-1e-8)
            log_lik = y_true*K.log(out)

            return K.sum(-log_lik*advantages)

        policy = Model(input=[input, advantages], output=[probs])
        #policy.compile(optimizer=Adam(lr=self.lr), loss=custom_loss)
        policy.compile(loss='binary_crossentropy', optimizer='adam')


        predict = Model(input=[input], output=[probs])

        return policy, predict

    def choose_action(self, observation):
        state = observation[np.newaxis, :]

        probabilities = self.predict.predict(state)[0]
        action = np.random.choice(self.action_space, p=probabilities)

        return action


    def choose_action_play(self, observation):
        state = observation[np.newaxis, :]
        probabilities = self.predict.predict(state)[0]
        action = np.argmax(probabilities)

        return action

    def store_transition(self, observation, action, reward):
        self.action_memory.append(action)
        self.state_memory.append(observation)
        self.reward_memory.append(reward)

    def learn(self):
        print('entered learn function....')
        state_memory = np.array(self.state_memory)
        action_memory = np.array(self.action_memory)
        reward_memory = np.array(self.reward_memory)

        actions = np.zeros([len(action_memory), self.n_actions])
        actions[np.arange(len(action_memory)), action_memory] = 1

        G = np.zeros_like(reward_memory)
        for t in range(len(reward_memory)):
            print('entered for t loop in learn function...')
            G_sum = 0
            discount = 1
            for k in range(t, len(reward_memory)):
                G_sum += reward_memory[k]*discount
                discount *= self.gamma

            G[t] = G_sum
        mean = np.mean(G)
        std = np.std(G) if np.std(G) > 0 else 1
        self.G = (G-mean)/std

        print('b4 self.policy.train_on_batch()..........')
        cost = self.policy.train_on_batch([state_memory, self.G], actions)
        print('finish train_on_batch()....')

        self.state_memory = []
        self.action_memory = []
        self.reward_memory = []

    def save_model(self):
        self.policy.save(self.model_file)
        #print(self.policy.summary())

    def save_model_json(self):
        # serialize model to JSON
        model_json = self.policy.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)
        # serialize weights to HDF5
        self.policy.save_weights("model.h5")
        print("Saved model to disk")


    def load_model(self):
        self.policy = load_model(self.model_file)


    def load_model_json(self):

        # load json and create model
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        self.policy = model_from_json(loaded_model_json)
        # load weights into new model
        self.policy.load_weights("model.h5")
        print("Loaded model from disk")
        #self.policy.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        self.policy.compile(loss='binary_crossentropy', optimizer='adam')
        print('model compiled')


    def load_model_custom(self):

        advantages = Input(shape=[1])

        def custom_loss(y_true, y_pred):
            out = K.clip(y_pred, 1e-8, 1-1e-8)
            log_lik = y_true*K.log(out)

            return K.sum(-log_lik*advantages)

        self.policy = load_model(self.model_file, custom_objects={'custom_loss': custom_loss})

        # see what the network is
        print(self.policy.summary())





