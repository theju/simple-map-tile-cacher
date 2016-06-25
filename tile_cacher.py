import os
import json
import time
import random
import asyncio
import requests
import functools

from bottle import Bottle, route, run, response, redirect


app = Bottle()
loop = asyncio.get_event_loop()
config = None


def download_tile(frag, path):
    output_path = os.path.join(config["tiles"]["output_path"], path)
    response = requests.get(config["tiles"]["url"].format(frag) + path)
    try:
        os.makedirs(os.path.dirname(output_path))
    except OSError:
        pass
    ff = open(output_path, "wb")
    ff.write(response.content)
    ff.close()
    return response


@app.route("/<xx>/<yy>/<zz>.<ext>")
def index(xx=None, yy=None, zz=None, ext=None):
    subdomains = config["tiles"]["subdomains"]
    tiles_dir = config["tiles"]["output_path"]
    max_age = config["max_age"]
    tiles_url = config["tiles"]["url"]

    tiles_path = "{0}/{1}/{2}.{3}".format(xx, yy, zz, ext)

    filename = os.path.join(tiles_dir, tiles_path)
    try:
        result = os.stat(filename)
        if result.st_mtime + max_age < time.time():
            raise FileNotFoundError
        response.content_type = "image/{0}".format(ext)
        response.headers["Cache-Control"] = "public, max-age={0}".format(max_age)
        return open(filename, "rb")
    except FileNotFoundError:
        frag = random.choice(subdomains)
        loop.run_in_executor(None, download_tile, frag, tiles_path)
        redirect(tiles_url.format(frag) + "/" + tiles_path)


if __name__ == '__main__':
    try:
        config = json.load(open("config.json"))
    except FileNotFoundError:
        print("Missing config.json file in current directory")
        loop.close()
    if config:
        try:
            server_kwargs = config["server"]
            run_func = functools.partial(run, **server_kwargs)
            fut = loop.create_task(run_func(app))
            loop.run_until_complete(fut)
        except KeyboardInterrupt:
            pass
        finally:
            loop.close()
