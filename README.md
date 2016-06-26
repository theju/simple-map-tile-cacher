## Map Tile Cacher

A simple web-service that caches tiles from mapping services like [OpenStreetMap](https://www.openstreetmap.org/).
to disk for a specified duration.

## Installation

You require Python3.4.3 or more. Ubuntu 14.04 and above should suffice.

Install [virtualenv](https://virtualenv.pypa.io/en/stable/) and then run the
following commands

```bash
$ virtualenv tc_env
$ source tc_env/bin/activate
$ git clone https://github.com/theju/simple-map-tile-cacher/
$ cd simple-map-tile-cacher
$ pip install -r requirements.txt
# Create a config.json (more below in the configuration section)
$ python tile_cacher.py
```

## Configuration

A `config.json` file is searched for within the current directory. The file
may look like below

```json
{
    "server": {
        "server": "wsgiref",
        "host": "localhost",
        "port": 8001
    },
    "tiles": {
        "url": "https://{0}.tile.openstreetmap.org/",
        "subdomains": ["a", "b", "c"],
        "output_path": "/home/ubuntu/tiles"
    },
    "max_age": 3600
}
```
The `server` object is the keywords that are passed to the bottle.py's
(run)[http://bottlepy.org/docs/dev/api.html#bottle.run] function.
The `tiles` object contains the `url` of the tiles (could be OSM, Mapbox etc).
The `tiles` object also contains a `subdomains` attribute which holds all value
of all subdomains of the tiles server. The `output_path` is where all the tiles
are cached. The `max_age` is how frequently should the tiles be refreshed.

## License

Released under the `MIT License`. Please refer to the `LICENSE.txt` for more details.

## Notes

- The primary motivation for writing this was to learn about Python3's asyncio.
- Please don't forget to add the [attribution](https://www.openstreetmap.org/copyright) if using OpenStreetMap's tiles.
