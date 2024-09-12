#%%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%%

"""
Settings for the plots
"""
sns.set_theme(context='notebook', style='whitegrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)


#%%
# Read the data from the file
data = pd.read_csv("../Data/U233.txt", delimiter=",")


#%%
# Plot the cross sections

sns.lineplot(data=data, x="Energy(eV)", y="sigma", color="black")
plt.xscale("log")
plt.yscale("log")

# Add labels and title
plt.xlabel("Incident neutron Energy (eV)")
plt.ylabel("Cross Section (Barns)")
plt.title("U-233 Fission Cross Section")

# Show the plot
plt.show()
# %%
