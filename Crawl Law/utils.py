
import requests
from bs4 import BeautifulSoup
import json
import os
from glob import glob
from tqdm import tqdm
import re

MAP_LAW = {
    'muc': 'Mục',
    'dieu': 'Điều',
    'chuong_pl': 'Chương Phụ Lục'
}


with open('/mnt/tuannb/Crawl_data/list_answer.txt', 'r') as output:
    list_word_answer = output.read().split('\n')

with open('/mnt/tuannb/Crawl_data/list_pps.txt', 'r') as output:
    list_word_pps = output.read().split('\n')

with open('/mnt/tuannb/Crawl_data/list_image.txt', 'r') as output:
    list_word_image = output.read().split('\n')

with open('/mnt/tuannb/Crawl_data/Remove/remove_answer.txt', 'r') as output:
    list_remove_answer = output.read().split('\n')

with open('/mnt/tuannb/Crawl_data/remove_data.txt', 'r') as output:
    list_remove_data = output.read().split('\n')

def get_link_crawl(name_domain, start_page, end_page, path_folder):
    # print('huhi')
    suffer = '?page='
    for i in tqdm(range(start_page, end_page)):
        present_domain = name_domain + suffer + str(i+1)
        # print(present_domain)
        list_data = open(path_folder  + '/' + get_name_folder(name_domain) + '/link_from_page_' + str(start_page) + '_to_' + str(end_page) + '.txt', 'a')

        try:
            r = requests.get(present_domain)
            soup = BeautifulSoup(r.content)
            table = soup.find('section').find_all('article')
            for item in table:
                list_data.write(item.find('a').get('href') + '\n')
        except:
            continue
        # print(table)
            
            
def get_name_folder(name_domain):
    list_character = name_domain.split('/')[-1].removesuffix('\n').split('-')
    b = str()
    for i in range(len(list_character)):
        if i != len(list_character) - 1:
            b += list_character[i] + ' '
        else:
            b += list_character[i]
    return b


def create_folder(list_domain):
    for domain in list_domain:
        last_name = domain.split('/')[-1].replace('-' , ' ')
        print(last_name)
        os.mkdir('/mnt/tuannb/Crawl_data/Name_domain/' + last_name)
    pass
        
    

