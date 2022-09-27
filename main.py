import json
import requests
import datetime
from get_rubrics import get_info_by_rubric
import os

from get_subrubrics import get_subrubrics

rubrics = []
tags_list = []
authors = []
authors_list = []

def get_info(name):

    if not os.path.exists(f'data'):
        os.mkdir(f'data')
    
    if not os.path.exists(f'data/category_{name}'):
        os.mkdir(f'data/category_{name}')
    
    path_file = f'data/category_{name}/'

    url=f'https://api.lenta.ru/v4-alfa/topics/by_list?slug={name}'
    
    # try:
    resp = requests.get(url=url).json()
    topics = resp['topics']
    with open(f'{path_file}info_{name}.json', 'w', encoding='utf-8') as file:
        json.dump(obj=topics, fp=file, ensure_ascii=False, indent=4)
    topics_info = []
    for topic in topics:
        headline = topic['headline']
        try:
            author_name = headline.get('authors')[0].get('name')
            author_job = headline.get('authors')[0].get('job')
            author_slug = headline.get('authors')[0].get('slug')
        except:
            author_job = ''
            author_name = ''
            author_slug = ''
        link = headline.get('links').get('public')
        rubric = headline.get('rubrics').get('main_rubric').get('slug')
        try:
            subrubric = headline.get('rubrics').get('subrubrics')[0].get('slug')
        except:
            subrubric = ''
        tags = [tag.get('slug') for tag in headline.get('tags')]
        info = headline.get('info')
        url = info['id']
        description = info['announce']
        title = info['title']
        modified_at = datetime.datetime.fromtimestamp(info['modified_at']).strftime("%d-%m-%Y %H-%M")
        topic_type = headline.get('type')
        topic_info = {
            'Author_name': author_name,
            'Author_job': author_job,
            'Author_url': f'https://api.lenta.ru/parts/authors/{author_slug}',
            'Link': link,
            'Rubric': rubric,
            'Subrubric': subrubric,
            'Tags': ', '.join(tags),
            'URL': url,
            'Description': description,
            'Title': title,
            'Modified_at': modified_at,
            'Type': topic_type
        }
        if author_name and author_name not in authors:
            authors.append(author_name)
            authors_list.append({
                'Author_name': author_name,
                'Author_job': author_job,
                'Author_url': f'https://api.lenta.ru/parts/authors/{author_slug}'
            })
        if rubric and rubric not in rubrics:
            rubrics.append(rubric)

        [tags_list.append(tag) for tag in tags if tag and tag not in tags_list]
        topics_info.append(topic_info)

        with open(f'{path_file}topics_info_{name}.json', 'w', encoding='utf-8') as file:
            json.dump(obj=topics_info, fp=file, ensure_ascii=False, indent=4)        

    # except Exception as ex:
    #     print(ex)

def get_slugs():

    url = 'https://api.lenta.ru/v2/lists'
    list_slugs = requests.get(url).json()
    slugs = []
    for list_slug in list_slugs:
        slug = list_slug['slug']
        slugs.append(slug)
    
    with open('slugs.txt', 'w', encoding='utf-8') as file:
        file.write(', '.join(slugs))

    return slugs

def get_authors():
    print(f'[INFO] {len(authors)} authors')
    with open('authors.json', 'w', encoding='utf-8') as file:
        json.dump(obj=authors_list, fp=file, ensure_ascii=False, indent=4)

def get_rubrics():
    print(f'[INFO] {len(rubrics)} rubrics')
    with open('rubrics.txt', 'w', encoding='utf-8') as file:
        file.write(', '.join(rubrics))

def get_tags():
    print(f'[INFO] {len(tags_list)} tags')
    with open('tags.txt', 'w', encoding='utf-8') as file:
        file.write(', '.join(tags_list))

def main():

    slugs = get_slugs()
    print(slugs)

    for slug in slugs:
        get_info(slug)
    
    print('[INFO] Slug OK!')
    
    get_authors()

    for rubric in rubrics:
        get_info_by_rubric(rubric)
    
    print('[INFO] Rubrics OK!')
    
    get_rubrics()
    
    get_tags()

    # get_subrubrics()
    # print('[INFO] Subrubrics OK!')

if __name__ == '__main__':
    main()
