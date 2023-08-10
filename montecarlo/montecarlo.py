import pandas as pd
import numpy as np
from collections import Counter

class Die:
    '''The Die class is used to create Die objects, which have declared sides and weights for each side'''
    def __init__(self, faces):
        '''The __init__ method instantiates objects of the Die class using the specified "faces" and sets the weights to 1.0 by default'''
        '''faces (argument of type NumPy Array): contains all the sides to the die'''
        '''weights (attribute of type float): each face has a corresponding weight, which defaults to 1 and defines how much a side is favored'''
        '''die_df (attribute): a dataframe with an index of the faces and a column containing the corresponding weights'''
        if not isinstance(faces, np.ndarray):
            raise TypeError("Argument must be of type np.array.")
        if len(np.unique(faces)) != len(faces):
            raise ValueError("Values in array are not unique.")
                
        self.faces = faces
        self.weights = np.ones(len(faces))
        self.die_df = pd.DataFrame({'weight' : self.weights}, self.faces)
            
    def set_weight(self, f_val, wt):
        '''set_weight take input arguments f_val and wt and allows the user to change the weight of a specific side for a specific object of the Die class'''
        '''f_val (argument of type string or numeric): the side with the corresponding wieght that the user wishes to chance'''
        '''wt (argument of type string or numeric): the new weight value the user wishes to set for the specified side'''
        if f_val not in self.faces:
            raise IndexError("Index is not valid.")
        if (type(wt) != str) & (type(wt) != float) & (type(wt) != int):
            raise ValueError("Weight entered is not a valid data type.")
                
        wt_cast = float(wt)
        self.die_df.loc[f_val] = wt_cast
        self.weights = self.die_df['weight'].values
            
    def roll_die(self, rolls = 1):
        '''The roll_die method takes input argument rolls and returns a list of simulated dice rolls based on the faces and corresponding wieghts of the object'''
        '''rolls (argument of type integer) specifies the amount of times the user wishes to roll the Die object'''
        results = list(self.die_df.sample(n=rolls, weights='weight', replace=True).index)
        return results
            
    def get_df(self):
        '''The get_df method returns the attribute self_df, which is a dataframe that containes the faces and weights of the object'''
        return self.die_df.copy()
        
class Game:
    '''The Game class creates objects using objects of the Die class and contains methods that display the results of the specified amount of rolls for each Die object involved in the "game"'''
    def __init__(self, d_list):
        '''The __init__ method has an argument d_list, which is a list of objects of the Die class, and initializes objects of the Game class, which have attributes d_list and game_df'''
        '''d_list (argument of type list): list of Die objects used for the Game object'''
        '''game_df (attribute of type dataframe): shows the results of each roll of a the objects in d_list'''
        self.d_list = d_list
        self.game_df = None
            
    def play(self, rolls):
        '''The play method takes the integer rolls as an argument, which specifies how many times each dice is rolled and sets game_df (wide by default) to the results'''
        '''rolls (argument of type ineger): specifies how many times each dice is rolled'''
        result_list = []
        col_names = []
        count = 1
        for i in self.d_list:
            result_list.append(i.roll_die(rolls))
            col_names.append(f"Object {count}")
            count += 1
        self.game_df = pd.DataFrame(result_list).T
        self.game_df.columns = col_names
            
    def get_recent_play(self, form = 'w'):
        '''The get_recent_play takes the string argument form and returns the game_df dataframe either in wide or narrow form'''
        '''form (argument of type string): specifies if the game_df should be in narrow or wide form (wide by default)'''
        if (form != 'w') & (form != 'n'):
            raise ValueError("Must input 'w' for wide or 'n' for narrow")
        if form == 'w':
            return self.game_df.copy()
        elif form == 'n':
            game_df_narrow = pd.melt(self.game_df, var_name = 'Die Object', value_name = 'Results')
            return game_df_narrow.copy()
        
        
            
class Analyzer:
    '''The Analyzer class is used to create Analyzer objects, which take the results of a single game and computes various descriptive statistical properties about it.'''
    def __init__(self, g_obj):
        '''The __init__ method take thes argument g_obj and instantiates objects of the Analyzer class'''
        '''g_obj (argument and object of Game class): the specified Game object the user wishes to analyze'''
        if not isinstance(g_obj, Game):
            raise ValueError("Object passed must be an object of the Game class.")
        self.g_obj = g_obj
            
    def jackpot(self):
        '''The jackpot method takes no arguments and return the integer count of scenarios where all die rolled the same "face" during the same roll'''
        count = 0
        for i in range(len(self.g_obj.get_recent_play())):
            if len(set(list(self.g_obj.get_recent_play().loc[i]))) == 1:
                count += 1
        return count

    def fc_roll(self):
        '''The fc_roll method computes how many times a given face is rolled in each event and returns the result as a dataframe'''
        roll_counts = self.g_obj.get_recent_play().apply(lambda r: r.value_counts(), axis=1).fillna(0).astype(int)
        return roll_counts
        
    def combo_count(self):
        '''The combo_count method computes the distinct combinations of faces rolled, along with their counts and returns a dataframe of the results'''
        combo_counts = pd.DataFrame(Counter(tuple(sorted(r)) for _, r in \
                                                self.g_obj.get_recent_play().iterrows()),index=['Combo Counts']).T
        return combo_counts
        
    def perm_count(self): 
        '''The perm_count method computes the distinct permutations of faces rolled, along with their counts and returns a dataframe of the results'''
        perm_counts = pd.DataFrame(Counter(tuple(r) for _, r in \
                                                self.g_obj.get_recent_play().iterrows()),index=['Perm Counts']).T
        return perm_counts

