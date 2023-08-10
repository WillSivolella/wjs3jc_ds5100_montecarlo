import unittest
import pandas as pd
import numpy as np
from collections import Counter
from montecarlo import Die
from montecarlo import Game
from montecarlo import Analyzer

class MontecarloTestSuite(unittest.TestCase):
    
    def test_1__init__Die(self): 
        #Create an object the __init__ method of the Die class and see if the dataframe created is the right shape and type
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        #Expect 6 rows for each face and 1 column for the weights; face labels are indecies
        expected = (6,1)
        self.assertEqual(die_obj1.die_df.shape, expected)
        
    def test_2_set_weight(self):
        #Change weight of a side of the die object and see if it works
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj1.set_weight(3,5.0)
        expected = 5.0
        self.assertEqual(die_obj1.weights[2], expected)
        
    def test_3_roll_die(self): 
        #Call the roll_die method on the Die object and see if it returns a list
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        result = die_obj1.roll_die()
        self.assertIsInstance(result, list)
        
        
    def test_4_get_df(self): 
        #Call the get_df method on Die object and see if it returns an object of type pd.DataFrame
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        result = die_obj1.get_df()
        self.assertIsInstance(result, pd.DataFrame)
        
    def test_5_num__init__Game(self): 
        #Create and object and see if it is an object of the Game class
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2]
        g_obj1 = Game(die_list)
        #Expect the length of d_list for the Game object to be 2, which are the number of die objects in the game
        expected = 2
        self.assertEqual(len(g_obj1.d_list), expected) 

    def test_6_play(self):
        #Call play method with 5 rolls on Game object and see if it updates the dataframe to a dataframe with 5 rows
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2]
        g_obj1 = Game(die_list)
        g_obj1.play(100)
        expected = 100
        self.assertEqual(len(g_obj1.game_df), expected)
        
    def test_7_get_recent_play_wide(self):
        #Call get_recent_play method with default argument and see if it returns a wide dataframe
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        self.assertTrue(g_obj1.get_recent_play().shape[1] > 2)

    def test_8_get_recent_play_narrow(self):
        #Call get_recent_play method with default 'n' argument and see if it returns a narrow dataframe
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        self.assertTrue(g_obj1.get_recent_play('n').shape[1] == 2 and "Results" in g_obj1.get_recent_play('n').columns)
        
    def test_9__init__Analyzer(self):
        #Creates an object and sees if the game object attribute is of the Game class
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        a_obj1 = Analyzer(g_obj1)
        result = a_obj1.g_obj
        self.assertIsInstance(result, Game)
        
    def test_10_jackpot(self):
        #Calls jackpot on Analyzer Object and sees if it returns the correct amount of jackpots
        #Because the dice are so heavily weighted to the same side we should expect a jackpot for every roll
        die_list = np.array([1,2])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        
        die_obj1.set_weight(1, 10000)
        die_obj2.set_weight(1, 10000)
        
        die_list = [die_obj1, die_obj2]
        g_obj1 = Game(die_list)
        g_obj1.play(5)
        a_obj1 = Analyzer(g_obj1)
        expected = 5
        self.assertEqual(a_obj1.jackpot(), expected)
        
    def test_11_fc_roll(self):
        #Calls fc_roll on Analyzer object and sees if it returns a dataframe
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        a_obj1 = Analyzer(g_obj1)
        result = a_obj1.fc_roll()
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_12_combo_count(self):
        # add some books with ratings to the list, making sure some of them have rating > 3. 
        # Your test should check that the returned books have rating  > 3
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        a_obj1 = Analyzer(g_obj1)
        result = a_obj1.combo_count()
        self.assertIsInstance(result, pd.DataFrame)
        
    def test_13_perm_count(self):
        # add some books with ratings to the list, making sure some of them have rating > 3. 
        # Your test should check that the returned books have rating  > 3
        die_list = np.array([1,2,3,4,5,6])
        die_obj1 = Die(faces = die_list)
        die_obj2 = Die(faces = die_list)
        die_obj3 = Die(faces = die_list)
        die_list = [die_obj1, die_obj2, die_obj3]
        g_obj1 = Game(die_list)
        g_obj1.play(10)
        a_obj1 = Analyzer(g_obj1)
        result = a_obj1.perm_count()
        self.assertIsInstance(result, pd.DataFrame)
        
        
                
if __name__ == '__main__':
    
    unittest.main(verbosity=3)