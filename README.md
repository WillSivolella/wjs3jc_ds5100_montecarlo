# Metadata
Author: Your Name
Date: August 10, 2023

# Synopsis
The Montecarlo package provides three classes: Die, Game, and Analyzer, which allow you to simulate dice rolls, play dice games, and analyze the results.

## Die Class
The Die class is used to create dice objects with specific sides and weights. Each side of the die can have a different weight, determining the likelihood of it being rolled.

## Game Class
The Game class allows you to simulate playing a game with multiple dice objects. It takes a list of Die objects and simulates rolling them a specified number of times.

## Analyzer Class
The Analyzer class helps you analyze the results of a game played with the Game class. It provides methods to calculate various statistical properties of the game results.

# API
* 'Die' class
  * __init__(faces)
  * set_weight(f_val, wt)
  * roll_die(rolls=1)
  * get_df()
  
* 'Game' class
  * __init__(d_list)
  * play(rolls)
  * get_recent_play(form='w')
  
* 'Analyzer' class
  * __init__(g_obj)
  * jackpot()
  * fc_roll()
  * combo_count()
  * perm_count()
