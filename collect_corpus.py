import requests, re
from bs4 import BeautifulSoup
from IPython.display import HTML, display

home = "http://inza-vpered.ru/article/"
categ = "http://inza-vpered.ru/article/?category="

# cant collect all categories from main page automatically
categories = ['obschestvo', 'smi', 'obrazovanie', 'sotsialnoe-partnerstvo',
              'pravo-i-zakon', 'zhkh', 'kultura', 'sport', 'politika',
              'selskoe-hozyajstvo', 'ekonomika', 'meditsina',
              'proisshestviya', 'investitsii', 'stroitelstvo',
              'promyishlennost', 'transport', 'ekologiya',
              'malyij-i-srednij-biznes', 'nauka', 'informatsionnyie-tehnologii',
              'trud-i-zanyatost', 'turizm', 'kosmos']

text_links = []

def get_links(soup, page_track):
    page_track = page_track
    next_page_match = 0
    np_link = ''
    
    for tag in soup.findAll('a'):
        link = tag['href']
        match = re.search('/article/[0-9]', link)
        if match:
            print(link)
            
            if link not in text_links:
                text_links.append(link)
                
        # check for next page
        match2 = re.search('page=' + str(page_track + 1), link)
        if match2:
            print('next page:')
            print(link)
            
            np_link = 'http://inza-vpered.ru' + link
            next_page_match += 1
            page_track += 1

    # repeat search for next page            
    if next_page_match > 0:
        print(np_link)
        print(page_track)
        req1 = requests.get(np_link)
        soup1 = BeautifulSoup(req1.text, 'lxml')
        
        get_links(soup1, page_track)

for category in categories:
    req = requests.get('http://inza-vpered.ru/article/?category=' + category)
    soup = BeautifulSoup(req.text, 'lxml')
    page_track = 1
    
    get_links(soup, page_track)
    print('\n')
    print('category ' + category + ' done')
    print('\n')

print(len(text_links))

f = open('text_links.txt', 'w')
for link in text_links:
    f.write(link)
    f.write('\n')
f.close()

def link_to_text(link):
    
    test_page = 'http://inza-vpered.ru' + link
    req = requests.get(test_page)
    soup = BeautifulSoup(req.text, 'lxml')
    
    file_name = re.search('/([0-9]+)/', test_page)
    file_name = file_name[0]
    while '/' in file_name:
        file_name = re.sub('/', '', file_name)

    # author:     <span class="b-object__detail__author__name"> ...
    for tag in soup.findAll('span'):
        if tag.has_attr('class'):
            if tag['class'] == ['b-object__detail__author__name']:
                author = '@au ' + tag.contents[0]

    # date:     <span class="date">
            if tag['class'] == ['date']:
                if not any(c.isalpha() for c in tag.contents[0]):
                    date = '@da ' + tag.contents[0]

    # title:     <meta name="title" content="..."/>
    for tag in soup.findAll('meta'):
        if tag.has_attr('name'):
            if tag['name'] == 'title':
                title = '@ti ' + tag['content']

    # topic:     <a href="/article/?category=obrazovanie" rel="nofollow"> ...
    topics = []
    for tag in soup.findAll('a'):
        if tag.has_attr('href'):
            if tag['href'].startswith('/article/?category='):
                topics.append(tag.contents[0])

        topic = '@topic ' + ', '.join(topics)

    # url
    url = '@url ' + test_page

    # text:     <div class="b-block-text__text"> ...
    all_text = ''
    for tag in soup.findAll('div'):
        if tag.has_attr('class'):
            
            # decription first:     <div class="b-object__detail__annotation">
            if tag['class'] == ['b-object__detail__annotation']:
                all_text += tag.text
            
            if tag['class'] == ['b-block-text__text']:                
                all_text += ' ' + tag.text
                
    while '\n' in all_text:
        all_text = re.sub('\n', ' ', all_text)
    while '  ' in all_text:
        all_text = re.sub('  ', ' ', all_text)
        
    save_dir = '/Users/Sofia/Desktop/inza-vpered'
    f1 = open('/Users/Sofia/Desktop/inza-vpered/' + file_name + '.txt', 'w')
    
    try:
        author
    except NameError:
        author = '@au N/A'
    
    info = [author, title, date, topic, url, all_text]
    for i in info:
        f1.write(i)
        f1.write('\n')

    f1.close()
    
links = open('/Users/Sofia/Desktop/text_links.txt', 'r') # machine-specific
lines = links.read().splitlines()

i = 0
for line in lines:
    print(i)
    link_to_text(line)
    i += 1

