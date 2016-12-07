from psychopy.iohub.datastore.util import ExperimentDataAccessUtility         
from psychopy.iohub import EventConstants

def printEventTypesWithDataDemo():
    # Create an instance of the ExperimentDataAccessUtility class
    # for the selected DataStore file. This allows us to access data
    # in the file based on Device Event names and attributes.
    # 
    experiment_data=ExperimentDataAccessUtility('..\hdf5_files' , 'events.hdf5')
    
    # Get any event tables that have >=1 event saved in them
    #
    events_by_type=experiment_data.getEventsByType()
    
    # print out info on each table
    #
    for event_id, event_gen in events_by_type.iteritems():
        event_constant=EventConstants.getName(event_id)
        print "{0} ({1}): {2}".format(event_constant,event_gen.table.nrows,event_gen)

    # Close the HDF5 File
    #
    experiment_data.close()

# Run the main demo function
#
printEventTypesWithDataDemo()