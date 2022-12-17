from collections import namedtuple
import re

with open('specifications.txt', 'rt') as file:
    specifications = file.read()

specs = namedtuple('specs', 'range regex')
#specs range builtin module
#specs regex from re.compile

req_regex = re.compile(
    r"requirements: between (?P<low>\d+) and (?P<high>\d+).*")


def get_linkedin_dict():
    '''Convert specifications into a dict where:
       keys: feature
       values: specs namedtuple'''
    res = dict()
    for line in specifications.splitlines():
        line = line.lstrip()
        if line.startswith('feature'):
            feature = line.split(':')[-1].strip()
        elif line.startswith('requirements'):
            rng = range(*[int(val)
                        for val in req_regex.search(line).groups()])
        elif 'characters:' in line:
            char_str = line.split(':')[-1].strip().replace(' ', '').replace('.', '\\.')
            # allowed character range to be used in regex
            if feature == 'custom_url':
                reg_str = f"^[{char_str}]+$"
            elif feature == 'login':
                reg_str = f"^[{char_str}]+@[{char_str}]+[\\.com|\\.net|\\.org]$"
        elif len(line) == 0:
            res[feature] = specs(rng, re.compile(reg_str))
    return res


def check_linkedin_feature(feature_text, url_or_login):
    '''Raise a ValueError if the url_or_login isn't login or custom_url
       If feature_text is valid, return True otherwise return False'''
    valid_modes = ['custom_url', 'login']
    if url_or_login not in valid_modes:
        raise ValueError(f"url_or_login must be one of: {valid_modes}")
    spc = get_linkedin_dict()[url_or_login]
    if len(feature_text) not in spc.range:
        return False
    if spc.regex.match(feature_text) is None:
        return False
    return True

    
