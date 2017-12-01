import sdutils

# 
prices = sdutils.model_prices(date, data)

demand = sdutils.model_demand(date, data)

output = sdutils.model_pv(data)

health = sdutils.model_battery(data)


plan = sdutils.optimize_usage(date, prices, demand, output, health)