""" This program outputs the optimization window.
"""

def optimize_solar(dt):
  """ Does things.
  """
  
  from sundial import models
  
  pv_hourly = models.pv_model(dt)
  pr_hourly = models.pr_model(dt)
  dm_hourly = models.dm_model(dt)
  bd_hourly = models.dm_model(dt)
  
  sundial_df = pv_hourly.merge([pr_hourly, dm_hourly, bd_hourly])
  
  sundial_df['ScenarioA'] = # function for scenario A
  sundial_df['ScenarioB'] = # function for scenario B
  sundial_df['ScenarioC'] = # function for scenario C
  
def optimize_viz(df):
  """ Does things.
  """
  
  import matplotlib.pyplot as plt
  
  fig = 
