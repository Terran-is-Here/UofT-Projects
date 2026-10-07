def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes

    global good_battery_health

    cur_time = 0
    cur_charge = 50
    cur_temp = 20
    good_battery_health = True

    # overcharge-related data 
    global overcharge_events 
    overcharge_events = [] 

    # Constants 
    global BAD_BATTERY_LIMIT,GOOD_BATTERY_LIMIT, SLOW_CHARGE, FAST_CHARGE, CAPPED_CHARGE
    BAD_BATTERY_LIMIT = 80 # maximum charge for battery in bad battery state
    GOOD_BATTERY_LIMIT = 100 # maximum charge for battery in general 
    SLOW_CHARGE = "slow" # identifier for a slow charge regimen
    FAST_CHARGE = "fast" # identifier for a fast charge regimen
    CAPPED_CHARGE = "capped" #identifier for charging while at max battery

    # Minimum Values
    global MINIMUM_CHARGE, MINIMUM_TEMPERATURE
    MINIMUM_CHARGE = 0 # absolute minimum charge that the battery can discharge to
    MINIMUM_TEMPERATURE = 0

    # Charging Constants
    global SLOW_CHARGE_RECHARGE_RATE, SLOW_CHARGE_TEMPERATURE_RATE,FAST_CHARGE_RECHARGE_RATE, FAST_CHARGE_TEMPERATURE_RATE
    global FAST_CHARGE_RECHARGE_LIMIT, FAST_CHARGE_TEMPERATURE_LIMIT
    FAST_CHARGE_RECHARGE_LIMIT = 80 # maximum fast charge value for battery 
    FAST_CHARGE_TEMPERATURE_LIMIT = 40 # maximum temperature value for fast charge
    
    SLOW_CHARGE_RECHARGE_RATE = 1 # percent / minute
    SLOW_CHARGE_TEMPERATURE_RATE = 0.25 #C/minute
    FAST_CHARGE_RECHARGE_RATE = 3 # percent / minute
    FAST_CHARGE_TEMPERATURE_RATE = 0.5#C/minute

    # Usage Constants
    global USAGE_DISCHARGE_RATE, USAGE_TEMPERATURE_RATE
    USAGE_DISCHARGE_RATE = 2 #percent/minute
    USAGE_TEMPERATURE_RATE = 1 #C/minute 

    # Empty Battery / Idling Constants
    global IDLING_TEMPERATURE_RATE, IDLING_DISCHARGE_RATE, DEAD_TEMPERATURE_RATE
    IDLING_TEMPERATURE_RATE = 1 #c/minute
    IDLING_DISCHARGE_RATE = 0.5 # percent / minute
    DEAD_TEMPERATURE_RATE = 1 #c/minute
    
    ## Overcharge related constants 
    global OVERCHARGE_CHARGE_THRESHOLD, OVERCHARGE_TIME_THRESHOLD, OVERCHARGE_EVENT_COUNT_THRESHOLD
    OVERCHARGE_CHARGE_THRESHOLD = 90 # value until overcharge events occur. 
    OVERCHARGE_TIME_THRESHOLD = 300 #in minutes
    OVERCHARGE_EVENT_COUNT_THRESHOLD = 3 # How many events are allowed until our battery enters a bad health state? 

# Return current battery temperature. 
def get_cur_temp():
    global cur_temp
    return cur_temp 

# Return current battery charge value. 
def get_cur_charge():
    global cur_charge 
    return cur_charge

# Return current time. 
def get_cur_time(): 
    global cur_time
    return cur_time

# Return current battery health status. 
def get_cur_battery_health():
    global good_battery_health
    return good_battery_health

# Return max possible charge
def get_max_possible_charge(): 
    global good_battery_health
    if good_battery_health:
        return GOOD_BATTERY_LIMIT
    else:
        return BAD_BATTERY_LIMIT

# Setter helper functions 
def set_cur_temp(newTemp): 
    global cur_temp
    # Caps temperature to be at minimum, MINIMUM_TEMPERATURE
    if newTemp < MINIMUM_TEMPERATURE: 
        cur_temp= MINIMUM_TEMPERATURE
    else:
        cur_temp = newTemp 

def set_cur_charge(newCharge): 
    global cur_charge

    # Caps temperature to be at minimum, MINIMUM_CHARGE
    if newCharge < MINIMUM_CHARGE: 
        cur_charge = MINIMUM_CHARGE
    else: 
        cur_charge = newCharge 

