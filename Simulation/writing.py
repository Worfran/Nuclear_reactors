import h5py

# Define file paths
materials_file_path = 'Data/materials-data.h5'
th232_file_path = 'Data/endfb-vii.1-hdf5/neutron/Th233.h5'
u235_file_path = 'Data/endfb-vii.1-hdf5/neutron/U235.h5'
u238_file_path = 'Data/endfb-vii.1-hdf5/neutron/U238.h5'

try:
    # Open the new HDF5 file for writing
    with h5py.File(materials_file_path, 'w') as materials_file:
        # Set the '# groups' attribute and 'domain type' attribute on the root of the file
        materials_file.attrs['# groups'] = 3  # Example attribute, adjust as needed
        materials_file.attrs['domain type'] = 'material'  # Set domain type to 'material'

        # Create the materials group
        materials_group = materials_file.create_group('material')

        # Function to copy data from source to destination
        def copy_material_data(source_path, dest_group, material_name):
            with h5py.File(source_path, 'r') as source_file:
                source_data = source_file['/']
                dest_group.copy(source_data, material_name)

        # Copy material data
        copy_material_data(th232_file_path, materials_group, 'Th-232')
        copy_material_data(u235_file_path, materials_group, 'U-235')
        copy_material_data(u238_file_path, materials_group, 'U-238')

except Exception as e:
    print(f"An error occurred: {e}")
