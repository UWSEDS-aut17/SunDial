## Component List

- Energy price modeling
- Energy Demand modeling
- PV output modeling
- Battery State of Health modeling
- Optimization Procedure

### Energy price modeling
1. What it does. This should be a high level description of the roles of the component.
2. Name. This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).

### Energy Demand modeling
1. What it does. This should be a high level description of the roles of the component.
2. Name. This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).

### PV output modeling
1. What it does. This should be a high level description of the roles of the component
2. Name:  This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).

### Battery State of Health modeling
1. What it does: The battery model calculates expected degradation of the battery due to a) time and b) cycles, and relates this degradation to cost. Thus, each battery cycle will have a "cost penalty" due to the impact of that cycle on degradation
2. Name: BatterySOH
3. Inputs: Input data to predict the battery State of Health (SOH). SOH is a %, where 100% is new battery performic at specified capacity and 0% is the battery is done. Input data columns include Battery age, battery age * Temperature, past cycle information (Energy vs. time), proposed future cycle information
4. Outputs: Battery SOH [%], Battery Capacity [MWhr], Economics [$ net present value]
5. How it works (ideally with pseudo code): Battery degradation is a function of a) time+environment and b) past cycle history. For simplicity, we will use some battery models developed by NREL rather than training our own (which is a very complex problem).

### Optimization Procedure
1. What it does. This should be a high level description of the roles of the component.
2. Name. This should be the name that you use in the component's implementation (e.g., the name of a python class or function).
3. Inputs. Be specific about the data types. For DataFrames, specify the column names and the types of the column values.
4. Outputs. Same consideration as with inputs.
5. How it works (ideally with pseudo code).
