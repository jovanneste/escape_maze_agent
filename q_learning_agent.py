import numpy as np
import random
import sys

global maze
global qtable

np.set_printoptions(formatter={'float':"{:6.5g}".format})

def up(index):
    return (index[0]-1, index[1])

def down(index):
    return (index[0]+1, index[1])

def left(index):
    return (index[0], index[1]-1)

def right(index):
    return (index[0], index[1]+1)


def step(state, a):
    actions = {0:up, 1:down, 2:left, 3:right}
    action = actions[a]
    done = False
    new_state = action(state)
    l = maze[new_state]
    if l!=[' ']:
        # if we hit a wall
        new_state = state
        reward = -0.2

    elif l==['F']:
        # if we are finished
        done = True
        reward = 10

    else:
        # move
        reward = 0.1


    return new_state, done, reward



maze = np.asarray([['+', '-', '+', '-', '+', '-', '+'],
        ['|', ' ', ' ', ' ', ' ', ' ', '|'],
        ['+', ' ', '+', '-', '+', ' ', '+'],
        ['|', ' ', ' ', 'F', '|', ' ', '|'],
        ['+', '-', '+', '-', '+', ' ', '+'],
        ['|', '$', ' ', ' ', ' ', ' ', '|'],
        ['+', '-', '+', '-', '+', '-', '+']])



maze = np.where((maze=='+')|(maze=='-')|(maze=='|'), 1, maze)
print(maze)

# quantise
spaces = np.argwhere(maze==' ')
mapping = {}
i=0
for space in spaces:
    mapping[tuple(space)] = i
    i+=1

state = np.where(maze == '$')
state_finish = np.where(maze == 'F')
mapping[tuple(np.squeeze(state))] = len(mapping)
mapping[tuple(np.squeeze(state_finish))] = len(mapping)

qtable = np.zeros((len(mapping), 4))

learning_rate = 0.6
discount_rate = 0.5
epsilon = 0.9
decay_rate= 0.005

num_episodes = 50
max_steps = 50

print("Training agent...")
for episode in range(num_episodes):
    print("Episode:", episode)
    done = False
    # reset start state
    state = np.where(maze == '$')
    for s in range(max_steps):
        # print(tuple(np.squeeze(state)))
        old_state_index = mapping[tuple(np.squeeze(state))]
        # pick an action (0-up, 1-down, 2-left, 3-right)
        # exploration-exploitation tradeoff
        if random.uniform(0,1) < epsilon:
            # explore
            action = random.choice([0,1,2,3])
        else:
            # exploit
            action = np.argmax(qtable[old_state_index,:])

        # perfom action
        new_state, done, reward = step(state, action)
        new_state_index = mapping[tuple(np.squeeze(new_state))]


        # update q table
        qtable[new_state_index, action] += learning_rate * (reward + discount_rate *
                                            np.max(qtable[new_state_index,:])-qtable[old_state_index,action]).round(1)


        state = new_state
        if done == True:
            print("Done")
            break

    epsilon = np.exp(-decay_rate*episode)


print(qtable)

rewards = 0
done = False
print(f"TRAINED AGENT")
print(mapping)
print(maze)
state = np.where(maze == '$')
for s in range(2):
    print(tuple(np.squeeze(state)))
    print(qtable[mapping[tuple(np.squeeze(state))]])
    action = np.argmax(qtable[mapping[tuple(np.squeeze(state))],:])
    print(action)
    new_state, done, reward = step(state, action)



    rewards += reward

    # print(f"score: {rewards}")
    state = new_state

    if done == True:
        break
