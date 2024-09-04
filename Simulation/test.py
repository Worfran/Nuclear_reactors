import h5py

with h5py.File('Data/materials-data.h5', 'r') as file:
    materials_group = file['material 3']
    print("Datasets in materials group:")
    for name in materials_group:
        print(name)