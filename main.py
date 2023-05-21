import json
import os
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup


def lambda_handler(event, context):
    # Get information from CGV webpage
    html = urlopen("http://www.cgv.co.kr/movies/?lt=1&ft=0")
    bs_object = BeautifulSoup(html, "html.parser", from_encoding="utf-8")

    result = ""

    movie_list = bs_object.find_all("div", "box-contents")
    for index, movie_item in enumerate(movie_list):
        title = movie_item.find("strong", "title").text
        release_date = movie_item.find("span", "txt-info").find("strong").contents[0].get_text(strip=True)
        result += (str(index + 1) + ". " + title + " " + release_date + "\n")

    # Send to telegram
    bot_token = os.environ.get('TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + chat_id + \
                '&parse_mode=HTML&text=' + result
    response = requests.get(send_text)
    print(response)
    return {
        'statusCode': 200,
        'body': json.dumps("ok")
    }


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    lambda_handler(None, None)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
