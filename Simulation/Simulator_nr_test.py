import openmc
import openmc.deplete as od

#confinguration hcp
od.pool.USE_MULTIPROCESSING = False

#chain file of the simulation should be changed for different fuels (Th232)
chain_file = "../../Data/chain_endfb80_pwr.xml"

# Create PWR assembly geometry
pwr_assembly = openmc.examples.pwr_assembly()

# Define materials
uo2 = openmc.Material(name='UO2')
uo2.add_element('U', 1.0, enrichment=1.5)
uo2.add_element('O', 2.0)
uo2.set_density('g/cc', 10.0)
uo2.depletable = True

zircaloy = openmc.Material(name='Zircaloy')
zircaloy.set_density('g/cm3', 6.55)
zircaloy.add_nuclide('Zr90', 7.2758e-3)

water = openmc.Material(name='Water')
water.set_density('g/cm3', 0.76)
water.add_element('H', 2)
water.add_element('O', 1)
water.add_s_alpha_beta('c_H_in_H2O')
water.depletable = True

# Calculate volumes
# Assuming a typical PWR fuel pin radius and height
fuel_pin_radius = 0.41  # cm
fuel_pin_height = 365.76  # cm (12 feet)
fuel_pin_volume = 3.14159 * fuel_pin_radius**2 * fuel_pin_height  # cm³

# Assuming a typical PWR coolant channel volume
coolant_channel_radius = 0.6  # cm
coolant_channel_height = 365.76  # cm (12 feet)
coolant_channel_volume = 3.14159 * coolant_channel_radius**2 * coolant_channel_height  # cm³

# Set volumes
uo2.volume = fuel_pin_volume
water.volume = coolant_channel_volume

# Instantiate a Materials collection and export to xml
materials_file = openmc.Materials([uo2, water, zircaloy])
materials_file.export_to_xml()

# Define geometry
geom = openmc.Geometry(pwr_assembly)
geom.export_to_xml()

# OpenMC simulation parameters
point = openmc.stats.Point((0, 0, 0))
src = openmc.Source(space=point)
settings = openmc.Settings()
settings.source = src
settings.batches = 100
settings.inactive = 10
settings.particles = 1000
settings.threads = 10
settings.energy_max = 20.0e6  # 20 MeV
settings.export_to_xml()

# Create the depletion operator
model = openmc.Model(geom, settings)
op = od.CoupledOperator(model, normalization_mode='source_rate', chain_file=chain_file)
integrator = od.PredictorIntegrator(op, timesteps=[30]*10, power=1.0e9)

# Run the depletion simulation
integrator.integrate()
