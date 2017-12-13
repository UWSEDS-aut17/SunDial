# Project functional specification

### Problem Statement: Optimize user's cost savings by intelligently utilizing solar and battery assets.

### User profile:
- Multiple levels of user profiles (End User and Co-developer)
End users have:
- Detailed knowledge about different types of solar and battery assets in use.
- Should have enough understanding about the solar/battery assets being used by the user.
- Understand the high-level concepts that were involved in building the optimization models.
- Should be able to evaluate the results from the model.
- General knowledge in navigating a webpage.
Co-developers have all of the knowledge of End User, plus knowledge of python programming and packages we employ

### Components/elements
- What solar/battery feartures would be most responsible for optimizing costs?
- What other elements (for eg. weather) are responsible for the costs?
- See Flowchart schematic for our [workflow](../img/Model_flowchart_outline.png)
- The following components of the workflow can be developed in parallel then integrated:
1. Model to predict future utility costs (using historical utility data and weather forecast)
2. Model to predict future energy demand (using historical data, weather forecast)
3. Model to predict future PV generation (using Weather data and knowledge of PV generation)
4. Model to predict battery state of health (using battery cycle data)

These four elements will work together to solve an optimization problem to minimize costs, which will decide (A) what to do with generated electricity (from PV and battery and (B) where to receive electricity to meet demand (grid, PV, battery)

### Use Cases
1. Application to currently operating PV-Battery system

In this use case, an end user uses output optimization protocols (solutions to A and B listed above) and applies to their PV-battery assets to maximize profits. Essentially, our models tell their batteries when to charge/discharge and where to send the PV generated electricity (sell vs. use vs. charge battery)

2. Use for designing/evaluating possible future systems

In this use case, systems engineers use our models to make decisions on where and how to employ PV-battery systems. They can evaluate which locations will give maximum value for implementing a PV-battery system that uses our smart use algorithm. Or, for a particular location, they can evaluate which PV size and battery capacity could be most profitable.

3. Use by collaborators to further improve models

Our models will be fairly simple. For example, we will use limited Li-ion battery discharge data to train a simple state of health model. Our software can be used by other developers to further improve with more sophisticated models trained on larger datasets, or applied to additional battery chemistries (other than Li-ion)
