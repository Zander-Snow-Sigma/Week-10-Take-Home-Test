# A team of analysts wish to discover how far people are travelling to their nearest
# desired court. We have provided you with a small test dataset so you can find out if
# it is possible to give the analysts the data they need to do this. The data is in
# `people.csv` and contains the following columns:
# - person_name
# - home_postcode
# - looking_for_court_type

# The courts and tribunals finder API returns a list of the 10 nearest courts to a
# given postcode. The output is an array of objects in JSON format. The API is
# accessed by including the postcode of interest in a URL. For example, accessing
# https://courttribunalfinder.service.gov.uk/search/results.json?postcode=E144PU gives
# the 10 nearest courts to the postcode E14 4PU. Visit the link to see an example of
# the output.

# Below is the first element of the JSON array from the above API call. We only want the
# following keys from the json:
# - name
# - dx_number
# - distance
# dx_number is not always returned and the "types" field can be empty.

"""
[
    {
        "name": "Central London Employment Tribunal",
        "lat": 51.5158158439741,
        "lon": -0.118745425821452,
        "number": null,
        "cci_code": null,
        "magistrate_code": null,
        "slug": "central-london-employment-tribunal",
        "types": [
            "Tribunal"
        ],
        "address": {
            "address_lines": [
                "Victory House",
                "30-34 Kingsway"
            ],
            "postcode": "WC2B 6EX",
            "town": "London",
            "type": "Visiting"
        },
        "areas_of_law": [
            {
                "name": "Employment",
                "external_link": "https%3A//www.gov.uk/courts-tribunals/employment-tribunal",
                "display_url": "<bound method AreaOfLaw.display_url of <AreaOfLaw: Employment>>",
                "external_link_desc": "Information about the Employment Tribunal"
            }
        ],
        "displayed": true,
        "hide_aols": false,
        "dx_number": "141420 Bloomsbury 7",
        "distance": 1.29
    },
    etc
]
"""

# Use this API and the data in people.csv to determine how far each person's nearest
# desired court is. Generate an output (of whatever format you feel is appropriate)
# showing, for each person:
# - name
# - type of court desired
# - home postcode
# - nearest court of the right type
# - the dx_number (if available) of the nearest court of the right type
# - the distance to the nearest court of the right type

import pandas as pd
import requests

COURTS_API_URL = "https://www.find-court-tribunal.service.gov.uk/search/results.json?postcode="


def load_csv_data(file: str) -> pd.DataFrame:
    """Returns the csv data from a file as a pd.DataFrame."""

    return pd.read_csv(file)


def get_nearest_courts_data(postcode: str) -> list:
    """Returns information about the nearest courts to a given postcode."""

    response = requests.get(COURTS_API_URL + postcode)

    if response.status_code == 200:
        return response.json()

    raise requests.HTTPError(
        f"{response.status_code} Error")


def add_court_info_to_dataframe(df: pd.DataFrame, court_data: list, index: int) -> None:
    """Adds the relevant court data to the data frame at the specified index."""
    for court in court_data:
        if df.at[index, 'looking_for_court_type'] in court['types']:
            df.at[index, 'court_name'] = court['name']
            df.at[index, 'distance_to_court'] = court['distance']
            df.at[index, 'court_dx_number'] = court.get('dx_number')
            break


if __name__ == "__main__":

    get_nearest_courts_data("asff")

    data = load_csv_data("people.csv")
    data['court_name'] = None
    data['distance_to_court'] = None
    data['court_dx_number'] = None

    for i in data.index:
        court_data = get_nearest_courts_data(data.at[i, 'home_postcode'])
        court_data.sort(key=lambda x: x['distance'])
        add_court_info_to_dataframe(data, court_data, i)

    data.to_csv("report.csv", index=False)
    data.to_markdown("report.md", index=False)
