import openmc
import matplotlib.pyplot as plt
import openmc.deplete.results as dr
import numpy as np
import seaborn as sns

from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter

"""
Ploting settings
"""
sns.set_theme(
    context='notebook',
    style='whitegrid',
    palette='deep',
    font='sans-serif',
    font_scale=1,
    color_codes=True,
    rc={'grid.color': '0.5', 'grid.linewidth': 1.2}  # Adjust the grid color and width
)

# Load the depletion results
results = dr.Results("depletion_results.h5")

# Get all time steps in days and convert to months
time_steps_days = results.get_times()
time_steps_months = time_steps_days / 30.4167 

# Specify the nuclides to include in the resulting materials
initial_nuclei = ["U235", "U238", "Pu239", "Th232", "U233"]

nuclide_to_plot = ["U235", "Th232", "U233"]

# Initialize dictionary to store normalized concentrations
concentrations_normalized = {nuc: [] for nuc in initial_nuclei}

# Iterate over all burnup steps
for timei in time_steps_days:
    burnup_index = results.get_step_where(time=timei)
    # Export materials for the current burnup step with specified nuclides
    materials = results.export_to_materials(burnup_index, nuc_with_data=initial_nuclei)
    
    # Find the fuel material (UO2)
    fuel_material = None
    for material in materials:
        if material.name == 'Fuel':
            fuel_material = material
            break

    if fuel_material is None:
        raise ValueError("Fuel material not found in the depletion results.")

    # Get the concentrations of the isotopes for the fuel material
    concentrations = {}
    for nuc in initial_nuclei:
        _, conc = results.get_atoms(mat=fuel_material, nuc=nuc)
        concentrations[nuc] = conc

    # Calculate the initial total number of nuclei for normalization
    if burnup_index == 0:
        initial_C = sum(concentrations[nuc][0] for nuc in initial_nuclei)

    # Normalize the concentrations with respect to the initial total number of nuclei
    for nuc in initial_nuclei:
        concentrations_normalized[nuc].append(concentrations[nuc][burnup_index] / initial_C)

# Convert lists to numpy arrays for plotting
for nuc in initial_nuclei:
    concentrations_normalized[nuc] = 100 * np.array(concentrations_normalized[nuc])

# Create a figure with subplots for each nuclide in nuclide_to_plot
fig, axs = plt.subplots(len(nuclide_to_plot), 1, figsize=(8, 4 * len(nuclide_to_plot)), sharex=True)


# Define the list of styles
styles = ['dotted', '--', '-.', 'steps', '-' ]
j = len(styles)

# Plot the normalized concentrations in each subplot
for i, nuc in enumerate(nuclide_to_plot):
    axs[i].plot(time_steps_months, concentrations_normalized[nuc], label=nuc, color='black', linestyle=styles[i % j])
    axs[i].set_ylabel("Normalized Concentration [%]")
    axs[i].legend()

# Set the xlabel for the last subplot
axs[-1].set_xlabel("Time [months]")

# Add a title to the entire figure
fig.suptitle("Concentrations of Fissionable Materials in a PWR Using Thorium Fuel", fontsize=12)

# Adjust the spacing between subplots
plt.tight_layout()

# Save the plot
plt.savefig('../../Plots/concentration_th232_try1.png', dpi=600)