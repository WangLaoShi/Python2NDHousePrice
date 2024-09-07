import csv

def save_list_to_csv(data, filename):
    """Save a list to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow([item])

def save_set_to_csv(data, filename):
    """Save a set to a CSV file."""
    save_list_to_csv(list(data), filename)

def save_dict_to_csv(data, filename):
    """Save a dictionary to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Key', 'Value'])
        for key, value in data.items():
            writer.writerow([key, value])