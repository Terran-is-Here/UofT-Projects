def initialize():
    '''Initializes the global variables needed for the simulation.
    Note: this function is incomplete, and you may want to modify it.
    '''
    global cur_temp # in degrees Celsius
    global cur_charge # in percentage points
    global cur_time # in minutes
    global bad_battery_charge_times
    global good_battery_health

    cur_time = 0
    cur_charge = 50 # set to 50% charge 
    cur_temp = 20 # set to 20C temperature
    bad_battery_charge_times = [] #
    good_battery_health = True

def simulate_activity(activity, duration):
    global cur_time
    cur_time = cur_time + duration
    
    if activity == "charge": 

        # if fast charge is available, calculate fast-chargable time and charge from there
        if duration_fast_charge_possible() != 0: 
            charge_time = min(duration_fast_charge_possible(),duration)
            charge_battery('fast', charge_time) 
            # in the case in which we have more duration over our corresponding charge time 
            if duration > charge_time: 
                pass
        else: 
            pass
            # charge_time = duration 


    elif activity == "use": 
        pass
    elif activity == "idle": 
        pass

    else: 
        pass


# Helper function for charging operations
def charge_battery(type, duration): 
    if type == "fast": #fast-charging regimen
        set_cur_temp(get_cur_temp() + 0.5 * duration)
        set_cur_charge(get_cur_temp() + 3 * duration)
    else: #slow-charging regimen
        set_cur_charge(get_cur_charge + duration)
        set_cur_temp(get_cur_temp() + 0.25 * duration)
        



# Will return 0 if fast charge is not possible, else returns the time possible. 
def duration_fast_charge_possible():
    length_of_fast_charge = 0
    current_temperature = get_cur_temp() 
    current_charge = get_cur_charge() 
    current_battery_healthy = get_cur_battery_health()

    # If battery is not healthy, C >80, T > 40
    if not current_battery_healthy or current_charge > 80 or current_temperature > 40: 
        return length_of_fast_charge
    else: 
        time1 = (80-current_charge)/3 #from C = C_0 + 3t
        time2 = (40-current_temperature)*2 # from T = T_0 + 0.5t 
        return min(time1,time2)
    
def set_cur_temp(new_value): 
    global cur_temp
    cur_temp = new_value 

def set_cur_charge(new_value): 
    global cur_charge
    cur_charge = new_value

def get_cur_temp():
    global cur_temp 
    return cur_temp 

def get_cur_charge():
    global cur_charge
    return cur_charge

def get_cur_battery_health():
    global good_battery_health
    return good_battery_health

def charge_time_needed(minutes):
    battery_use_desired = minutes * 2 
    delta_battery_amount = battery_use_desired - get_cur_charge() 
    charge_time = 0
    if delta_battery_amount <= 0: 
        return charge_time
    # Check if battery can even still be fully charged
    elif get_cur_battery_health(): 
        charge_time = duration_fast_charge_possible() # Get amount of time possible for fast charging, 





# Test Cases
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
