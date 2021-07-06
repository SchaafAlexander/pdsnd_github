import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

month_comparison = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
day_comparison = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters(month_comparison, day_comparison):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = None
    month = None
    day = None
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while city not in CITY_DATA.keys():
        city = input("Choose your city of interest (Chicago, New York City or Washington): ").lower()
        print('City of choice: {}'.format(city))
        
    # get user input for month (all, january, february, ... , june)
    while month not in month_comparison:
        month = input("Enter month name please (January, February, March, April, May, June or all): ").lower()
        print('month of choice: {}'.format(month))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while day not in day_comparison:
        day = input("Enter day of interest please please (Monday, Tuesday, ... or all): ").lower()
        print('Day of choice: {}'.format(day))

    print('-'*40)
    return city, month, day


def load_data(city, month, day, month_comparison):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = month_comparison.index(month) + 1
        print(month)
        
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df, month_comparison):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    mc_month = df['month'].mode()[0]
    print("Most common month: {}".format(month_comparison[mc_month-1].title()))
    
    # display the most common day of week
    mc_day = df['day_of_week'].mode()[0]
    print("Most common day of week: {}".format(mc_day))

    # display the most common start hour
    mc_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most common start hour: {}".format(mc_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].mode()[0]
    print("Most common start station: {}".format(mc_start_station))

    # display most commonly used end station
    mc_end_station = df['End Station'].mode()[0]
    print("Most common end station: {}".format(mc_end_station))

    # display most frequent combination of start station and end station trip
    mfc_stations = (df['Start Station'] + " || " + df['End Station']).mode()[0]
    print("Most frequent combination fo start and end station: {}".format(mfc_stations))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("Total travel time: {} [s]".format(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time: {} [s]".format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    cnt_user_type = df.groupby(['User Type'])['User Type'].count()
    print(cnt_user_type.to_string())
    
    #check if column 'Gender' exists (due to missing columns 'Gender' and 'Birth Year' for Washington)
    if 'Gender' in df.columns:
    
        # Display counts of gender
        df = df.dropna(axis = 0)
        cnt_gender = df.groupby(['Gender'])['Gender'].count()
        print(cnt_gender.to_string())

        # Display earliest, most recent, and most common year of birth
        #Earliest YoB
        earliest_year_ob = df['Birth Year'].min()
        print("Earliest Year of Birth: {}".format(int(earliest_year_ob)))
        #Most recent YoB
        mr_year_ob = df['Birth Year'].max()
        print("Most recent Year of Birth: {}".format(int(mr_year_ob)))
        #Most common YoB
        mc_year_ob = df['Birth Year'].mode()[0]
        print("Most common Year of Birth: {}".format(int(mc_year_ob)))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df,index):
    """Displaying raw data 5 rows each time."""

    print('\nDisplaying 5 rows each time...\n')
    start_time = time.time()
    
    #Display 5 raw data rows each request
    for i in range(index,index+5):
        print('\n',df.iloc[i,:].to_dict())
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def main():
    """Main function. Where all the other functions get triggered."""
    while True:
        city, month, day = get_filters(month_comparison, day_comparison)
        df = load_data(city, month, day, month_comparison)

        time_stats(df, month_comparison)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
        index = 0
        while raw.lower() == 'yes':
            raw_data(df,index)
            raw = input('\nWould you like to see 5 rows of raw data? Enter yes or no.\n')
            index += 5
            

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
