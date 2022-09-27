import json
import requests
import datetime
import os

def get_info_by_rubric(name):

    subrubrics_list = []

    if not os.path.exists(f'data'):
        os.mkdir(f'data')
    
    if not os.path.exists(f'data/rubric_{name}'):
        os.mkdir(f'data/rubric_{name}')
    
    path_file = f'data/rubric_{name}/'

    url=f'https://api.lenta.ru/v3/topics/by_rubrics?rubric[]={name}'

    try:
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
            rubric = headline.get('rubrics').get('main_rubric')['slug']
            try:
                subrubric = headline.get('rubrics').get('subrubrics')[0].get('slug')
            except:
                subrubric = ''
            tags = [tag.get('slug') for tag in headline.get('tags')]
            info = headline.get('info')
            url = info['id']
            description = info['announce']
            title = info['title']
            modified_at = datetime.datetime.fromtimestamp(info['modified']).strftime("%d-%m-%Y %H-%M")
            topic_type = headline.get('type')
            topic_info = {
                'Author_name': author_name,
                'Author_job': author_job,
                'Author_slug': f'https://api.lenta.ru/parts/authors/{author_slug}',
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


            if subrubric and subrubric not in subrubrics_list:
                subrubrics_list.append(subrubric)
                


            topics_info.append(topic_info)
        
        subrubrics = [{f'{name}': ', '.join(subrubrics_list)}]

        with open(f'{path_file}subrubrics_{name}.json', 'w', encoding='utf-8') as file:
            json.dump(obj=subrubrics, fp=file, ensure_ascii=False, indent=4)  

        with open(f'{path_file}topics_info_{name}.json', 'w', encoding='utf-8') as file:
            json.dump(obj=topics_info, fp=file, ensure_ascii=False, indent=4)        

    except Exception as ex:
        print(ex)
