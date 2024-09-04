import openmoc
import openmoc.materialize as materialize

# Load cross section data from HDF5 files
hdf5_materials = materialize.load_from_hdf5(filename='materials-data.h5', directory='Data')[^3^][3]

# Retrieve materials
th232 = hdf5_materials['Th-232']
u235 = hdf5_materials['U-235']
u238 = hdf5_materials['U-238']

# Create surfaces
left = openmoc.XPlane(x=-2.0, name='left')
right = openmoc.XPlane(x=2.0, name='right')
bottom = openmoc.YPlane(y=-2.0, name='bottom')
top = openmoc.YPlane(y=2.0, name='top')
fuel_cylinder = openmoc.ZCylinder(x=0.0, y=0.0, radius=0.4, name='fuel')

# Create regions
fuel_region = openmoc.Intersection()
fuel_region.addSurface(halfspace=-1, surface=fuel_cylinder)

moderator_region = openmoc.Complement(fuel_region)

# Create cells
fuel = openmoc.Cell(name='fuel')
fuel.setFill(th232)
fuel.addRegion(fuel_region)

moderator = openmoc.Cell(name='moderator')
moderator.setFill(u235)
moderator.addRegion(moderator_region)

# Create universe
root_universe = openmoc.Universe(name='root universe')
root_universe.addCell(fuel)
root_universe.addCell(moderator)

# Create geometry
geometry = openmoc.Geometry()
geometry.setRootUniverse(root_universe)

# Initialize track generator
track_generator = openmoc.TrackGenerator(geometry, num_azim=64, azim_spacing=0.05)[^4^][4]
track_generator.generateTracks()

# Initialize solver
solver = openmoc.CPUSolver(track_generator)
solver.computeEigenvalue()

# Output results
solver.printTimerReport()
