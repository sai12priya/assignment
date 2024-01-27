import csv
from collections import defaultdict
from datetime import datetime, timedelta

#file paths
file_path = 'C:\\Users\\DELL\\Desktop\\assignment\\data\\data.csv'
output_file_path = 'C:\\Users\\DELL\\Desktop\\assignment\\data\\output.txt'


# Creating a defaultdict to store employee data
employee_data = defaultdict(lambda: {'dates': set(), 'entries': []})

# reading the CSV file and processed the data
with open(file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        position_id = row['Position ID']
        time = row['Time']
        timecard_hours = row.get('Timecard Hours (as Time)', '')  
        employee_name = row.get('Employee Name', '') 

        # Check if the 'Time' column is not empty
        if time:
            # Extract only the date part from the 'Time' column
            time_date = datetime.strptime(time, '%m/%d/%Y %I:%M %p').strftime('%m/%d/%Y')

            
            if position_id and time_date and timecard_hours:
                # Check if the date is not already recorded for the position
                if time_date not in employee_data[position_id]['dates']:
                    
                    employee_data[position_id]['entries'].append((time_date, timecard_hours, employee_name))
                    employee_data[position_id]['dates'].add(time_date)


with open(output_file_path, 'w') as output_file:
   
    print("Solution A:", file=output_file)

    for position_id, data in employee_data.items():
        
        employee_name = data['entries'][0][2] if data['entries'] and len(data['entries'][0]) > 2 else 'Unknown'
        
        # Checking for consecutive 7 or more days
        consecutive_days = False
        if len(data['dates']) >= 7:
            dates_list = sorted(data['dates'])
            for i in range(len(dates_list) - 6):
                start_date = datetime.strptime(dates_list[i], '%m/%d/%Y')
                end_date = datetime.strptime(dates_list[i + 6], '%m/%d/%Y')
                if (end_date - start_date).days == 6:
                    consecutive_days = True
                    break

        
        if consecutive_days:
            print(f"{position_id} ; {employee_name}", file=output_file)

employee_data_solution_b = defaultdict(list)


employee_data_solution_b = defaultdict(list)

with open(file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        position_id = row['Position ID']
        time = row['Time']
        time_out = row['Time Out']
        employee_name = row['Employee Name']

        
        if position_id and time and time_out and employee_name:
            
            employee_data_solution_b[position_id].append((time, time_out, employee_name))

# Append the result to the output file
with open(output_file_path, 'a') as output_file:  
    
    print("\n\nSolution B:", file=output_file)

    for position_id, data in employee_data_solution_b.items():
      
        employee_name = data[0][2] if data and len(data[0]) > 2 else 'Unknown'

        # Calculating and print the time differences
        time_differences = []
        for i in range(len(data) - 1):
            time_diff = datetime.strptime(data[i + 1][0], '%m/%d/%Y %I:%M %p') - datetime.strptime(data[i][1], '%m/%d/%Y %I:%M %p')
            time_differences.append(time_diff.total_seconds() / 3600)  # Convert to hours

        # Check if any value in the time differences list is > 1 and < 10
        if any(1 < diff < 10 for diff in time_differences):
            
            print(f"{position_id}; {employee_name}", file=output_file)





time_cards_solution_c = defaultdict(list)


with open(file_path, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        position_id = row['Position ID']
        timecard_hours_raw = row.get('Timecard Hours (as Time)', '')  
        employee_name = row.get('Employee Name', '')  

        
        if position_id and timecard_hours_raw and employee_name:
            # Convert the timecard hours to a list of timedelta objects
            timecard_hours = [
                timedelta(hours=int(part.split(':')[0]), minutes=int(part.split(':')[1]))
                for part in timecard_hours_raw.split(',')
            ]

            
            time_cards_solution_c[position_id].extend(zip(timecard_hours, [employee_name]*len(timecard_hours)))

with open(output_file_path, 'a') as output_file:  
    
    print("\n\nSolution C:", file=output_file)

    for position_id, time_cards in time_cards_solution_c.items():
        # Check if any time card is greater than 14 hours
        if any(hours.total_seconds() / 3600 > 14 for hours, _ in time_cards):
           
            employee_name = time_cards[0][1]
            
            print(f"{position_id}; {employee_name}", file=output_file)

print(f"Output saved to {output_file_path}")