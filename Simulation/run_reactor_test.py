import pwr_model_source as pwr
import openmc.deplete as od

#confinguration hcp
od.pool.USE_MULTIPROCESSING = False

#chain file of the simulation should be changed for different fuels (Th232)
chain_file = "../../Data/chain_endfb80_pwr.xml"

# Create a depletion operator
op = od.Operator(pwr.pwr_assembly(), normalization_mode='source-rate', chain_file=chain_file)

# Total simulation time in seconds ( 10 minutes )
total_simulation_time = 600

# Number of steps
num_steps = 10

# Calculate the timestep for each step
timestep = total_simulation_time / num_steps

# Set the depletion parameters
op.timesteps = [timestep]*num_steps  # Depletion time steps in days
op.power = 1.0e9  # Power level in watts

# Create the integrator
integrator = od.PredictorIntegrator(op)

# Run the depletion simulation
integrator.integrate()