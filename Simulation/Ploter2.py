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
sns.set_theme(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)
# Function to format the y-axis labels
def scientific_formatter(x, pos):
    return f'{x:.1e}'


# Load the depletion results
results = dr.Results("depletion_results.h5")

# Get all time steps in days and convert to years
time_steps_days = results.get_times()
time_steps_years = time_steps_days/365

# Specify the nuclides to include in the resulting materials
nuclides_of_interest = ["U235", "U238", "Pu239"]

# Initialize lists to store normalized concentrations
concentrations_U235_normalized = []
concentrations_U238_normalized = []
concentrations_Pu239_normalized = []

# Iterate over all burnup steps
for timei in time_steps_days:
    burnup_index = results.get_step_where(time=timei)
    # Export materials for the current burnup step with specified nuclides
    materials = results.export_to_materials(burnup_index, nuc_with_data=nuclides_of_interest)
    
    # Find the fuel material (UO2)
    fuel_material = None
    for material in materials:
        if material.name == 'UO2':
            fuel_material = material
            break

    if fuel_material is None:
        raise ValueError("Fuel material (UO2) not found in the depletion results.")

    # Get the concentrations of the isotopes for the fuel material
    _, conc_U235 = results.get_atoms(mat=fuel_material, nuc="U235")
    _, conc_U238 = results.get_atoms(mat=fuel_material, nuc="U238")
    _, conc_Pu239 = results.get_atoms(mat=fuel_material, nuc="Pu239")

    # Calculate the initial total number of nuclei for normalization
    if burnup_index == 0:
        initial_C = conc_U235[0] + conc_U238[0]  + conc_Pu239[0]

    # Normalize the concentrations with respect to the initial total number of nuclei
    concentrations_U235_normalized.append(conc_U235[burnup_index] / initial_C)
    concentrations_U238_normalized.append(conc_U238[burnup_index] / initial_C)
    concentrations_Pu239_normalized.append(conc_Pu239[burnup_index] / initial_C)

# Convert lists to numpy arrays for plotting
concentrations_U235_normalized = np.array(concentrations_U235_normalized)
concentrations_U238_normalized = np.array(concentrations_U238_normalized)
concentrations_Pu239_normalized = np.array(concentrations_Pu239_normalized)

# Create a figure with three subplots
fig, axs = plt.subplots(3, 1, figsize=(8, 12), sharex=True)

# Plot the normalized concentrations in each subplot
axs[0].plot(time_steps_years, concentrations_U235_normalized, label="U-235", color='black', linestyle='-')
axs[1].plot(time_steps_years, concentrations_U238_normalized, label="U-238", color='black', linestyle='--')
axs[2].plot(time_steps_years, concentrations_Pu239_normalized, label="Pu-239", color='black', linestyle='dashdot')

# Set the labels and title for each subplot
axs[2].set_xlabel("Time [years]")
axs[0].set_ylabel("Normalized Concentration")
axs[1].set_ylabel("Normalized Concentration")
axs[2].set_ylabel("Normalized Concentration")

# Add a legend to each subplot
axs[0].legend()
axs[1].legend()
axs[2].legend()

# Adjust the spacing between subplots
plt.tight_layout()

# Set the formatter for the y-axis to use scientific notation
formatter = FuncFormatter(scientific_formatter)

for ax in axs:
    ax.yaxis.set_major_formatter(formatter)

# Save the plot
plt.savefig('Plots/concentration_U02_try2.png', dpi=600)