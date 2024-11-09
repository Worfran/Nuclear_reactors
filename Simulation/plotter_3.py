import matplotlib.pyplot as plt
import openmc.deplete.results as dr
import numpy as np
import seaborn as sns
import matplotlib.ticker as ticker


"""
Ploting settings 1 
"""
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
"""

"""
Ploting settings 2
"""
sns.set_theme(
    context='paper',  # Paper context for academic styling
    style='whitegrid',  # Whitegrid adds a grid to the background
    palette='deep',  # High-contrast color palette
    font='serif',  # Serif font for formal appearance
    font_scale=1.2,  # Larger font size for readability
    color_codes=True,  # Enable shorthand color codes
    rc={
        'grid.color': '0.85',  # Lighter grid color for subtlety
        'grid.linewidth': 0.6,  # Thinner gridlines for minimalism
        'axes.edgecolor': '0.2',  # Darker edge color for emphasis
        'axes.linewidth': 1.5,  # Slightly thicker axes
        'axes.labelsize': 14,  # Larger label size for readability
        'xtick.labelsize': 12,  # X-axis tick label size
        'ytick.labelsize': 12,  # Y-axis tick label size
        'legend.fontsize': 12,  # Set legend font size
        'legend.frameon': False  # Remove legend frame
    }
)


# Load the depletion results
results = dr.Results("depletion_results.h5")

# Get all time steps in days and convert to months
time_steps_days = results.get_times()
time_steps_months = time_steps_days / 30.4167 

# Specify the nuclides to include in the resulting materials

#initial_nuclei = ["U238", "U235",]

initial_nuclei = ["Th232", "U238", "U235",]

#initial_nuclei = ["Pu239", "Th232"]

nuclide_to_plot = ["Th232", "U238", "U235", "U233", "U232","Pu239"]

#nuclide_to_plot = ["Th232", "U233", "U232",]

#nuclide_to_plot = ["U235", "U238", "Pu239", "Pu240",]

nuclide_avarged = ["U238", "Th232", "U235", ]

nuclide_max = [ "U233", "Pu240", "Pu239", "U232",]

# Initialize dictionary to store percentual changes
percentual_changes = {nuc: [] for nuc in initial_nuclei}

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
    for nuc in nuclide_to_plot:
        _, conc = results.get_atoms(mat=fuel_material, nuc=nuc)
        concentrations[nuc] = conc

# Calculate percentual changes
percentual_changes = {nuc: [] for nuc in nuclide_to_plot}
total_initial_nuclei = 0
for nuc in initial_nuclei:
    total_initial_nuclei += concentrations[nuc][0]


for nuc in nuclide_to_plot:
    for i in range(1, len(concentrations[nuc])):
        previous = concentrations[nuc][i-1]
        current = concentrations[nuc][i]
        if previous == 0:
            change = 100* current / total_initial_nuclei  # Handle the case where the previous concentration is zero
        else:
            change = 100 * (current - previous) / total_initial_nuclei
        percentual_changes[nuc].append(change)



# Convert lists to numpy arrays for plotting
for nuc in nuclide_to_plot:
    percentual_changes[nuc] = np.array(percentual_changes[nuc])

# Create a figure with subplots for each nuclide in nuclide_to_plot
#fig, axs = plt.subplots(len(nuclide_to_plot), 1, figsize=(8, 4 * len(nuclide_to_plot)), sharex=True)


# Create a figure with a 2x3 grid of subplots
fig, axs = plt.subplots(2, 3, figsize=(15, 10), sharex=True)
axs = axs.flatten()

# Define the list of styles
styles = ['dotted', (0, (3, 1, 1, 1, 1, 1)), 'dashdot', ':' ]
j = len(styles)

# Plot the percentual changes in each subplot
for i, nuc in enumerate(nuclide_to_plot):
    axs[i].plot(time_steps_months[1:], percentual_changes[nuc], label=nuc, color='black', linestyle=styles[i % j])
    if nuc in nuclide_avarged:
        avareged = np.mean(percentual_changes[nuc])
        axs[i].axhline(y=avareged, color='red', linestyle='--', label=f'Average: {avareged:.2e}%', linewidth=1)
    if nuc in nuclide_max:
        max = np.max(percentual_changes[nuc])
        axs[i].axhline(y=max, color='red', linestyle='--', label=f'Max: {max:.2e}%', linewidth=1)

    axs[i].set_ylabel("Percentual Change [%]")
    axs[i].legend(loc='best')
    """
    if nuc == "Th232":
        axs[i].legend(loc='upper center')
    else:
        axs[i].legend(loc='best')
    """
for ax in axs:
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter(useOffset=False))
    
# Set the xlabel for the last subplot
#axs[-1].set_xlabel("Time [months]")

# Set the xlabel for the three plots in the bottom part
for ax in axs[-3:]:
    ax.set_xlabel("Time [months]")


# Add a title to the entire figure
#fig.suptitle("Percentual Change in Concentrations of \nFissionable Materials Using Thorium Fuel", fontsize=12)

fig.suptitle("Concentrations change in time of Fuel Isotopes \n Uranium Oxide with 10% Th232 addition", fontsize=16)

# Adjust the spacing between subplots
plt.tight_layout()

# Save the plot
plt.savefig('../../Plots/percentual_change_th232_con_10.pdf', dpi=1200)

#plt.savefig('../../Plots/percentual_change_UO2_test1.png', dpi=600)

