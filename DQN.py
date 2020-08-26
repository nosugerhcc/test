import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import gym
import fakeData
# Hyper Parameters
BATCH_SIZE = 32
LR = 0.01                   # learning rate
EPSILON = 0.9               # greedy policy
GAMMA = 0.9                 # reward discount
TARGET_REPLACE_ITER = 100   # target update frequency
MEMORY_CAPACITY = 200

N_ACTIONS = 2
N_STATES = 1
ENV_A_SHAPE = 0

class Net(nn.Module):
    def __init__(self, ):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(N_STATES, 50)
        self.fc1.weight.data.normal_(0, 0.1)   # initialization
        self.out = nn.Linear(50, N_ACTIONS)
        self.out.weight.data.normal_(0, 0.1)   # initialization

    def forward(self, x):
        x = self.fc1(x)
        x = F.relu(x)
        actions_value = self.out(x)
        return actions_value


class DQN(object):
    def __init__(self):
        self.eval_net, self.target_net = Net(), Net()

        self.learn_step_counter = 0                                     # for target updating
        self.memory_counter = 0                                         # for storing memory
        self.memory = np.zeros((MEMORY_CAPACITY, N_STATES * 2 + 2))     # initialize memory
        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr=LR)
        self.loss_func = nn.MSELoss()

    def choose_action(self, x):
        x = torch.unsqueeze(torch.FloatTensor([x]), 0)
        # input only one sample
        if np.random.uniform() < EPSILON:   # greedy
            actions_value = self.eval_net.forward(x)
            action = torch.max(actions_value, 1)[1].data.numpy() #输出action_value最大值的位置索引
            action = action[0]  # return the argmax index
        else:   # random
            action = np.random.randint(0, N_ACTIONS)
            action = action
        return action

    def store_transition(self, s, a, r, s_):
        transition = np.hstack((s, [a, r], s_))
        # replace the old memory with new memory
        index = self.memory_counter % MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self):
        # target parameter update
        if self.learn_step_counter % TARGET_REPLACE_ITER == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict()) #将eval_net的权重值给target_network
        self.learn_step_counter += 1

        # sample batch transitions
        sample_index = np.random.choice(MEMORY_CAPACITY, BATCH_SIZE)
        b_memory = self.memory[sample_index, :]
        b_s = torch.FloatTensor(b_memory[:, :N_STATES])
        b_a = torch.LongTensor(b_memory[:, N_STATES:N_STATES+1].astype(int))
        b_r = torch.FloatTensor(b_memory[:, N_STATES+1:N_STATES+2])
        b_s_ = torch.FloatTensor(b_memory[:, -N_STATES:])

        # q_eval w.r.t the action in experience
        q_eval = self.eval_net(b_s).gather(1, b_a)  # shape (batch, 1) 输入state
        q_next = self.target_net(b_s_).detach()     # detach from graph, don't back_propagate
        q_target = b_r + GAMMA * q_next.max(1)[0].view(BATCH_SIZE, 1)   # shape (batch, 1)
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

dqn = DQN()

print('\nCollecting experience...')

for i_episode in range(4000):
    s=146 #意义是此时的发送速率高（146Kbit/s） 需要调节
    ep_r=0
    while True:
        a=dqn.choose_action(s) # a是以10Kbps增加或者减少发送速率
        # TODO:通过a更新s->s_ 发送500个包 得到r，r是30-平均队列长度 当队列长度为0时候，done=True
        if a==0:
            if s==156:
                s_=s
                r=fakeData.getData(str(s_))
                dqn.store_transition(s, a, r, s_)
                ep_r+=r
            else:
                s_=s+10
                r = fakeData.getData(str(s_))
                dqn.store_transition(s, a, r, s_)
                ep_r+=r
        else:
            if s==66:
                s_=s
                r = fakeData.getData(str(s_))
                dqn.store_transition(s, a, r, s_)
                ep_r += r
            else:
                s_ = s - 10
                r = fakeData.getData(str(s_))
                dqn.store_transition(s, a, r, s_)
                ep_r += r


        if dqn.memory_counter>MEMORY_CAPACITY:
            dqn.learn()
            if s==66:
                #round()返回四舍五入值
                print('Ep: ',i_episode,'| Ep_r: ',round(ep_r,2))

        if s==66:
            break

        s = s_