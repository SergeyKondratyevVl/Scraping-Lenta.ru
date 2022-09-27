import requests
import json

with open('rubrics.txt') as file:
    rubrics = file.read().split(', ')

count_rubrics = []

all_topics = 0

for rubric in rubrics:
    url = f'https://api.lenta.ru/v4-alfa/topics/by_rubrics?rubric[]={rubric}'

    resp = requests.get(url).json()

    total_count = resp.get('metadata').get('total_count')
    count_rubric = {rubric: total_count}
    count_rubrics.append(count_rubric)
    all_topics += total_count

count_rubrics.append({
    'all_topics': all_topics
})

with open('count_rubrics.json', 'w', encoding='utf-8',) as file:
    json.dump(obj=count_rubrics, fp=file, ensure_ascii=False, indent=4)
