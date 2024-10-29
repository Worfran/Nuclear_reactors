import pwr_model_source as pwr
import openmc.deplete as od

#chain file of the simulation should be changed for different fuels (Th232)
chain_file = "../../Data/chain_endfb80_pwr.xml"

#materials

#fuelElement ={
#    'U234': 4.4843e-6,
#    'U235': 5.5815e-4,
#    'U238': 2.2408e-2,
#    'O16': 4.5829e-2
#}

#materialsTh232
#fuelElement = {
#    'U234': 4.4843e-6 * 0.5,
#    'U235': 5.5815e-4 * 0.5,
#    'U238': 2.2408e-2 * 0.5,
#    'Th232': 2.2408e-2 * 0.5,
#    'O16': (2.2408e-2 * 2 + 5.5815e-4 * 2 + 4.4843e-6 * 2) * 0.5 + (2.2408e-2 * 2 ) * 0.5
#}

#materialsTh232-U233 5%
#fuelElement = {
#    'U233': 2.2408e-3,
#    'Th232': 4.4816e-2,
#    'O16': (2.2408e-2 + 2.2408e-3) * 2
#}

#materialsTh232-U233 10%
#fuelElement = {
#    'U233': 4.9816e-3,
#    'Th232': 4.4816e-2,
#    'O16': (2.2408e-2 + 2.2408e-3) * 2
#}

#materialsTh232-Pu239 10%
fuelElement = {
    'Pu239': 1.5204e-3,
    'Th232': 1.1204e-2,
    'O16': (1.1204e-2 + 1.5204e-3) * 2
}

# Create a depletion operator
op = od.CoupledOperator(pwr.pwr_assembly(fuelElements=fuelElement, threads=6), normalization_mode='source-rate', chain_file=chain_file)

# Total simulation time in seconds (10 minutes)
total_simulation_time = 6 * 30.4167 * 24 * 60  * 60 #Moths, Avarage number of days in a month, hours, minutes, seconds

# Number of steps
num_steps = 100

# Calculate the timestep for each step
timestep = total_simulation_time / num_steps

# Create the integrator
integrator = od.PredictorIntegrator(op, timesteps=[timestep]*num_steps, power=1.0e9)

# Run the depletion simulation
integrator.integrate()

# Save the results
results = od.Results("depletion_results.h5")