def get_all(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table = soup.find('body').find('div', attrs={'class' : 'tvpl-main container pt-3 pb-3 wap-page-detail'})
        return table
    pass

def get_categories(table):
    list_categires = table.find_all('div', attrs={'class' : 'row'})[1].find('div', attrs={'class' : "col-md-9"}) \
                          .find('article').find('div', attrs={'class' : 'row'}) \
                          .find('section', attrs={'class' : 'col-md-3'}) \
                          .find_all('section', attrs={'class' : 'news-box-keyword mb-3'}) 
    list_cate = []
    for item in list_categires:
        list_cate.append(item.find('header', attrs={'class' : 'fs-6 fw-bold p-2 m-0'}).find('a').text)
    return list_cate

def get_table(table):
    return table.find_all('div', attrs={'class' : 'row'})[1].find('div', attrs={'class' : "col-md-9"}) \
                .find('article').find('div', attrs={'class' : 'row'}) \
                .find('div', attrs={'class' : 'col-md-9'}).find('section', attrs={'class' : 'news-content'})

def get_title(table):
    return table.find_all('div', attrs={'class' : 'row'})[1].find('div', attrs={'class' : "col-md-9"}) \
                .find('article').find('div', attrs={'class' : 'row'}) \
                .find('div', attrs={'class' : 'col-md-9'}).find('header').find('h1', attrs={'class' : 'h3 fw-bold title'}).text
                

def check_pps(texts):
    for item in list_word_pps:
        if item in texts:
            return True
    return False   

def check_answer(texts):
    for item in list_word_answer:
        if item in texts:
            return True
    return False

def check_image(texts):
    for item in list_word_image:
        if item in texts:
            return True
    return False

def get_sample(url):
    flag = False
    all = get_all(url)
    table = get_table(all)
    question, context, answer, reference = [], [], [], []
    num_valid = 1
    datas = {
        'url': url,
        'category': get_categories(all),
        'title': get_title(all),
        'samples': [],
    }
    
    # Format khong co nhieu cau hoi
    if len(table.find_all(['h2'])) > 0:
        for item in table.find_all(['h2', 'p', 'blockquote']):
            if check_image(item.text):
                continue
            
            if item.find('a'):
                reference.append(item.find('a').get('href'))
            
            if item.name == 'h2':
                if len(question) == 0:
                    question.append(item.text)
                    num_valid = 1
                elif context != '':
                    datas['samples'].append({
                        'question': question,
                        'context': context,
                        'answer': answer,
                        'reference': reference,
                    })
                    num_valid = 1
                    question, context, answer, reference = [], [], [], []
                    # question = []
                    question.append(item.text)
                    
            elif check_answer(item.text):
                # print(item.text)
                answer.append(item.text)
                num_valid = 2
        
            elif check_pps(item.text):
                # print(item.text)
                if num_valid == 2:
                    answer.append(item.text)
                else:
                    context.append(item.text)

            else:
                if num_valid == 1:
                    context.append(item.text)
                else:
                    answer.append(item.text)  
            

        datas['samples'].append({
            'question': question,
            'context': context,
            'answer': answer,
            'reference': reference,
        })
        
    else:
        flag = True
        data = table.find_all(['strong', 'p'])
        for idx in range(0, len(data)):
            
            if data[idx].find('a'):
                reference.append(data[idx].find('a').get('href'))
                
            if idx > 0 and data[idx-1].name == 'strong':
                # print(data[idx])
                context.append(data[idx])
                continue
            
            if check_image(data[idx].text):
                continue
            
            if data[idx].name == 'strong' and '?' in data[idx].text:
                # print(data[idx].text)
                if len(question) == 0:
                    question = []
                    question.append(data[idx])
                    num_valid = 1
                    
                elif context != '':
                    datas['samples'].append({
                        'question': question,
                        'context': context,
                        'answer': answer,
                        'reference': reference,
                    })
                    num_valid = 1
                    question, context, answer = [], [], []
                    
            elif check_answer(data[idx].text):
                # print(data[idx].text)
                answer.append(data[idx])
                num_valid = 2
        
            elif check_pps(data[idx].text):
                # print(item.text)
                if num_valid == 2:
                    answer.append(data[idx])
                else:
                    context.append(data[idx])

            else:
                if num_valid == 1:
                    context.append(data[idx])
                else:
                    answer.append(data[idx])  
                    
        # print(question)
        datas['samples'].append({
            'question': question,
            'context': context,
            'answer': answer,
            'reference': reference,
        })
    return datas, flag

def replace_tokens(text):
    return text.replace('\n' ,' ').replace('\xa0' ,' ').replace('\r' ,' ').strip()

def normalize(data):
    new_data = []
    for item in data:
        new_data.append(replace_tokens(item))
    return new_data

def remove_duplicate_strong_tags(html_list, type='context'):
    seen_contents = []
    for item in html_list[type]:
        content = item.text
        if content == '':
            continue
        flag = False
        for itm in seen_contents:
            if content == itm:
                flag = True
                break
        if flag == False:
            seen_contents.append(content) 
        
    if len(seen_contents) > 0:
        return seen_contents
    else:
        return []


def get_last_output(data, remove_tag=False):
    new_data = {
        'url': data['url'],
        'category': data['category'],
        'title': data['title'],
        'QA': [],
    }
    if remove_tag == True:
        for item in data['samples']:
            question = remove_duplicate_strong_tags(item, 'question')
            answer = remove_duplicate_strong_tags(item, 'answer')
            context = remove_duplicate_strong_tags(item, 'context')
            new_data['QA'].append({
                'question': normalize(question),
                'context': normalize(context),
                'answer': normalize(answer),
                'reference': item['reference']
            })
    else:
        for item in data['samples']:
            new_data['QA'].append({
                'question': normalize(item['question']),
                'context': normalize(item['context']),
                'answer': normalize(item['answer']),
                'reference': item['reference']
            })
    return new_data



def normalize_text(text):
    return re.sub(r'\s+', ' ', text)

def get_infor_vbpl(url):
    num_dieu = url.split('?')[-1]
    text_dieu = ''
    for item in MAP_LAW.keys():
        if item in num_dieu:
            text_dieu = MAP_LAW[item]
    for item in num_dieu.split('_'):
        if item.isdigit():
            text_dieu += (' ' + item + ',')
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        table_all = soup.find('body').find('form', attrs={'id' : 'form1'}) \
                    .find('table', attrs={'id' : 'tblcontainer'}) \
                    .find_all('div', attrs={'class' : 'cldivContentDocVn'})[0] \
                    .find('div', attrs={'class' : 'content1'}) \
                    .find('div').find('div')
                    
        table_numlaw = table_all.find('table').find_all('tr')[1].find_all('td')
        
        table_namelaw = table_all.find_all('p')[5].find('a').text + ' : ' + table_all.find_all('p')[6].find('a').text
        
        # return table_namelaw
        text_numlaw = ''
        for itm in table_numlaw[1].find('p').find_all('i'):
            text_numlaw += itm.text

        return {
            'link': url,
            'Number Law': normalize_text(table_numlaw[0].find('p').text),
            'Time create': normalize_text(text_numlaw),
            'Dieu': normalize_text(text_dieu.removesuffix(',')),
            'Name Law': normalize_text(table_namelaw),
        }
    return False

def remove_answer(text):
    for item in list_remove_answer:
        if item in text:
            text = text.replace(item, '').strip(',. !')
    return text

def remove_image(text):
    for item in list_word_image:
        if item in text:
            return True
    return False

def get_text(data, type):
    contexts = ''
    for context in data[type]:
        if context != '' and context != '...' and remove_image(context) == False:
            contexts += '\n' + context 
    return contexts

def bool_remove(questions, contexts, answers):
    if len(contexts.split(' ')) < len(answers.split(' ')):
        return False
    if len(questions.split(' ')) > len(answers.split(' ')):
        return False
    for item in list_remove_data:
        if item in answers:
            return False
    return True

def get_data_process_and_combine(x):
    cc = 0
    leng = 0
    new_data = []
    for data in x:
        QA_data = []
        questions, contexts, answers = '', '', ''
        
        for sample in data[0]['samples']:
            cc += 1
            if len(sample['context']) != 0 and len(sample['answer']) != 0:
                questions, contexts, answers = get_text(sample, type='question'), get_text(sample, type='context'), remove_answer(get_text(sample, type='answer')) 
                
                if bool_remove(questions=questions, contexts=contexts, answers=answers) == True:
                    QA_data.append({
                        'question': questions,
                        'context': contexts,
                        'answer': answers,
                        'reference': sample['reference']
                    })
        total_contexts = ''
        for sample in data[0]['samples']:
            total_contexts +=' ' + get_text(sample, type='context')
            
        if len(total_contexts.split(' ')) < 950:
            for sample in data[0]['samples']:
                for idx in range(len(QA_data)-7 if len(QA_data) - 7 > 0 else 0, len(QA_data)):
                    if sample['reference'] == QA_data[idx]['reference']:
                        QA_data[idx]['context'] = total_contexts
                        
        if len(QA_data) != 0:
            new_data.append({
                'url': data[0]['url'],
                'title': data[0]['title'],
                'category': data[0]['category'],
                'samples': QA_data,
            })
    for item in new_data:
        leng += len(item['samples'])
    print('First Data: ' + str(cc))
    print('Fix Data: ' + str(leng))
    
    return new_data, leng
