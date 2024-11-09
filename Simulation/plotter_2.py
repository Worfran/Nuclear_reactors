import openmc
import matplotlib.pyplot as plt
import openmc.deplete.results as dr
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter

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

# Get all time steps in days and convert to years
time_steps_days = results.get_times()
time_steps_moths = time_steps_days/30.4167 


# Extract neutron flux values from the results
# Assuming the neutron flux is stored in the 'flux' attribute
_, keff_values = results.get_keff()

keff_values = keff_values[:, 0] 

reactivity = (keff_values - 1)/keff_values
average_reactivity = np.mean(reactivity)


# Plot neutron flux against time steps
plt.figure(figsize=(10, 6))
plt.plot(time_steps_moths, reactivity, linestyle='-', color='black', label='Reactivity')
plt.axhline(average_reactivity, color='red', linestyle='--', label='Average: {:.4f}'.format(average_reactivity))
plt.xlabel('Time [months]')
plt.ylabel('Reactivity')
plt.title('Uranium Oxide\n Reactivity vs Time', fontsize=16)
plt.legend()
plt.savefig('../../Plots/Reactivity_vs_Time_UOX.pdf', dpi=1200)