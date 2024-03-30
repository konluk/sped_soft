import csv, os

from sped_soft import filename


def get_all_transports():
    all_transports = []

    if os.path.exists(filename):
        with open(filename, mode='r') as file:
            csv_reader = csv.reader(file)
            for f_client_id, f_zip_code, f_city, f_lat, f_lon, f_date in csv_reader:
                all_transports.append([f_client_id, f_zip_code, f_city,
                                       f_lat.split(".")[0] + "/" + f_lon.split(".")[0],
                                       f_date
                                       ])
            all_transports.reverse()
    else:
        return None

    return all_transports


print(get_all_transports())