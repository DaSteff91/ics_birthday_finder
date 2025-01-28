from ics import Calendar, Event
import questionary
import os

def extract_and_select_birthdays(input_file, output_file):
    # Read the .ics file
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            calendar = Calendar(file.read())
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
        return
    
    # Filter for yearly repeating events
    potential_birthdays = []
    for event in calendar.events:
        if event.name and event.rrule and "FREQ=YEARLY" in event.rrule:
            potential_birthdays.append(event)
    
    if not potential_birthdays:
        print("No yearly recurring events found.")
        return

    # Batch overview of all potential birthdays
    print("\nDetected yearly recurring events (potential birthdays):\n")
    for i, event in enumerate(potential_birthdays, start=1):
        print(f"{i}. {event.name} - {event.begin.date()}")
    
    # Interactive selection
    print("\nSelect which events to export:\n")
    selected_events = []
    for event in potential_birthdays:
        answer = questionary.select(
            f"Export '{event.name}' scheduled on {event.begin.date()}?",
            choices=["Yes", "No"]
        ).ask()
        if answer == "Yes":
            selected_events.append(event)

    # Create a new calendar with the selected events
    new_calendar = Calendar(events=selected_events)

    # Save the new calendar to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(new_calendar.serialize_iter())

    print(f"\nSelected birthdays saved to {output_file}")

# Input and output file paths
input_ics = input("Enter the path to the input .ics file: ").strip()
output_ics = input("Enter the path to save the new .ics file: ").strip()

# Ensure output directory exists
os.makedirs(os.path.dirname(output_ics), exist_ok=True)

# Run the function
extract_and_select_birthdays(input_ics, output_ics)
