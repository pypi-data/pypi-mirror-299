
import re
import json
import scrapy
from urllib.parse import urlencode
from scrapy.loader import ItemLoader
from datetime import datetime
import pytz


def clean_text(text):

    if text is None:

        return '-'

    if text is not None:

        cleaned_value = re.sub(r'<(?!br\s?\/?)[^>]*>', '', text)
                
        # Remove leading and trailing whitespaces, including newline characters
        cleaned_value = cleaned_value.strip()

        # Replace consecutive newline characters with a single space
        cleaned_value = re.sub(r'\n+', ' ', cleaned_value)

        # Replace other unwanted characters
        cleaned_value = cleaned_value.replace("\xa0", "").replace("  ","").replace("m<sup>2</sup>","").replace("m<sup>3</sup>","").replace("\r","").replace("\t","").replace("<span>","").replace("</span>","").strip()

        # Use strip() to remove leading and trailing whitespace and newline characters
        return cleaned_value
    
class IndeedJobSpider(scrapy.Spider):
  name = "indeed_jobs"

  def get_indeed_search_url(self, keyword, location, offset=0, radius =50,fromage=14):
      parameters = {
          "q": keyword,
          "l": location,
          "filter": 0,
          "start": offset,
          "sort": "date",
          'radius': radius,
          "fromage": fromage  # Added fromage parameter (search jobs from the last n days)
      }
      return "https://nl.indeed.com/jobs?" + urlencode(parameters)

  def start_requests(self):
    #parameters sent to the proxy api, fromage means the number of days that the ad has been placed on indee, and radius means the number of kilometers from the search word in location list.
    keyword_list = ['python']
    location_list = ['nederland']
    fromage = 14
    radius = 50

    for keyword in keyword_list:
      for location in location_list:
        indeed_jobs_url = self.get_indeed_search_url(keyword, location,radius,fromage)
        yield scrapy.Request(url=indeed_jobs_url,
                             callback=self.parse_search_results,
                             meta={
                                'keyword': keyword,
                                'location': location,
                                'offset': 0,
                                'sort': 'date',
                                'radius': radius,
                                'fromage': fromage

                             })

  def parse_search_results(self, response):
    script_tag = re.findall(
        r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});',
        response.text)
    if script_tag:
      json_blob = json.loads(script_tag[0])

      if response.meta['offset'] == 0:
        meta_data = json_blob["metaData"]["mosaicProviderJobCardsModel"][
            "tierSummaries"]
        num_results = sum(category["jobCount"] for category in meta_data)
        if num_results > 1000:
          num_results = 50

        for offset in range(10, 20, 10):
          url = self.get_indeed_search_url(response.meta['keyword'],
                                           response.meta['location'], 
                                           offset,
                                           response.meta['radius'],
                                           response.meta['fromage'])
          yield scrapy.Request(url=url,
                               callback=self.parse_search_results,
                               meta={
                                   'keyword': response.meta['keyword'],
                                   'location': response.meta['location'],
                                   'offset': offset,
                                   'sort':'date',
                                   'radius': response.meta['radius'],
                                   'fromage': response.meta['fromage']
                               })

      jobs_list = json_blob['metaData']['mosaicProviderJobCardsModel'][
          'results']
      for index, job in enumerate(jobs_list):
        if job.get('jobkey') is not None:
          job_url = 'https://nl.indeed.com/viewjob?viewtype=embedded&jk=' + job.get(
              'jobkey')
          yield scrapy.Request(url=job_url,
                               callback=self.parse_job,
                               meta={
                                'keyword': response.meta['keyword'],
                                'location': response.meta['location'],
                                'offset': response.meta['offset'],
                                'position': index,
                                'jobKey': job.get('jobkey'),
                                'company': job.get('company'),
                                'maxSalary': job.get('extractedSalary')['max'] if job.get('extractedSalary') and job.get('extractedSalary')['max'] > 0 else 0,
                                'minSalary': job.get('extractedSalary')['min'] if job.get('extractedSalary') and job.get('extractedSalary')['min'] > 0 else 0,
                                'salaryType': job.get('extractedSalary')['type'] if job.get('extractedSalary') is not None else 'none',
                                'pubDate': job.get('pubDate'),
                                'jobTitle': job.get('title'),
                                'jobLocationCity': job.get('jobLocationCity'),
                                'jobLocationPostal': job.get('jobLocationPostal'),
                                'jobLocationState': job.get('jobLocationState')
                               })

  def parse_job(self, response):
    script_tag = re.findall(r"_initialData=(\{.+?\});", response.text)
    if script_tag:
      job_info = {}
      json_blob = json.loads(script_tag[0])
      job = json_blob["jobInfoWrapperModel"]["jobInfoModel"]
      job_info['source'] = 'indeed'
      job_info['job_key'] = response.meta['jobKey']
      job_info['url'] = response.url
      job_info['salary'] = {
        "max":response.meta['maxSalary'],
        "min":response.meta['minSalary'],
        "type":response.meta['salaryType']
      }
      job_info['title'] = response.meta['jobTitle']
      job_info['place'] = response.meta['jobLocationCity']
      job_info['place_postal'] = response.meta['jobLocationPostal']
      job_info['place_full'] = job['jobInfoHeaderModel']['formattedLocation']
      job_info['recruiter'] = {
        'name':response.meta['company']
      }
      job_info['benefits'] = response.xpath('//div[@class="css-1oelwk6 eu4oa1w0"]/div[@class="css-k3ey05 eu4oa1w0"]//li/text()').getall()
      job_info['description'] = clean_text(job.get('sanitizedJobDescription',''))
      job_info['hours'] = {
        "type":job['jobMetadataHeaderModel']['jobType']
      }

      timestamp_ms = response.meta['pubDate']

      # Convert to seconds by dividing by 1000
      timestamp_s = timestamp_ms / 1000
      
      # Define the Amsterdam timezone
      amsterdam_tz = pytz.timezone('Europe/Amsterdam')

      # Convert timestamp to datetime in Amsterdam timezone
      dt = datetime.fromtimestamp(timestamp_s, tz=pytz.utc).astimezone(amsterdam_tz)

      job_info['dateRefreshed'] = dt.isoformat()

      yield job_info
