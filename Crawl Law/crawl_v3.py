from utils import *
from glob import glob
from tqdm import tqdm
import os
import json

# list_folder = json.load(open('/mnt/ngoclt/Crawl_data/total.json', 'r'))

# def get_link_crawl_v2(name_domain, start_page, end_page, path_folder):
#     # print('huhi')
#     suffer = '?page='
#     for i in tqdm(range(start_page, end_page)):
#         present_domain = name_domain + suffer + str(i+1)
#         # print(present_domain)
#         list_data = open(path_folder + '/link_from_page_' + str(start_page) + '_to_' + str(end_page) + '.txt', 'a')

#         try:
#             r = requests.get(present_domain)
#             soup = BeautifulSoup(r.content)
#             table = soup.find('section').find_all('article', attrs={'class' : 'news-card'})
            
#             for item in table:
#                 try:
#                     list_data.write('https://thuvienphapluat.vn' + item.find('a').get('href') + '\n')
#                 except:
#                     continue
#         except:
#             continue
        
        
# for item in range(18, 27):
#     get_link_crawl_v2(name_domain=list_folder[item]['link'], start_page=0, end_page=int(list_folder[item]['max_page']), path_folder=list_folder[item]['folder'])





list_folder =     {
        "link": "https://thuvienphapluat.vn/phap-luat/phap-luat/dich-vu-phap-ly",
        "max_page": "71",
        "folder": "/mnt/ngoclt/Crawl_data/Split Phap Luat/xuat nhap khau"
}

# for item in range(11, 22):
list_link_domain = glob(list_folder['folder'] + '/*.txt')[0]

with open(list_link_domain, 'r') as f:
    list_link = f.read().split('\n')

data = []
for idx in tqdm(range(1000)):
    try:
        sample = get_sample(list_link[idx])
        data.append(sample)
    except:
        continue
    
with open(list_folder['folder'] + '/data_domain.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
        




































# list_folder = glob('/mnt/ngoclt/Crawl_data/Name_domain/*')


# for idx in range(0, 43):
#     list_data = []
#     name_folder = list_folder[idx].split('\n')[-1]
    
#     if os.path.exists(list_folder[idx] + '/link_from_page_201_to_300.txt'):
#         with open(list_folder[idx] + '/link_from_page_201_to_300.txt', 'r') as f:    
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

#     with open(list_folder[idx] + '/data_from_201_to_300_v2.json', 'w', encoding='utf-8') as f:
#         json.dump(list_data, f, ensure_ascii=False)
#     print(list_folder[idx].split('\n')[-1] + ': ' + str(len(list_data)))