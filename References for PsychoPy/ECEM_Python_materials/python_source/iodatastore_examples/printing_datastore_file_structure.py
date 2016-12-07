from psychopy.iohub.datastore.util import ExperimentDataAccessUtility         

# Create an instance of the ExperimentDataAccessUtility class
# for the selected DataStore file. This allows us to access data
# in the file based on Device Event names and attributes.
#
experiment_data=ExperimentDataAccessUtility('.\hdf5_files' , 'events.hdf5')

# Print the HDF5 Structure for the given ioDataStore file.
#
experiment_data.printHubFileStructure()

# Close the HDF5 File
#
experiment_data.close()