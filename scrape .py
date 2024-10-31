import requests
from bs4 import BeautifulSoup
import webbrowser
import click

def fetch_hacker_news_pages():
    res = requests.get('https://news.ycombinator.com/news')
    res2 = requests.get('https://news.ycombinator.com/news?p=2')
    if res.status_code != 200 or res2.status_code != 200:
        raise RuntimeError(f'Error fetching Hacker News pages: {res.status_code}, {res2.status_code}')
    return res.text, res2.text

# Parse the HTML 
def parse_hacker_news_pages(page_1_html, page_2_html):
    soup = BeautifulSoup(page_1_html, 'html.parser')
    soup2 = BeautifulSoup(page_2_html, 'html.parser')

    links = soup.select('.titleline > a')
    subtext = soup.select('.subtext')
    links2 = soup2.select('.titleline > a')
    subtext2 = soup2.select('.subtext')

    mega_links = links + links2
    mega_subtext = subtext + subtext2

    return mega_links, mega_subtext

def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)

# Print top 3 Hacker News stories
def print_top_hn_stories(hn_stories):
    top_stories = hn_stories[:3]
    for story in top_stories:
        print(f"{story['title']} ({story['votes']} points)")
        print(f"Link: {story['link']}")
        print("-")
        
        if click.confirm(f"Do you want to open '{story['title']}' in your browser?", default=False):
            webbrowser.open(story['link'])

if __name__ == '__main__':
        page_1_html, page_2_html = fetch_hacker_news_pages()
        links, subtext = parse_hacker_news_pages(page_1_html, page_2_html)
        top_stories = create_custom_hn(links, subtext)
        print_top_hn_stories(top_stories)
