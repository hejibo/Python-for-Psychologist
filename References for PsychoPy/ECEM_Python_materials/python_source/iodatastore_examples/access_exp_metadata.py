from psychopy.iohub.datastore.util import ExperimentDataAccessUtility         

def printExperimentMetaDataDemo():
    # Create an instance of the ExperimentDataAccessUtility class
    # for the selected DataStore file. This allows us to access data
    # in the file based on Device Event names and attributes.
    # 
    experiment_data=ExperimentDataAccessUtility('..\hdf5_files' , 'events.hdf5')
    
    # Access the Experiment Meta Data for the first Experiment found in the file.
    # Note that currently only one experiment's data can be saved in each hdf5 file 
    # created. However multiple sessions / runs of the same experiment are all
    # saved in one file.
    #
    exp_md=experiment_data.getExperimentMetaData()[0]
    
    printExperimentMetaData(exp_md)
    
    # Close the HDF5 File
    #
    experiment_data.close()
    
def printExperimentMetaData(exp_md):
    """ 
    Function to 'pretty print' the data. Should be added to the 
    ExperimentDataAccessUtility class itself.
    """
    exp_md_dict=exp_md._asdict()
    print 'ExperimentMetaData:'
    for fname,fvalue in exp_md_dict.iteritems():
        if fname !='sessions':
            print "{0} : {1}".format(fname,fvalue)            
    printSessionMetaData(exp_md.sessions)
    
def printSessionMetaData(sess_md):
    """ 
    Function to 'pretty print' the data. Should be added to the 
    ExperimentDataAccessUtility class itself.
    """
    for session_info in sess_md:
        sess_md_dict=session_info._asdict()
        print '\tSessionMetaData:'
        for fname,fvalue in sess_md_dict.iteritems():
            print "\t\t{0} : {1}".format(fname,fvalue)

# Run the main demo function
#
printExperimentMetaDataDemo()