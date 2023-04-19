from bs4 import BeautifulSoup
from settings import SII_URL, LOGGING_CONFIG, MONTHS_YEAR
from urllib3.exceptions import HTTPError
from datetime import datetime
from exceptions import NotFound
import requests
import logging.config
import logging

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class ParseSii(object):
    """
       A class used to represent a property

       ...

       Attributes
       ----------
       property_id : str
           id of property to find

       Methods
       -------
       _store_property_cache(property_info)
            store in redis the information of property
       _get_property_price_and_currency(property_data)
            parse information to get the price and currency of the property
       find_property()
            find in the graphql of infocasa for the information on price and  type of currency of specific property

    """

    def __init__(self, date: datetime):
        self.date = date

    def get_sii_information(self) -> str:
        """

        :return:
        """
        try:
            logger.info("Make requests from sii page")
            response = requests.get(url=SII_URL.format(str(self.date.year)))
        except requests.exceptions.HTTPError as e:
            logger.error(f"Request Problem exceptions HTTPError {str(e)}")
            raise HTTPError(str(e))
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Request Problem exceptions ConnectionError {str(e)}")
            raise ConnectionError(str(e))
        except requests.exceptions.Timeout as e:
            logger.error(f"Request Problem exceptions Timeout {str(e)}")
            raise TimeoutError(str(e))
        except requests.exceptions.RequestException as e:
            logger.error(f"Request Problem exceptions RequestException {str(e)}")
            raise ValueError(str(e))
        except Exception as e:
            logger.error(f"Request Problem exceptions {str(e)}")
            raise Exception(str(e))
        if response.status_code == 200:
            return response.text
        raise NotFound("Uf from specific date does not exists")

    def parse_html(self, source: str) -> BeautifulSoup:
        """
            Parser the content html

            :param source: html to parse
            :type source: str
            :return: BeautifulSoup parser content
        """
        try:
            logger.info("parse html page")
            parser = BeautifulSoup(source, 'html.parser')
        except Exception as e:
            logger.error(f"ERROR cannot be parser this content {str(e)}")
            raise ValueError(str(e))
        return parser

    def convert_uf_float(self, value: str):
        """
            convert value in tpe float

            :param value: value of uf
            :type value: str
            :return: the value transformed in float type
        """
        transform = 0
        if value != 0:
            transform = value.replace(".", "").replace(",", ".")
        return float(transform)

    def get_uf_sii(self):
        """

        :return:
        """
        try:
            sii_html_parse = self.parse_html(self.get_sii_information())
        except NotFound as e:
            raise NotFound(str(e))
        except Exception as e:
            msg = f"ERROR in obtain html from sii page {str(e)}"
            logger.error(msg)
            raise Exception(msg)
        logger.info("find uf from specific date")
        specific_month = sii_html_parse.find("div", {"id": f"mes_{MONTHS_YEAR.get(str(self.date.month))}"})
        if specific_month is None:
            raise NotFound("Uf from specific date does not exists")
        items = specific_month.select('tr')
        for item in items[1:]:
            days = item.select("th")
            values = item.select("td")
            for day, value in zip(days, values):
                if day.get_text() == str(self.date.day):
                    if value.get_text():
                        return self.convert_uf_float(value.get_text())
                    else:
                        return None
        return None



