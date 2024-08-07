import pygplates

lh_provs = pygplates.FeatureCollection('Longhurst_world_v4_2010.shp')
reconstruction_ages = [2.5, 4.5, 7.5, 10, 12.5, 15, 18, 22]
rotation = pygplates.RotationModel('1000_0_rotfile_Merdith_et_al.rot')

for age in reconstruction_ages:
    export_fname = 'Longhurst_world_{0}Ma.shp'.format(age)
    pygplates.reconstruct(lh_provs, rotation, export_fname, age)


