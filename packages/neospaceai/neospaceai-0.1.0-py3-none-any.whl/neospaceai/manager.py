import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class Manager:
  def __init__(self, host="https://foymabhkqri53clg7epea6hfhi.apigateway.us-chicago-1.oci.customer-oci.com"):
    self.host = host
    self.session = requests.Session()
    retry = Retry(connect=3, backoff_factor=.5)
    adapter = HTTPAdapter(max_retries=retry)
    self.session.mount('http://', adapter)


  def getCycles(self, cycle_name):
    url = f"{self.host}/v1/cycles/{cycle_name}/executions"
    try:
      data = self.session.get(url)
      return data.json()

    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      return None

  def getModelById(self, model_id):
    url = f"{self.host}/v1/models/{model_id}"
    try:
      data = self.session.get(url)
      return data.json()

    except requests.exceptions.RequestException as e:
      print(f"An error occurred: {e}")
      return None