def set_cur_battery_health(newState): 
    global good_battery_health
    good_battery_health = newState 

def set_cur_time(newTime): 
    global cur_time
    cur_time = newTime 

# Charging helper function
# Wrapper for setter functions above for preset charge operations.  
def charge_helper_function(operation, time):
    global SLOW_CHARGE, FAST_CHARGE, CAPPED_CHARGE
    global SLOW_CHARGE_RECHARGE_RATE, SLOW_CHARGE_TEMPERATURE_RATE
    global FAST_CHARGE_RECHARGE_RATE, FAST_CHARGE_TEMPERATURE_RATE

    if operation == SLOW_CHARGE: 
        set_cur_temp(get_cur_temp() + SLOW_CHARGE_TEMPERATURE_RATE*time)
        set_cur_charge(get_cur_charge() + SLOW_CHARGE_RECHARGE_RATE*time)
    elif operation == FAST_CHARGE: 
        set_cur_temp(get_cur_temp() + FAST_CHARGE_TEMPERATURE_RATE*time)
        set_cur_charge(get_cur_charge() + FAST_CHARGE_RECHARGE_RATE*time)
    elif operation == CAPPED_CHARGE: 
        set_cur_temp(get_cur_temp() + SLOW_CHARGE_TEMPERATURE_RATE*time) #?? unsure will revise 

# Return time until a possible overcharge event, given a set of conditions. 
def time_until_overcharge(temp,charge,health): 
    deltaCharge = OVERCHARGE_CHARGE_THRESHOLD - charge #find difference between overcharge threshold and current charge
    time = 0
    while deltaCharge > 0: 
        # Check if fast charging is possible. 
        if duration_fast_charge_possible_internal(temp,OVERCHARGE_CHARGE_THRESHOLD,health) > 0: 
            fastChargeTime = duration_fast_charge_possible_internal(temp,OVERCHARGE_CHARGE_THRESHOLD,health)
            time += fastChargeTime
            deltaCharge -= FAST_CHARGE_RECHARGE_RATE*fastChargeTime
        # If fast charging is not possible, then slow charge to delta charge -> 0
        else:
            slowChargeTime = deltaCharge/SLOW_CHARGE_RECHARGE_RATE
            time += slowChargeTime
            deltaCharge -= slowChargeTime * SLOW_CHARGE_RECHARGE_RATE
    return time
    



## Battery Simulation Functions 

# Updates overcharge event log, then checks if battery will go to a bad state from these events. 
def new_overcharge_event(deltaTime=0): 
    global overcharge_events
    overcharge_events.insert(0,get_cur_time() + deltaTime) # Insert current time as a new overcharge entry. 
    if get_recent_overcharge_events() >= OVERCHARGE_EVENT_COUNT_THRESHOLD: #then check recent overcharge events
        set_cur_battery_health(False) #


def get_recent_overcharge_events(deltaTime=0): 
    recentOverchargeEvents = 0
    for overchargeEvent in overcharge_events: 
        # If the time between our overcharge event and current time is greater than the threshold, count the event. 
        if (get_cur_time()-overchargeEvent - deltaTime) < OVERCHARGE_TIME_THRESHOLD: 
            recentOverchargeEvents += 1 
    return recentOverchargeEvents
        
# Simulate battery activities. 
def simulate_activity(activity, duration):
    if activity == "charge": 
        charge_battery(duration)
    if activity == "use": 
        use_battery(duration)
    if activity == "idle": 
        idle_battery(duration)

# battery use function
def use_battery(duration): 
    # battery temperature logic 
    timeToEmpty = get_cur_charge()/USAGE_DISCHARGE_RATE
    # Get desired / new battery value assuming no throttling
    newBatteryValue = get_cur_charge() - (USAGE_DISCHARGE_RATE*duration)
    set_cur_charge(newBatteryValue) # set_cur_charge() automatically sets it to a minimum
    # loop through while continuously using the use_battery time bucket /duration
    remainingTime = duration
    while remainingTime > 0 : 
        # If time to empty is greater than the duration of time used to discharge the battery, then temperature can work as normal. 
        if timeToEmpty > 0 and timeToEmpty >= duration: 
            set_cur_temp(get_cur_temp() + USAGE_TEMPERATURE_RATE*duration) 
            remainingTime = 0 
        else: #If time to empty is 0 (in the cases that it's discharged) or the duration is larger than time to empty, temperature decreases. 
            set_cur_temp(get_cur_temp()  + USAGE_TEMPERATURE_RATE* (timeToEmpty))
            set_cur_temp(get_cur_temp() - DEAD_TEMPERATURE_RATE*(duration-timeToEmpty))
            remainingTime=0
    set_cur_time(get_cur_time() + duration)

