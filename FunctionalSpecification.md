# Project functional specification

### Problem Statement: Optimize user's cost savings by intelligently utilizing solar and battery assets.

### User profile:
- Detailed knowledge about different types of solar and battery assets in use.
- Should have enough understanding about the solar/battery assets being used by the user.
- Understand the high-level concepts that were involved in building the optimization models.
- Should be able to evaluate the results from the model.
- General knowledge in navigating a webpage.
- What else does the user need to know?

### Elements
- What solar/battery feartures would be most responsible for optimizing costs?
- What other elements (for eg. weather) are responsible for the costs?
- See Flowchart schematic for our [workflow](Model_flowchart_outline.png)
- The following components of the workflow can be developed in paralel then integrated:
1. Model to predict future utility costs (using historical utility data and weather forecast)
2. Model to predict future energy demand (using histortical data, weather forecast)
3. Model to predict future PV generation (using Weather data and knoweldge of PV generation)
4. Model to predict battery state of health (using battery cycle data)

These four elements will work together to solve an optimization problem to minimize costs, which will decide (A) what to do with generated electricity (from PV and batter)y and (B) where to receive electricity to meet demand (grid, PV, battery)

### Use Cases
- TODO
