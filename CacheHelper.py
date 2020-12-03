from os import name
import json
import urllib.request
import urllib.parse
import urllib.error
import os


class CacheHelper:

    def read_cache(self, CACHE_FNAME):
        """
        This function reads from the JSON cache file and returns a dictionary from the cache data.
        If the file doesn’t exist, it returns an empty dictionary.
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        CACHE_FILE = dir_path + '/' + CACHE_FNAME + ".json"
        try:
            # Try to read the data from the file
            cache_file = open(CACHE_FILE, 'r', encoding="utf-8")
            cache_contents = cache_file.read()  # If it's there, get it into a string
            # And then load it into a dictionary
            CACHE_DICTION = json.loads(cache_contents)
            # Close the file, we're good, we got the data in a dictionary.
            cache_file.close()
            return CACHE_DICTION
        except:
            CACHE_DICTION = {}
            return CACHE_DICTION


    def write_cache(self, cache_file, cache_dict):
        """
        This function encodes the cache dictionary (CACHE_DICT) into JSON format and
        writes the JSON to the cache file (CACHE_FNAME) to save the search results.
        """
        dumped_json_cache = json.dumps(cache_dict)
        fw = open(cache_file + ".json", 'w')
        fw.write(dumped_json_cache)
        fw.close()
