from utils import *
from glob import glob
from tqdm import tqdm
import os
import json


# path_file = glob('/mnt/ngoclt/Crawl_data/Split Phap Luat/*/data_domain.json')

# # for idx in range(0, 9):
# with open('/mnt/ngoclt/Crawl_data/Split Phap Luat/dau tu/data_domain.json', 'r') as f:
#     data = json.load(f)

# new_data = []
# for item in tqdm(data[15:25]):
#     samples = []

#     for sample in item[0]['samples']:
#         refer = []
#         for xxx in sample['reference']:
#             print(xxx)
#             if '?anchor=' in xxx:
#                 try:
#                     refer.append(get_infor_vbpl(xxx))
#                 except:
#                     'Nhu db'
#                     continue
        
#             samples.append({
#                 'question': sample['question'],
#                 'context': sample['context'],
#                 'answer': sample['answer'],
#                 'reference': refer
#             })
    
#     new_data.append({
#         'url': item[0]['url'],
#         'category': item[0]['category'],
#         'title': item[0]['title'],
#         'reference': samples,
#     })

# with open('/mnt/ngoclt/Crawl_data/Split Phap Luat/dau tu/data_domain_v2.json', 'w', encoding='utf-8') as f:
#     json.dump(new_data, f, ensure_ascii=False)





from tqdm import tqdm

new_data = []
train = json.load(open('/mnt/ngoclt/Data/Data_Law/test_pseudo.json', 'r'))



for item in tqdm(train):
    try:
        new_data.append({
            'question': item['question'],
            'context': item['context'],
            'answer': item['answer'],
            'reference': [get_infor_vbpl(itm) for itm in item['reference']]

        })    
        # json.dump(new_data, open('/mnt/ngoclt/Data/Data_Law/have_refer.json', 'w', encoding='utf-8'), ensure_ascii=False)
    except:
        continue
    

    
json.dump(new_data, open('/mnt/ngoclt/Data/Data_Law/have_refer.json', 'w', encoding='utf-8'), ensure_ascii=False)
























# list_folder = glob('/mnt/ngoclt/Crawl_data/Name_domain/*')


# for idx in range(0, 43):
#     list_data = []
#     name_folder = list_folder[idx].split('\n')[-1]
    
#     if os.path.exists(list_folder[idx] + '/link_from_page_101_to_200.txt'):
#         with open(list_folder[idx] + '/link_from_page_101_to_200.txt', 'r') as f:    
#             list_link = f.read().split('\n')
#         if len(list_link) == 1:
#             continue
        
#         # In ra số lượng link trong mỗi file
#         print(list_folder[idx].split('\n')[-1] + ': ' + str(len(list_link)))
#         counts = 0
        
        
#         for i in tqdm(range(0, len(list_link))):
#             try:
#                 url = get_all(list_link[i])
#             except:
#                 continue
            
#             try:
#                 category = get_categories(url)
#             except:
#                 category = []
            
#             try:
#                 raw_data, flag = get_sample(list_link[i], category)
#                 list_data.append(get_last_output(raw_data, flag))
#                 # print(raw_data)
#             except:
#                 continue
            
#     with open(list_folder[idx] + '/data_from_101_to_200_v2.json', 'w', encoding='utf-8') as f:
#         json.dump(list_data, f, ensure_ascii=False)
#     print(list_folder[idx].split('\n')[-1] + ': ' + str(len(list_data)))