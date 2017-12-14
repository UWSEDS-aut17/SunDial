# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 19:49:58 2017

@author: Casey
"""

# %% Imports

import unittest
from sundial.demand_model import demand_model

# %%

class Test(unittest.TestCase):
    """ Smoke Test """
    
    def Smoketest(self):
        with self.assertRaises(Exception):
            try:
                demand_model.get_demand_cph()
            except Exception:
                pass
            else:
                raise Exception
                
    def OutputTest(self):
        with self.assertRaises(Exception):
            demand = demand_model.get_demand_cph()
            self.assertTrue(len(demand) == 24)