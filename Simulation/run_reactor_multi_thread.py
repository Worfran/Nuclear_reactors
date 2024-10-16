from mpi4py import MPI
import pwr_model_source as pwr
import openmc.deplete as od
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, filename='run_reactor_multi_thread.log', filemode='w')
logger = logging.getLogger()

logger.debug("Initializing MPI")
# Initialize MPI for the HPC
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

logger.debug(f"MPI initialized with rank {rank} and size {size}")

# Configuration for HPC
od.pool.USE_MULTIPROCESSING = False

# Chain file of the simulation should be changed for different fuels (Th232)
chain_file = "Data/chain_endfb80_pwr.xml"

# Materials
fuelElement = {
    'U234': 4.4843e-6,
    'U235': 5.5815e-4,
    'U238': 2.2408e-2,
    'O16': 4.5829e-2  # + 2.0e-3
}

logger.debug("Creating depletion operator")
# Create a depletion operator
op = od.CoupledOperator(pwr.pwr_assembly(fuelElements=fuelElement), normalization_mode='source-rate', chain_file=chain_file)

# Total simulation time in seconds (10 minutes)
total_simulation_time = 600 #Moths, Avarage number of days in a month, hours, minutes, seconds

# Number of steps
num_steps = 10

# Calculate the timestep for each step
timestep = total_simulation_time / num_steps

logger.debug("Creating integrator")
# Create the integrator
integrator = od.PredictorIntegrator(op, timesteps=[timestep] * num_steps, power=1.0e9)

logger.debug("Starting depletion simulation")
# Run the depletion simulation
try:
    if rank == 0:
        integrator.integrate()
except Exception as e:
    logger.error(f"Rank {rank} encountered an error during integration: {e}")

logger.debug("Saving results")
# Save the results
try:
    if rank == 0:
        results = od.ResultsList.from_hdf5("depletion_results.h5")
except Exception as e:
    logger.error(f"Rank {rank} encountered an error while saving results: {e}")

logger.debug("Finalizing MPI")
# Finalize MPI
MPI.Finalize()
logger.debug("MPI finalized")