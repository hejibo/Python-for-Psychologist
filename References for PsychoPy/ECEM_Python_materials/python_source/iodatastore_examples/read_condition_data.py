from psychopy.iohub.datastore.util import ExperimentDataAccessUtility         
from pprint import pprint 

def printExperimentConditionVariableDemo():
    # Create an instance of the ExperimentDataAccessUtility class
    # for the selected DataStore file. This allows us to access data
    # in the file based on Device Event names and attributes.
    # 
    experiment_data=ExperimentDataAccessUtility('..\hdf5_files' , 'events.hdf5')
    
    # Here we are accessing the condition values saved.
    # A list is returned, with each element being the condition variable data 
    # for a trial of the experiment, in the order the trials 
    # were run for the given session.    
    #    
    condition_variables=experiment_data.getConditionVariables()

    print "Experiment Condition Variable values:"
    print 
    
    for variable_set in condition_variables:
        pprint(dict(variable_set._asdict()))
        print
    # Close the HDF5 File
    #
    experiment_data.close()

# Run the main demo function
#
printExperimentConditionVariableDemo()