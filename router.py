import os.path
import urllib2
import re

POKEAPI_URL = "http://pokeapi.co/"


class Router():
    def dispatch(self, path, response):
        full_url = path.split("?")
        url = full_url[0]

        param_hash = {}
        if(len(full_url) > 1):
            params = full_url[1].s
            param_hash = dict([pair.split("=") for pair in params.split("&")])

        routes = {
            "^/index.html$": {
                'content_type': "text/html",
                'response': self.get_file,
            },
            "^/data/static/.*\.html$": {
                'content_type': "text/html",
                'response': self.get_file,
            },
            "^/data/static/.*\.js$": {
                'content_type': "application/javascript",
                'response': self.get_file,
            },
            "^/data/static/.*\.css$": {
                'content_type': "text/css",
                'response': self.get_file,
            },
            "^/data/static/.*\.png$": {
                'content_type': "image/png",
                'response': self.get_file,
            },
            "^/query/.*": {
                'content_type': "application/json",
                'response': self.do_query
            },
            "^/data/(api/.*)": {
                'content_type': "application/json",
                'response': self.get_api_data
            },
            "^/data/(media/.*)\.png$": {
                'content_type': "image/png",
                'response': self.get_api_data,
            },
        }

        content = ""
        try:
            matched = False
            for route in routes:
                match = re.match(route, url)
                if(match):
                    content = routes[route]['response'](url, param_hash,
                                                        match, response)
                    response.send_header("Content-type",
                                         routes[route]['content_type'])
                    matched = True
                    break

            if(not matched):
                response.send_error(404)

        except UpstreamError:
            response.send_error(404)

        return content

    def get_api_data(self, path, params, regex, response):
        path = re.sub("/$", "", path)
        disk_path = "./"+path
        if(os.path.isfile(disk_path)):
            response.send_response(200)
            return self.read_file(disk_path)
        else:
            api_path = regex.groups()[0]
            content = urllib2.urlopen("{0}/{1}".format(POKEAPI_URL, api_path))
            if(content.getcode() == 200):
                data = content.read()
                self.write_file(disk_path, data)
                response.send_response(200)
                return data
            else:
                raise UpstreamError("Could not find upstream resource")

    def get_file(self, path, params, regex, response):
        disk_path = "./"+path
        print disk_path
        if(os.path.isfile(disk_path)):
            response.send_response(200)
            return self.read_file(disk_path)
        else:
            raise UpstreamError("Could not find file {0}".format(path))

    def do_query(self, path, params, regex, response):
        response.send_response(200)
        return "query"

    def read_file(self, path):
        to_read = open(path, 'rb')
        content = to_read.read()
        to_read.close()
        return content

    def write_file(self, path, data):
        if(not os.path.exists(os.path.dirname(path))):
            os.makedirs(os.path.dirname(path))
        to_write = open(path, 'wb')
        to_write.write(data)
        to_write.close()
        return


class UpstreamError(Exception):
    def __init__(self, message):
        self.message = message
