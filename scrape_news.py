from bs4 import BeautifulSoup
import requests, csv

news_source = requests.get('https://news.bitcoin.com/').text

news = BeautifulSoup(news_source, 'lxml')

csv_file = open('news_scrape.csv', 'w')

csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Headline', 'Summary', 'Tags', 'Link', 'Featured_image'])

for article in news.find_all('div', class_='story'):
    link = article.find('a').get('href')
    headline = article.find(class_='story__title').text.strip()

    try:
        featured_image = article.find('img', class_='story__img').get('src')
    except Exception as e:
        featured_image = None

    source = requests.get(link).text
    story = BeautifulSoup(source, 'lxml')
    summary = story.find('article').find('p').text

    tags_block = story.find('div', class_="article__body__tags")
    tags = ''
    for tag in tags_block.find_all('a'):
        tags += tag.text + ', '

    csv_writer.writerow([headline, summary, tags, link, featured_image])

    print(summary)
print('Done!')
csv_file.close()