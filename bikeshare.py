import time
import pandas as pd
import numpy as np
import sys

#Functions to print colored text and background 
def prRed(skk): print("\033[91m{}\033[00m" .format(skk)) 
def prGreen(skk): print("\033[92m{}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m{}\033[00m" .format(skk)) 
def prPurple(skk): print("\033[95m{}\033[00m" .format(skk)) 

#Datasets reference 
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

#global lists:
cityList = ['Chicago', 'New York City', 'Washington']
dayList = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
monthList = ['January','February','March','April','May','June']

def greet():
#Greet user. Let them know the purpose of RideSolo app

    prLightPurple("-"*80)
    prGreen("Welcome to RideSolo") 
    print('Your home for finding opportunities for riding a bike share alone!')
    prLightPurple("-"*80)

    if input("Are you ready to find a solo bike ride? If so, type 'Yes': ").title() == "Yes":
        print("-"*80+"\n"+"Ok, let's go!"+"\n"+"-"*80)
    else:
        print('Okay, thanks for coming by. Feel free to restart if you change your mind.')
        sys.exit(0)
        
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    promptCity = "In what city's would you like to ride alone? \n(Type \'list\' to see a list of cities.) "
    
    city = input(promptCity).title()

    while city not in cityList:
        if city == "List":
            print("Washington, Chicago, New York City")
            city = input("What city's data woud you like to explore?").title()
        else:
            city = input(promptCity+ "Please try again. ").title()

    prPurple("-"*80)
    print("You've selected: \n")
    prRed(city)
    prPurple('\n'+"-"*80)

    # get user input for month (all, january, february, ... , june)
    
    month_name = input("For what month are you planning your trip? \n(Type \'list\' to see list of available months.)").title()
    
    while month_name not in monthList:
        if month_name == "List":
                strMonthList=''
                for month in monthList:
                    strMonthList+=month+", "
                print(strMonthList[:-2])
                month_name = input("For what month are you planning your trip?").title()
        else:
            month_name = input("It doesn\'t look like we have data on that month. Please try again. ").title()
    
    month_num = monthList.index(month_name) +1

    # get user input for day of week (all, monday, tuesday, ... sunday)
    
    day_name = input("For what day are you planning your trip?").title()
    
    while day_name not in dayList:
        day_name = input("Woops. Did you spell that correctly? Please check your spelling and retype your chosen day.").title()
    
    day_num = dayList.index(day_name) +1

    return city, month_num, day_name


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] =  df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hourtime']=df['Start Time'].dt.strftime('%I:00%p')
    df['hour']=df['Start Time'].dt.hour
    
#    print(type(month))
#    month = int(month)
#    print(type(month))
    
    df = df[(df['month']==month)]
    df = df[(df['day_of_week']==day)]

    return df


def time_stats(df, month, day, city):
    """Ok, we're going to find the best opportunity for you to ride solo!."""

    #display the least common start hour
    least_busy_hourtime = df['hourtime'].value_counts().idxmin()
    
    month_index = month-1
    print("It looks like this the best hour to rent a bike on " + str(day) + "s in " + monthList[month_index] + " in " + str(city) + '.')
    prRed(least_busy_hourtime)
    print('-'*80)
    

def station_stats(df):
    #Displays statistics on the least popular stations and trip.

    print('\nCalculating the least popular stations...\n')
    start_time = time.time()

    # display least commonly used start station
    least_busy_start_location = df['Start Station'].value_counts().idxmin()
    
    print("It looks like least busy start location is ")
        
    prRed(least_busy_start_location)
    print("\n",'-'*80)

    # display least commonly used end station
    least_busy_end_location = df['End Station'].value_counts().idxmin()
    
    print("It looks like least busy end location is ")
        
    prRed(least_busy_end_location)
    print("\n",'-'*80)

    # display least frequent combination of start station and end station trip
    least_busy_start_end_location = df.groupby(['Start Station', 'End Station']).size().idxmin()
    
    print("It looks like least busy start and end location is ")
        
    prRed(least_busy_start_end_location)
    print("\n",'-'*80)



def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # display total travel time
    total_travel_time = (df['Trip Duration'].sum()/2400).astype(int)
    
    print("Total travel time (in hours) on your day is")
    
    prRed(total_travel_time)
    
    # display longest travel time
    longest_travel_time = (df['Trip Duration'].max()/2400).astype(int)
    
    
    print("The longest travel time (in hours) on your day is")
    prRed(longest_travel_time)
    print('-'*80)
  

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nHere is who you will typically run into\n')

    # Display counts of user types
    print('\nHere is a breakdown of the customers\' membership type')
    dfUserTypeCounts = create_new_list(df, 'User Type')
    dfUserTypeCounts.columns=['Count']
    
    print(dfUserTypeCounts)

    #Display counts of gender
    print('\nHere is a breakdown of the customers\' gender')
    dfGenderCounts = create_new_list(df, 'Gender')
    dfGenderCounts.columns=['Count']
    print(dfGenderCounts)

    # Display earliest, most recent, and most common year of birth
    print('\n Here is a breakdown of the customers\' birth dates')
    print("Oldest person's birth year")
    print(df['Birth Year'].min().astype(int))
    print("\nYoungest person's birth year")
    print(df['Birth Year'].max().astype(int))
    print("\nMost frequent birth year")
    print(df['Birth Year'].mode().values[0].astype(int))
    
    print("\n",'-'*80)

def create_new_list(df, columnName):
    #creates new dataframe from two lists
    values = df[columnName].value_counts().values.tolist()
    index = df[columnName].value_counts().index.tolist()
    dfNew = pd.DataFrame(values,index)
    return dfNew

def main():
    while True:
        overall_start_time = time.time()
        greet()
        
        city, month, day = get_filters()
        
        df = load_data(city, month, day)

        time_stats(df, month, day, city)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        print("\nThis took %s seconds." % (time.time() - overall_start_time))
        print('-'*80)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        

if __name__ == "__main__":
	main()
