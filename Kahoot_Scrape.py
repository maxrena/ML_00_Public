import json
import requests
import urllib3
import re
from lxml import html
from lxml import etree
from bs4 import BeautifulSoup


def kahoot_details_scrape():
    url = 'https://create.kahoot.it/details/disney/0a39590a-cc49-4222-bf28-dd9da230d6bf'
    kahoot_id = url.split('/')[-1]
    # API link
    answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.format(
        kahoot_id=kahoot_id)
    data = requests.get(answers_url).json()

    # chỗ này print ra cho dễ hình dung về cấu trúc file Json
    # print(json.dumps(data, indent=4))

    # print ra câu trả lời đúng thôi
    for question in data['kahoot']['questions']:
        for choice in question['choices']:
            if choice['correct']:
                break
        print('Q: {:<70} A: {} '.format(question['question'].replace(
            '&nbsp;', ' '), choice['answer'].replace('&nbsp;', ' ')))

    # print hết câu trả lời ra
    for question in data['kahoot']['questions']:
        print('Q: {0} \n A: {1}'.format(
            question['question'].replace('&nbsp;', ' '), question['choices']))


def kahoot_pages_scrape_with_link(url_id):
    # API link
    answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.format(
        kahoot_id=url_id)
    data = requests.get(answers_url).json()

    # chỗ này print ra cho dễ hình dung về cấu trúc file Json
    # print(json.dumps(data, indent=4))

    # print ra câu trả lời đúng thôi
    for question in data['kahoot']['questions']:
        for choice in question['choices']:
            if choice['correct']:
                break
        print('Q: {:<70} A: {} '.format(question['question'].replace('&nbsp;', ' '),
                                        choice['answer'].replace('&nbsp;', ' ')))

    # print hết câu trả lời ra
    for question in data['kahoot']['questions']:
        print('Q: {0} \n A: {1}'.format(
            question['question'].replace('&nbsp;', ' '), question['choices']))


def kahoot_pages_scrape():
    pages_url = 'https://create.kahoot.it/pages/0f99068f-a310-4670-86e3-19fd0b05cf85'

    # API link
    top_kahoot_card_url = 'https://create.kahoot.it/rest/brands/0f99068f-a310-4670-86e3-19fd0b05cf85/kahoots/?limit=100'
    id_get_url = 'https://create.kahoot.it/rest/brands/0f99068f-a310-4670-86e3-19fd0b05cf85/data/'
    pages_data = requests.get(top_kahoot_card_url).json()
    topic_id_pages_data = requests.get(id_get_url).json()

    # print(json.dumps(pages_data, indent=4))
    # print thử ra title của tất cả các topic trong page
    # for topic in pages_data['entities']:
    #     print(topic['card']['title'])

    # dùng bs4 để tìm href của tất cả các topic trong pages
    # link đó xong bỏ lên function kahoot_details_scrap() là được
    # pages_soup = BeautifulSoup(requests.get(pages_url).content, 'html.parser')
    # href_elems = pages_soup.findAll('a', attrs={'href': re.compile('^https://')})
    # for href in href_elems:
    #     print(href)
    # with open('kahoot_pages.html', 'w+', encoding='utf-8') as file:
    #     file.writelines(str(pages_soup))
    # PHẦN NÀY LÀ TEST THỬ = BS4, NHƯNG PHÁT HIỆN RA KAHOOT LÀ DYNAMIC PAGE NÊN THÔI DẸP MẸ ĐI!!!

    # cái này là React, ko scrape theo kiểu static được
    # check API, lấy id, xong ghép với name, để tạo thành link form
    # API id link này nằm trong data/
    # print trước ra tất cả link id
    for topic in topic_id_pages_data['channels']:
        for id in topic['kahootIds']:
            # dùng id này kết hợp với phần bên page data API để get link
            # hơi lòng vòng nhưng sure kèo hơn
            # ở trên là phần kahoot_id là từ 1 link đi ra, giờ mình áp dụng luôn
            print(id)
            print('\n')
            kahoot_pages_scrape_with_link(id)

    # link kahoot đều sẽ có dạng này
    # answers_url = 'https://create.kahoot.it/rest/kahoots/{kahoot_id}/card/?includeKahoot=true'.
    # cho nên cái cần làm tìm ra các id, và thế vào
    # cho nên, việc scrape của function này chính là đi tới các pages để scrape ra tất cả các id
    # phần còn lại chỉ là bỏ id vào link form dạng này rồi scrape bằng function kahoot_pages_scrape()


# kahoot_details_scrape()
kahoot_pages_scrape()