# Battery Idle function
def idle_battery(duration): 
    set_cur_temp(get_cur_temp() - IDLING_TEMPERATURE_RATE*duration) #linear relation regardless of battery state 
    set_cur_charge(get_cur_charge() - IDLING_DISCHARGE_RATE*duration) #set_cur_charge catches battery under 0 conditions
    set_cur_time(get_cur_time() + duration)

# Charge Battery aid function. 
def charge_battery(duration): 
    # Let duration be a bucket we're trying to empty with our operations. 
    global BAD_BATTERY_LIMIT
    global SLOW_CHARGE_RECHARGE_RATE, SLOW_CHARGE_TEMPERATURE_RATE
    global FAST_CHARGE_RECHARGE_RATE, FAST_CHARGE_TEMPERATURE_RATE
    overchargeFlag = False #flag if we've already had an overcharge event during this charge operation. 

    # Try to empty duration
    while duration > 0: 
        timeToUse = 0  # Time to use for operations, calculated by other conditionals 
        timeUntilOvercharge = time_until_overcharge(get_cur_temp(),get_cur_charge(),get_cur_battery_health()) 

        # If fast charging is possible, fast charge for as long as possible. 
        # Fast charging operation. 
        if duration_fast_charge_possible() != 0: 
            timeToUse = duration_fast_charge_possible() #already inherently deals with charge cap 
            charge_helper_function(FAST_CHARGE, timeToUse)

        #If fast charging is not possible, slow charge until you reach the cap. 
        else: 

            # Check time till for max charge after overcharge status update
            timeUntilCap = (get_max_possible_charge()-get_cur_charge())/SLOW_CHARGE_RECHARGE_RATE 
            
            if get_cur_battery_health(): # Slow charging with good health
                
                if timeUntilOvercharge > 0: # If battery is still good and below 90%, charge until 90% then rerun logic 
                    timeToUse = timeUntilOvercharge
                    charge_helper_function(SLOW_CHARGE,timeToUse)

                elif timeUntilCap > 0 : # If battery is still good and charging past 90%, charge until maximum. 
                    timeToUse = timeUntilCap
                    charge_helper_function(SLOW_CHARGE,timeUntilCap)

                else: # If battery is still charging, use capped battery rules for the remaining time 
                    timeToUse = duration
                    charge_helper_function(CAPPED_CHARGE,timeToUse)   
            else: # If battery is in a BAD health state, then overcharges are imposssible. 

                if timeUntilCap > 0: # If battery is charging at a value below cap, charge until maximum. 
                    timeToUse = timeUntilCap
                    charge_helper_function(SLOW_CHARGE,timeToUse)
                
                else: #If battery is charging at value at or above cap, use capped battery rules for the remaining time. 
                    timeToUse = duration
                    charge_helper_function(CAPPED_CHARGE, timeToUse)
            
            # Checks actions on this step will cause an overcharge event. 
            if timeUntilOvercharge-duration <= 0 and not overchargeFlag:
                new_overcharge_event(timeUntilOvercharge) # If it does, start overcharge event and update corresponding values 
                overchargeFlag = True  

        set_cur_time(get_cur_time() + timeToUse) # Update global time by time stepped forwards 
        duration -= timeToUse # Reduce amount in duration bucket by time stepped forwards. 

# Checks how much fast charge time is still possible with current internal battery parameters
def duration_fast_charge_possible(): 
    return duration_fast_charge_possible_internal(get_cur_temp(), get_cur_charge(), get_cur_battery_health())

