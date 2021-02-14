import requests
import sys
import os


class VirusTotalApi:

    def __init__(self):
        self.base_api_url =  "https://www.virustotal.com/vtapi/v2"
        self.api_key = self.__get_vt_api_key()

    def get_ip_address_report(self, ip_address):
        return self.__vt_api_call(f"{self.base_api_url}/ip-address/report",
                                  {"apikey": self.api_key, "ip": ip_address})

    def get_domain_report(self, domain):
        return self.__vt_api_call(f"{self.base_api_url}/domain/report",
                                  {"apikey": self.api_key, "domain": domain})

    def get_url_report(self, url):
        return self.__vt_api_call(f"{self.base_api_url}/url/report",
                                  {"apikey": self.api_key, "resource": url})

    def get_file_report(self, file_hash):
        return self.__vt_api_call(f"{self.base_api_url}/file/report",
                                  {"apikey": self.api_key, "resource": file_hash})

    @staticmethod
    def __vt_api_call(url, params):
        resp = requests.get(url=url, params=params)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 204:
            print("VT API Rate Limiting (4 req/min) was reached!!!")
        return None

    @staticmethod
    def __get_vt_api_key() -> str:
        if os.getenv("VT_API_KEY") and len(os.getenv("VT_API_KEY")) == 64:
            return os.getenv("VT_API_KEY")
        else:
            print("Could not load VT API key!", file=sys.stderr)
            sys.exit(1)
