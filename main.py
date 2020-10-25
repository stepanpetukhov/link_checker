import requests
import re
import csv
import time
import logging

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w")
logging.info("Program started at {0}".format(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())))

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0', 'accept': '*/*'}
FILE = 'back_links.csv'
OLD_HOST = 'money.yandex.ru'
NEW_HOST = 'yoomoney.ru'

def get_html(url, params=None):
    try:
        result = requests.get(url, headers=HEADERS, params=params)
        if result.status_code == 200:
            return result.text
        else:
            print('Bad HTTP Code')
            logging.error("request to {0} have bad HTTP Code".format(url))
            time.sleep(5)
            return False
    except(requests.RequestException, ValueError):
        print('RequestException')
        logging.error("request to {0} have RequestException".format(url))
        time.sleep(5)
        return False


def csv_writer(data, path, firstLine):
    """
    Write data to a CSV file path
    """
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(firstLine)
        for line in data:
            writer.writerow(line)


result = []
with open(FILE, 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for line in reader:
        donor = line.get('donor')
        acceptor = line.get('acceptor')
        print(donor)
        html = get_html(donor)
        if html:
            oldHostEntry = re.findall(r'<a.*href.*{0}.*>.*</a>'.format(OLD_HOST), html, flags=re.IGNORECASE)
            newHostEntry = re.findall(r'<a.*href.*{0}.*>.*</a>'.format(NEW_HOST), html, flags=re.IGNORECASE)
            oldHostAcceptorEntry = re.findall(r'<a.*href.*{0}.*>.*</a>'.format(acceptor), html, flags=re.IGNORECASE)
            newHostAcceptor = re.sub(r'money.yandex.ru', 'yoomoney.ru', acceptor)
            newHostAcceptorEntry = re.findall(r'<a.*href.*{0}.*>.*</a>'.format(newHostAcceptor), html, flags=re.IGNORECASE)


            oldHostEntryCount = len(oldHostEntry)
            newHostEntryCount = len(newHostEntry)
            oldHostAcceptorEntryCount = len(oldHostAcceptorEntry)
            newHostAcceptorEntryCount = len(newHostAcceptorEntry)
            print('oldHostAcceptorCount = {0}, oldHostCount = {1}, newHostAcceptorCount = {2}, newHostCount = {3}\n'
                  .format(oldHostAcceptorEntryCount, oldHostEntryCount, newHostAcceptorEntryCount, newHostEntryCount))
            result.append([donor, 'OK', acceptor, oldHostAcceptorEntryCount, oldHostEntryCount,
                           newHostAcceptorEntryCount, newHostEntryCount])
        else:
            result.append([donor, 'Fail', acceptor])


csv_writer(result, 'result.csv', ['donor', 'donorHttpStatus', 'acceptor', 'oldHostAcceptorEntryCount',
                                  'oldHostEntryCount', 'newHostAcceptorEntryCount', 'newHostEntryCount'])

logging.info("Program finished at {0}".format(time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())))
