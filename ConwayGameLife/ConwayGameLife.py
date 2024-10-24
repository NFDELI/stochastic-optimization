import sys
sys.path.append("../")
import numpy as np
import pandas as pd
import plotly.express as px
import ConwayGameLifeModel as cgm
import ConwayGameLifePolicy as cgp
from BaseClasses import Util as util

# Example Usage
grid_size = 10
T = 10
model = cgm.ConwayGameLife(grid_size = grid_size, t0=0, T=T)

policy = cgp.ConwayGameOfLifePolicy(model = model)

number_of_iterations = 1
policy.run_policy(n_iterations = number_of_iterations)

print("Simulation Results:")
print(policy.results)

print("\nPerformance Metrics:")
print(policy.performance)

