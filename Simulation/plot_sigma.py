import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

"""
Settings
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

file = "Data/endf-6-16461.txt"

data = pd.read_csv(file, sep=',', skiprows=1, header=None)

x = data.iloc[:, 0]
y = data.iloc[:, 1]

plt.plot(x, y, linestyle='-.', color='black')
plt.title("U233 Fission Cross Section")
plt.xlabel("Incident Neutron Energy [eV]")
plt.ylabel("Cross Section [Barns]")
plt.yscale('log')
plt.xscale('log')
plt.savefig("U233_Cross_Section.pdf", dpi=1200, bbox_inches='tight')