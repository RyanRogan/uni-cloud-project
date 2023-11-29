import pytest
import proxy_utils as pu

# Setup
urls = pu.load_url_config()

# Constants
FAKE_SERVICE = "fake"
TOTAL_SERVICE = "grade-total"
SAVE_SERVICE = "state-save"

TOTAL_URL = "http://grade-total.example.com/"
GET_RECORD_URL = "http://save.example.com/get/record/"
DELETE_RECORD_URL = "http://save.example.com/delete/record/"
ADD_RECORD_URL = "http://save.example.com/add"

CONFIG_DICT = {
    'grade-total': 'http://grade-total.example.com/', 
    'maxmin': 'http://grade-maxmin.example.com/', 
    'sort': 'http://grade-sort.example.com/', 
    'grade-classifier': 'http://grade-classifier.example.com', 
    'grade-average': 'http://grade-average.example.com/', 
    'grade-review': 'http://grade-review.example.com/', 
    'state-save': {
        'url': 'http://save.example.com', 
        'add': '/add', 
        'get': '/get/record/', 
        'delete': '/delete/record/'
        }
    }


def testUrlConfigShouldBeDictionary():
    url = pu.load_url_config()
    assert type(url) is dict

def testUrlConfigShouldBeCorrect():
    assert urls == CONFIG_DICT

def testShouldReturnCorrectUrlForServiceGradeTotal():
    url = pu.get_url(TOTAL_SERVICE, urls)
    assert url == TOTAL_URL

def testShouldReturnMinusOneWhenServiceIsInvalid():
    url = pu.get_url(FAKE_SERVICE, urls)
    assert url == -1

def testShouldReturnCorrectAddressForGetRecord():
    url = pu.get_url(SAVE_SERVICE, urls)
    url_full = pu.get_saver_url("get", url)
    assert url_full == GET_RECORD_URL
    
def testShouldReturnCorrectAddressForDeleteRecord():
    url = pu.get_url(SAVE_SERVICE, urls)
    url_full = pu.get_saver_url("delete", url)
    assert url_full == DELETE_RECORD_URL
    
def testShouldReturnCorrectAddressForAddRecord():
    url = pu.get_url(SAVE_SERVICE, urls)
    url_full = pu.get_saver_url("add", url)
    assert url_full == ADD_RECORD_URL