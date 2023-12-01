"""
Script which finds how far each person's nearest court is of their desired type.
- Produces both a csv report and a markdown report of the findings.
"""


import pandas as pd
import requests

COURTS_API_URL = "https://www.find-court-tribunal.service.gov.uk/search/results.json?postcode="
SUCCESSFUL_STATUS_CODE = 200
PEOPLE_CSV_FILE = "people.csv"


def load_csv_data(file: str) -> pd.DataFrame:
    """Returns the csv data from a file as a pd.DataFrame."""

    return pd.read_csv(file)


def get_nearest_courts_data(postcode: str) -> list:
    """Returns information about the nearest courts to a given postcode."""

    response = requests.get(COURTS_API_URL + postcode, timeout=10)

    if response.status_code == SUCCESSFUL_STATUS_CODE:
        return response.json()

    raise requests.HTTPError(
        f"{response.status_code} Error")


def add_court_info_to_dataframe(dataframe: pd.DataFrame, court_info: list, index: int) -> None:
    """Adds the relevant court data to the data frame at the specified index."""
    for court in court_info:
        if dataframe.at[index, 'looking_for_court_type'] in court['types']:
            dataframe.at[index, 'court_name'] = court['name']
            dataframe.at[index, 'distance_to_court'] = court['distance']
            dataframe.at[index, 'court_dx_number'] = court.get('dx_number')
            break


if __name__ == "__main__":

    data = load_csv_data(PEOPLE_CSV_FILE)
    data['court_name'] = None
    data['distance_to_court'] = None
    data['court_dx_number'] = None

    for i in data.index:
        court_data = get_nearest_courts_data(data.at[i, 'home_postcode'])
        court_data.sort(key=lambda x: x['distance'])
        add_court_info_to_dataframe(data, court_data, i)

    data.to_csv("report.csv", index=False)
    data.to_markdown("report.md", index=False)