# Checks how much fast charge time is still possible with a given set of parameters. 
def duration_fast_charge_possible_internal(temp, charge, health):
    length_of_fast_charge = 0
    current_temperature = temp
    current_charge = charge 
    current_battery_healthy = health

    # Checks if battery is unhealthy, C >80, T > 40
    if not current_battery_healthy or current_charge > FAST_CHARGE_RECHARGE_LIMIT or current_temperature > FAST_CHARGE_TEMPERATURE_LIMIT: 
        return length_of_fast_charge # If it is one of the three states above, battery charge will stop. 
    else: 
        time1 = (FAST_CHARGE_RECHARGE_LIMIT-current_charge)/3 #from C = C_0 + 3t, solve for time until 80%
        time2 = (FAST_CHARGE_TEMPERATURE_LIMIT-current_temperature)*2 # from T = T_0 + 0.5t ,solve for time until 40C 
        return min(time1,time2) # return smaller of two values above 

# Return charging time needed for (minutes) minutes of the "use" action. 
def charge_time_needed(minutes):
    desired_charge = minutes * USAGE_DISCHARGE_RATE
    missingCharge = desired_charge - get_cur_charge() # Find charge missing / required to charge. 
    chargeTimeRequired = 0 
    # Only true if current charge is greater than or equal to desired charge amount 
    # Or, if desired charge is greater than max possible charge
    if missingCharge <= 0: 
        return chargeTimeRequired
    elif desired_charge > get_max_possible_charge():
        return None

    simTemp = get_cur_temp() 
    simCharge= get_cur_charge()
    # If desired use rate is in the range of (get_cur_charge(), get_max_possible_charge())
    # have to go through each case, loop while filling up chargeTimeRequired bucket
    while missingCharge > 0: 
        fastChargeTime = duration_fast_charge_possible_internal(simTemp,simCharge,get_cur_battery_health())
        if fastChargeTime> 0: # if fast charge is possible 
            chargeTimeRequired += fastChargeTime
            simTemp +=FAST_CHARGE_TEMPERATURE_RATE*fastChargeTime
            simCharge += FAST_CHARGE_RECHARGE_RATE*fastChargeTime

            missingCharge -= FAST_CHARGE_RECHARGE_RATE*fastChargeTime
            continue 

        # If fast charge is not possible, perform slow charge: 
        if get_cur_battery_health(): 
            #if desired charge is above the overcharge threshold, and in process would cause a bad battery event, 
            # return that it is impossible 
            if desired_charge > OVERCHARGE_CHARGE_THRESHOLD and get_recent_overcharge_events() + 1> OVERCHARGE_EVENT_COUNT_THRESHOLD: 
                return None

            # else, if desired charge is equal to the overcharge time, 
            elif desired_charge == OVERCHARGE_CHARGE_THRESHOLD: 
                temp = time_until_overcharge(simTemp,simCharge,get_cur_battery_health()) 
                simTemp += temp
                missingCharge -= SLOW_CHARGE_RECHARGE_RATE*temp 

            else: #if battery charge is less than overcharge: 
                chargeTimeRequired += missingCharge/SLOW_CHARGE_RECHARGE_RATE
                missingCharge = 0 
        else: # If battery health is already bad: 
            if desired_charge > OVERCHARGE_CHARGE_THRESHOLD:
                return None 
            else: 
                chargeTimeRequired += missingCharge/SLOW_CHARGE_RECHARGE_RATE
                missingCharge=0

    return chargeTimeRequired

if __name__ == '__main__':
    initialize()

    print(duration_fast_charge_possible()) # 10
    print(charge_time_needed(50)) # 30

    simulate_activity("charge",30)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 30

    simulate_activity("use",50)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 80

    simulate_activity("use",10)
    print(get_cur_charge()) # 0
    print(get_cur_temp()) # 70

    simulate_activity("charge",100)
    print(get_cur_charge()) # 100
    print(get_cur_temp()) # 95

    simulate_activity("idle",100)
    print(get_cur_charge()) # 50
    print(get_cur_temp()) # 0
    print(get_cur_battery_health()) # True
    print(duration_fast_charge_possible()) # 10

    simulate_activity("charge",80)
    print(get_cur_charge()) # 90
    print(get_cur_temp()) # 22.5
    print(get_cur_battery_health()) # False

    simulate_activity("use",40)
    print(get_cur_charge()) # 10
    print(get_cur_temp()) # 62.5

    simulate_activity("charge",80)
    print(get_cur_charge()) # 80
    print(get_cur_temp()) # 82.5

    initialize()
    # add your tests here
