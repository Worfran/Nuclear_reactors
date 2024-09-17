import pwr_model_source as pwr
import openmc.deplete as od

#confinguration hcp
od.pool.USE_MULTIPROCESSING = False

#chain file of the simulation should be changed for different fuels (Th232)
chain_file = "../../Data/chain_endfb80_pwr.xml"

# Create a depletion operator
op = od.Operator(pwr.pwr_assembly(), normalization_mode='source-rate', chain_file=chain_file)

# Total simulation time in seconds (2 years)
total_simulation_time = 2 * 365 * 24 * 60 * 60

# Number of steps
num_steps = 100

# Calculate the timestep for each step
timestep = total_simulation_time / num_steps

# Create the integrator
integrator = od.PredictorIntegrator(op, timesteps=[timestep]*num_steps, power=1.0e9)

# Run the depletion simulation
integrator.integrate()
