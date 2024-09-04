import openmoc
import openmoc.materialize as materialize

# Load cross section data from HDF5 files
hdf5_materials = materialize.load_from_hdf5(filename='materials-data.h5', directory='../Data')

# Retrieve materials
th232 = hdf5_materials['Th-232']
u235 = hdf5_materials['U-235']
u238 = hdf5_materials['U-238']

# Create boundary surfaces
left = openmoc.XPlane(x=-2.0, name='left')
right = openmoc.XPlane(x=2.0, name='right')
bottom = openmoc.YPlane(y=-2.0, name='bottom')
top = openmoc.YPlane(y=2.0, name='top')

# Create fuel cylinder surface
fuel_cylinder = openmoc.ZCylinder(x=0.0, y=0.0, radius=0.4, name='fuel')

# Create cells
fuel = openmoc.Cell(name='fuel')
fuel.setFill(th232)
fuel.addSurface(halfspace=-1, surface=fuel_cylinder)

moderator = openmoc.Cell(name='moderator')
moderator.setFill(u235)
moderator.addSurface(halfspace=1, surface=fuel_cylinder)

# Create a cell to fill the entire geometry
boundary_cell = openmoc.Cell(name='boundary')
boundary_cell.addSurface(halfspace=+1, surface=left)
boundary_cell.addSurface(halfspace=-1, surface=right)
boundary_cell.addSurface(halfspace=+1, surface=bottom)
boundary_cell.addSurface(halfspace=-1, surface=top)

# Create universe
root_universe = openmoc.Universe(name='root universe')
root_universe.addCell(fuel)
root_universe.addCell(moderator)
root_universe.addCell(boundary_cell)

# Create geometry
geometry = openmoc.Geometry()
geometry.setRootUniverse(root_universe)

# Initialize track generator
track_generator = openmoc.TrackGenerator(geometry, num_azim=32, azim_spacing=0.2)
track_generator.generateTracks()

# Initialize solver
solver = openmoc.CPUSolver(track_generator)
solver.computeEigenvalue()

# Output results
solver.printTimerReport()