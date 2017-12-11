""" This program outputs the optimization window.
"""

def optimize():
    """ Does things.
    """

    from sundial.bat_model import bat_model
    from sundial.price_model import price_model
    import sundial.pv_model
    import sundial.demand

    import numpy as np
    import pandas as pd

    ## Battery Modelling
    energy = 8 #kWhr
    hour_start = 18 #6pm, sun goes down
    hour_end = 22 #10pm, this means battery stops at 10:00pm, not 10:59
    day = 343 #Dec 9th
    bat_cap = 13.5 #kWhr
    bat_cost = 222*bat_cap # $ - cost scales with capacity, adjust to make relavent if needed

    bat_cph = bat_model.bat_price_per_hour(energy,hour_start,hour_end,day,bat_cap,bat_cost)
    bat_cph = np.squeeze(bat_cph)
    print("Battery CPH calculation successful.")

    ## Price Modelling

    epm = price_model.EnergyPriceModel()
    price_cph = epm.test_model("2016-12-08", "SVM_rbf")
    print("Energy price CPH calculation successful.")

    ## Demand Modelling

    demand_cph = sundial.demand.get_demand_cph()
    print("Energy demand CPH calculation successful.")

    ## PV Output Modelling

    pv_output_cph = sundial.pv_model.pv_output_cph()
    print("PV Output CPH calculation successful.")

    df = pd.DataFrame({'bat_cph': bat_cph,
                  'price_cph': price_cph,
                  'demand_cph': demand_cph,
                  'pv_output_cph': pv_output_cph})

    return df

def compute_cost_savings(df):
    # write scenario functions here

    print("Under construction.")

def plot_graphs(df):
    # write plot functions here

    print("Under construction.")
