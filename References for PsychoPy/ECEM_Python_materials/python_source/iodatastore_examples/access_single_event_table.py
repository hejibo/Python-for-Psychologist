from psychopy.iohub.datastore.util import ExperimentDataAccessUtility         
from psychopy.iohub import EventConstants

def printQueriedEventsDemo():
    # Create an instance of the ExperimentDataAccessUtility class
    # for the selected DataStore file. This allows us to access data
    # in the file based on Device Event names and attributes.
    # 
    experiment_data=ExperimentDataAccessUtility('..\hdf5_files' , 'events.hdf5')
    
    # Retrieve the 'time','device_time','event_id','delay','category','text'
    # attributes from the Message Event table, where the event time is between
    # the associated trials condition variables TRIAL_START and TRIAL_END
    # value.
    # i.e. only get message events sent during each trial of the eperiment, not any
    #      sent between trials.
    #
    event_results=experiment_data.getEventAttributeValues(EventConstants.MESSAGE,
                        ['time','device_time','event_id','delay','category','text'], 
                        conditionVariablesFilter=None, 
                        startConditions={'time':('>=','@TRIAL_START@')},
                        endConditions={'time':('<=','@TRIAL_END@')})

    
    for trial_events in event_results:    
        print '==== TRIAL DATA START ======='
        print "Trial Condition Values:"
        for ck,cv in trial_events.condition_set._asdict().iteritems():
            print "\t{ck} : {cv}".format(ck=ck,cv=cv)
        print
        
        trial_events.query_string
        print "Trial Query String:\t"
        print trial_events.query_string
        print 
        
        event_value_arrays=[(cv_name,cv_value) for cv_name,cv_value in trial_events._asdict().iteritems() if cv_name not in ('query_string','condition_set')]
        print "Trial Event Field Data:"
        for field_name,field_data in event_value_arrays:
            print "\t"+field_name+': '+str(field_data)
            print
        print '===== TRIAL DATA END ========'

    experiment_data.close()

# Run the main demo function
#
printQueriedEventsDemo()