import urllib.request
import re
import requests
from html.entities import name2codepoint
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class AdvisorReader:
    """
    Class to parse advisor information from math genealogy.
    """
    def __init__(self, _id):
        """
        Parses information for mathematician with mathgenealogy id `_id`.
        """
        self.id = _id
        self.name = None
        self.institution = None
        self.year = None
        self.advisors = []
        self.page_str = None


    def get_page(self):
        """
        Retrieve page from genealogy database.
        """
        url = f'https://www.genealogy.math.ndsu.nodak.edu/id.php?id={self.id}'
        with urllib.request.urlopen(url) as page:
            self.page_str = page.read()
            self.page_str = self.page_str.decode('utf-8')

    def parse_page_information(self):
        """
        Parses raw webpage for data.

        NOTE: This is fragile and could break without notice.
        """
        if self.page_str is None:
            self.get_page()

        lines = self.page_str.split('\n')

        if lines[0].find("You have specified an ID that does not exist") > -1:
            raise ValueError(f"Invalid page address for id {self.id}")

        idx = 0
        while idx < len(lines):
            line = lines[idx]
            if line.find("h2 style=") > -1:  # Main name
                idx += 1
                line = lines[idx]
                self.name = unescape(line.split('</h2>')[0].strip())
            if '#006633; margin-left: 0.5em">' in line:
                inst_year = line.split('#006633; margin-left: 0.5em">')[1].split("</span>")[:2]
                self.institution = unescape(inst_year[0].strip())
                if self.institution == "":
                    self.institution = None
                if inst_year[1].split(',')[0].strip().isdigit():
                    self.year = int(inst_year[1].split(',')[0].strip())
            if 'Advisor' in line:
                self.advisors = extract_advisor_names(line)
            if 'According to our current on-line database' in line:
                break
            idx += 1
        return [self.name, self.institution, self.year, self.advisors]


def extract_advisor_names(line):
    """
    Extracts advisor names from a line of HTML containing anchor tags.
    """
    names = re.findall(r"<a href=\"id\.php\?id=\d+\">([^<]+)</a>", line)
    return names


def unescape(string):
    """
    Given html entities like &aacute; for example, just return the
    character.
    """
    return re.sub('&(%s);' % '|'.join(name2codepoint),
                  lambda m: chr(name2codepoint[m.group(1)]), string)


def find_id_for_name(name):
    """
    Queries mathgenealogy for a name and returns the id (if found).
    Raises KeyError if not found, or if not unique.
    """
    url = "https://www.mathgenealogy.org/quickSearch.php"
    form_data = {
        'searchTerms': name,
        'Submit': 'Search',
    }
    try:
        response = requests.post(url, data=form_data, timeout=15)
        response.raise_for_status()
        # soup = BeautifulSoup(response.content, 'html.parser')
    except requests.exceptions.RequestException as e:
        print(f"Error during request: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    return _response_to_id(response, name)


def _response_to_id(response, name):
    """
    Parse response for id.
    """
    if 'quickSearch.php' in response.url:
        raise KeyError(f"{name} not found uniquely in database.")
    match = re.search(r"id=(\d+)", response.url)
    if match:
        return match.group(1)
    raise KeyError(f"Unexpected URL for {name}.")


def get_advisors(name):
    _id = find_id_for_name(name)
    areader = AdvisorReader(_id)
    name, inst, year, advisors = areader.parse_page_information()
    return advisors
