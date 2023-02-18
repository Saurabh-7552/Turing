import requests
import warnings
import logging as logger
import re
class LinkProbe:

    def __init__(self, link: str = None):
        self.link = link


    def get_link_probe(self):
        result = dict()
        status = self.__get_link_status_code()
        string_analysis = self.__get_link_string_analysis()
        username_details = self.__get_username()

        if status == 999:
            result['status'] = 'Valid in url'
            result['status_code'] = status
        else:
            result['status'] = 'Invalid in url'
            result['status_code'] = status

        result['string_details'] = string_analysis
        result['username_details'] = username_details

        return result

    def __get_username(self):
        regex = r'^https?://((www|\w\w)\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$'
        details = dict()
        if re.match(regex, self.link):
            if self.link.split('/')[-3] == 'in':
                details['username'] = self.link.split('/')[-2]
            else:
                details['username'] = self.link.split('/')[-1]
        else:
            details['username'] = None

        if details['username'] is not None:
            # Count the number of special characters
            special_chars = len(re.findall(r'[^\w\s]', details['username']))
            details['special_chars'] = special_chars

            # Count the number of alphabetical characters
            alpha_chars = len(re.findall(r'[a-zA-Z]', details['username']))
            details['alpha_chars'] = alpha_chars

            # Count the number of numeric characters
            num_chars = len(re.findall(r'\d', details['username']))
            details['num_chars'] = num_chars

        return details

    def __get_link_string_analysis(self):

        regex = r'^https?://((www|\w\w)\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$'
        details = dict()

        if re.match(regex, self.link):
            details['link_regex'] = 'Valid'
        else:
            details['link_regex'] = 'Invalid'

        # Count the number of special characters
        special_chars = len(re.findall(r'[^\w\s]', self.link))
        details['special_chars'] = special_chars

        # Count the number of alphabetical characters
        alpha_chars = len(re.findall(r'[a-zA-Z]', self.link))
        details['alpha_chars'] = alpha_chars

        # Count the number of numeric characters
        num_chars = len(re.findall(r'\d', self.link))
        details['num_chars'] = num_chars

        return details



    def __get_link_status_code(self):
        try:
            response = requests.get(self.link)
            return response.status_code
        except Exception as e:
            logger.error(e)
            return 'error'
