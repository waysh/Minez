import csv

def new_settings():
    return
    
def commit(val):
    with open('config.txt', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['width','height','mines'])
        writer.writerow(val)

def read_settings():
    try:
        with open('config.txt') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                return row.values()
    except:
        with open('config.txt', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['width','height','mines'])
            writer.writerow(['15','15','75'])
            return ['15','15','75']
