from datetime import date
from satsearch import Search


def get_satellite_image(coords):
    # set the date parameters for searching
    start_date = '2021-04-07T00:00:00Z'
    end_date = date.today().strftime('%Y-%m-%dT00:00:00Z')

    # search for a satellite image match
    search = Search(
        bbox=coords,
        datetime=start_date + '/' + end_date,
        url='https://earth-search.aws.element84.com/v0')

    # only record the latest one
    items = search.items(limit=1)

    # try to find a better way to do this
    keys = [k for i in items for k in i.assets]

    # download the latest one
    filename = items[0].download(
        keys[0],
        filename_template='satellite_images/image')

    return filename
