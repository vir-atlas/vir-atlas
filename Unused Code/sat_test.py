# this environment variable is required for this to work
# documentation says it can be passed in through Search(), but it doesn't say how
# export STAC_API_URL='https://earth-search.aws.element84.com/v0'
# TODO: add a way to specify where the file is saved and what it gets named

from satsearch import Search
from satstac import ItemCollection
from datetime import date

def retrieveSatelliteImage(min_lon, min_lat, max_lon, max_lat):
	'''retrieve a satellite image with min and max coordinates as corners'''
	start_date = '2021-03-25T00:00:00Z'
	end_date = date.today().strftime('%Y-%m-%dT00:00:00Z')

	search = Search(bbox=[min_lon, min_lat, max_lon, max_lat],
					datetime=start_date + '/' + end_date,
					url='https://earth-search.aws.element84.com/v0')

	print(search)

	items = search.items(limit=1)

	keys = [k for i in items for k in i.assets]

	filename = items[0].download(
		keys[0],
		filename_template='satellite_images/image')

	return filename

print(retrieveSatelliteImage(-110, 39.5, -109, 40.5))