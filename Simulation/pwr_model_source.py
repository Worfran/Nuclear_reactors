from numbers import Integral
import numpy as np
import openmc
import openmc.model

def pwr_assembly(maxEnergy=8.0e4, threads=1):
    
    """Create a PWR assembly model.

    This model is a reflected 17x17 fuel assembly from the the `BEAVRS
    <http://crpg.mit.edu/research/beavrs>`_ benchmark. The fuel is 2.4 w/o
    enriched UO2 corresponding to a beginning-of-cycle condition. Note that the
    number of particles/batches is initially set very low for testing purposes.

    Parameters
    ----------
    maxEnergy : float, optional
        The maximum energy of the source particles in electron volts (eV). 
        Default is 8.0e4 eV.
        
    threads : int, optional
        The number of threads to use for the simulation. Default is 1.

    Returns
    -------
    model : openmc.model.Model
        A PWR assembly model

    """

    model = openmc.model.Model()

    # Define materials.
    fuel = openmc.Material(name='Fuel')
    fuel.set_density('g/cm3', 10.29769)
    fuel.add_nuclide('U234', 4.4843e-6)
    fuel.add_nuclide('U235', 5.5815e-4)
    fuel.add_nuclide('U238', 2.2408e-2)
    fuel.add_nuclide('O16', 4.5829e-2)
    fuel.depletable = True

    clad = openmc.Material(name='Cladding')
    clad.set_density('g/cm3', 6.55)
    clad.add_nuclide('Zr90', 2.1827e-2)
    clad.add_nuclide('Zr91', 4.7600e-3)
    clad.add_nuclide('Zr92', 7.2758e-3)
    clad.add_nuclide('Zr94', 7.3734e-3)
    clad.add_nuclide('Zr96', 1.1879e-3)

    hot_water = openmc.Material(name='Hot borated water')
    hot_water.set_density('g/cm3', 0.740582)
    hot_water.add_nuclide('H1', 4.9457e-2)
    hot_water.add_nuclide('O16', 2.4672e-2)
    hot_water.add_nuclide('B10', 8.0042e-6)
    hot_water.add_nuclide('B11', 3.2218e-5)
    hot_water.add_s_alpha_beta('c_H_in_H2O')

    # Define the materials file.
    model.materials = (fuel, clad, hot_water)

    # Instantiate ZCylinder surfaces
    fuel_or = openmc.ZCylinder(x0=0, y0=0, r=0.39218, name='Fuel OR')
    clad_or = openmc.ZCylinder(x0=0, y0=0, r=0.45720, name='Clad OR')

    # Compute the volume of each material
    fuel_volume = np.pi * fuel_or.r**2


    fuel.volume = fuel_volume

    # Create boundary planes to surround the geometry
    pitch = 21.42
    min_x = openmc.XPlane(x0=-pitch/2, boundary_type='reflective')
    max_x = openmc.XPlane(x0=+pitch/2, boundary_type='reflective')
    min_y = openmc.YPlane(y0=-pitch/2, boundary_type='reflective')
    max_y = openmc.YPlane(y0=+pitch/2, boundary_type='reflective')

    # Create a fuel pin universe
    fuel_pin_universe = openmc.Universe(name='Fuel Pin')
    fuel_cell = openmc.Cell(name='fuel', fill=fuel, region=-fuel_or)
    clad_cell = openmc.Cell(name='clad', fill=clad, region=+fuel_or & -clad_or)
    hot_water_cell = openmc.Cell(name='hot water', fill=hot_water, region=+clad_or)
    fuel_pin_universe.add_cells([fuel_cell, clad_cell, hot_water_cell])


    # Create a control rod guide tube universe
    guide_tube_universe = openmc.Universe(name='Guide Tube')
    gt_inner_cell = openmc.Cell(name='guide tube inner water', fill=hot_water,
                                region=-fuel_or)
    gt_clad_cell = openmc.Cell(name='guide tube clad', fill=clad,
                               region=+fuel_or & -clad_or)
    gt_outer_cell = openmc.Cell(name='guide tube outer water', fill=hot_water,
                                region=+clad_or)
    guide_tube_universe.add_cells([gt_inner_cell, gt_clad_cell, gt_outer_cell])

    # Create fuel assembly Lattice
    assembly = openmc.RectLattice(name='Fuel Assembly')
    assembly.pitch = (pitch/17, pitch/17)
    assembly.lower_left = (-pitch/2, -pitch/2)

    # Create array indices for guide tube locations in lattice
    template_x = np.array([5, 8, 11, 3, 13, 2, 5, 8, 11, 14, 2, 5, 8,
                           11, 14, 2, 5, 8, 11, 14, 3, 13, 5, 8, 11])
    template_y = np.array([2, 2, 2, 3, 3, 5, 5, 5, 5, 5, 8, 8, 8, 8,
                           8, 11, 11, 11, 11, 11, 13, 13, 14, 14, 14])

    # Create 17x17 array of universes
    assembly.universes = np.tile(fuel_pin_universe, (17, 17))
    assembly.universes[template_x, template_y] = guide_tube_universe

    # Create root Cell
    root_cell = openmc.Cell(name='root cell', fill=assembly)
    root_cell.region = +min_x & -max_x & +min_y & -max_y

    # Create root Universe
    model.geometry.root_universe = openmc.Universe(name='root universe')
    model.geometry.root_universe.add_cell(root_cell)

    model.settings.batches = 10
    model.settings.inactive = 5
    model.settings.particles = 100
    #settings.particles = 100000
    model.settings.threads = threads
    model.settings.energy_max = maxEnergy 
    model.settings.source = openmc.IndependentSource(
        space=openmc.stats.Box([-pitch/2, -pitch/2, -1], [pitch/2, pitch/2, 1]),
        constraints={'fissionable': True}
    )

    return model
