# -*- coding: utf-8 -*-
"""Taxi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cwxGlYu1PNUKOH-LZItfoZA5W-AgXHDX
"""

!pip install gym[all] -q

import numpy as np
import gym
import random
import time
from tqdm.notebook import tqdm

# Commented out IPython magic to ensure Python compatibility.
!pip install pyvirtualdisplay -q
!apt install xvfb -y -q 

import matplotlib.pyplot as plt
from pyvirtualdisplay import Display
from IPython import display

# %matplotlib inline
Display().start()

def show_render_1(env):
  plt.figure(3,figsize=(27,9))
  plt.imshow(env.render(mode='rgb_array'))
  display.display(plt.gcf())
  display.clear_output(wait=True)

env = gym.make("Taxi-v3")
env.reset()
show_render_1(env)

state_space = env.observation_space.n
action_space = env.action_space.n
q_table = np.zeros((state_space,action_space))
(state_space,action_space)

epsilon = 1.
max_epsilon = 1.
min_epsilon = .01
decay_rate = .0005

total_episodes = 30000
each_episode_steps = 1000
learning_rate = 0.8
discount_rate = 0.95
log_interval = 1000

def epsilon_greedy_policy(epsilon,state,q_table):
  if random.uniform(0,1) > epsilon:
    action = np.argmax(q_table[state])
    select="table"
  else:
    action = env.action_space.sample()
    select = "random"
  return action, select

def epsilon_reduce(epsiode):
  return min_epsilon + (max_epsilon - min_epsilon)*np.exp(-decay_rate*epsiode)

def greedy_policy(state,q_table):
  return np.max(q_table[state])

def new_reward(reward, state, done, action):
  
  obs = []
  obs.append(state % 4)
  state = state // 4
  obs.append(state % 5)
  state = state // 5
  obs.append(state % 5)
  state = state // 5
  obs.append(state)
  assert 0 <= state < 5

  taxi_rows, taxi_cols, pas_loc, pas_dest = reversed(obs)

  locs = {0:(0, 0), 
          1:(0, 4), 
          2:(4, 0), 
          3:(4, 3),
          4:"in_taxi"}
  reward_drop, reward_pickup, reward_step = 0, 0, 0

  if action == 5: 
    if locs[pas_dest] == (taxi_rows, taxi_cols) and done:
      reward_drop = 100
    else:
      reward_drop = -20
  elif action == 4:
    if locs[pas_loc] == (taxi_rows, taxi_cols):
      reward_pickup = 50
    else:
      reward_pickup = -20
      
  if action < 4:
    if locs[4] == locs[pas_loc]:
      reward_step = -2
    else:
      reward_step = -4

  return reward_drop + reward_pickup + reward_step

def train():
  table_nos, random_nos, total_rewards, episode_reward = 0, 0, 0, 0
  for episode in range(total_episodes):
    state = env.reset()
    step = 0
    done = False
    step_reward = 0
    epsilon = epsilon_reduce(episode)
    for step in range(each_episode_steps):
      action, select = epsilon_greedy_policy(epsilon, state, q_table)
      new_state, reward, done, info = env.step(action)
      rewards = new_reward(reward, new_state, done, action)
      error = learning_rate*(rewards + discount_rate*(greedy_policy(new_state, q_table)) - q_table[state][action])
      q_table[state][action] = q_table[state][action] + error
      step_reward += rewards
      if done:
        break
      state = new_state
      if select == "table":
        table_nos += 1
      elif select == "random":
        random_nos += 1
    episode_reward += step_reward
    if episode % log_interval == 0:
      table_per = round((table_nos/(table_nos+random_nos))*100,2)
      random_per = round((random_nos/(table_nos+random_nos))*100,2)
      total_rewards += episode_reward
      print("Gen="+str(episode),"random="+str(random_per),"table="+str(table_per),"steps_taken="+str(step),"mean_reward="+str(episode_reward/1000),"episode_reward="+str(episode_reward),"total_reward="+str(total_rewards)) 
      episode_reward = 0
  env.close()
  print("Gen="+str(episode),"random="+str(random_per),"table="+str(table_per),"steps_taken="+str(step),"mean_reward="+str(episode_reward/1000),"episode_reward="+str(episode_reward),"total_reward="+str(total_rewards)) 
  return q_table

def play(q_table):
  state = env.reset()
  done = False
  rewards =0
  for step in range(each_episode_steps):
    time.sleep(1)
    show_render_1(env)
    action = np.argmax(q_table[state])
    new_state, reward, done, info = env.step(action)
    rewards += new_reward(reward, new_state, done, action)
    state = new_state
    if done:
      break
  show_render_1(env)
  print("#############steps_taken="+str(step),"reward="+str(rewards)+"###############")
  env.close()

#q_table = np.load("taxi.npy")

q_table_frozenlake = train()

play(q_table_frozenlake)

#np.save("taxi.npy",q_table)

img = plt.imshow(env.render('rgb_array'))
def show_render_2(env):
  img.set_data(env.render('rgb_array')) 
  display.display(plt.gcf())
  display.clear_output(wait=True)

!apt-get install python-opengl -y
!pip install piglet