import openmc
import openmc.deplete
import openmc.deplete.pool

# Open the depletion results file
results_file = openmc.deplete.Results('depletion_results.h5')

# Get the materials from the results file
materials = results_file.export_to_materials(0)

for material in materials:
    print(material.name)
    for nuclide in material.nuclides:
        print(f"{nuclide.name}")