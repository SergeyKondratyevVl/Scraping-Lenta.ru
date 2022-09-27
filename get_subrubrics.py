import json
from get_rubrics import get_info_by_rubric
    
# with open('full_rubrics.json', 'w', encoding='utf-8',) as file:
#     json.dump(obj=dict_rubrics, fp=file, ensure_ascii=False, indent=4)

def get_subrubrics():

    with open('rubrics.txt') as file:
        rubrics = file.read().split(', ')

    dict_rubrics = {}

    for rubric in rubrics:

        with open(f'data/rubric_{rubric}/subrubrics_{rubric}.json', encoding='utf-8') as file:
            subrubrics = json.load(file)[0].get(rubric).split(', ')
            dict_rubrics[rubric] = subrubrics
        
        for subrubric in subrubrics:
            name = f'{rubric}&rubric[]={subrubric}'
            get_info_by_rubric(name=name)