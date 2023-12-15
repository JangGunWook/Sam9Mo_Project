import json

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import nltk
nltk.download('punkt')

from pydantic import BaseModel

from multiprocessing import Process

import pymongo

model_dir = "gogamza/kobart-summarization"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
model = AutoModelForSeq2SeqLM.from_pretrained(model_dir)

class DataInput(BaseModel):
    inputText: str
class SummaryOut(BaseModel):
    summary: str

# mongodb 연결
client = pymongo.MongoClient('mongodb://sam9:sam9mo!!@59.3.28.12:27017/')
db = client["sam9mo"]
collection = db["news"]

def summary_content_process(Text_data):
    print("기사 요약중....")
    returnSummary: SummaryOut = None
    try:
        # print("Text_data\n", Text_data)
        text =  Text_data

        raw_input_ids = tokenizer.encode(text)
        input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

        summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=4000,  eos_token_id=1)
        predicted_title = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
        
        returnSummary: SummaryOut = predicted_title
    except Exception as e:
        returnSummary: SummaryOut = str(e)
        print(f'Local Summary EXCEPTION => {e}')
    print("기사 요약완료!!")
        
    return returnSummary

PROCESS_COUNT = 1

# offsetValue_save.txt에서 마지막 실행 offset변수 불러오기
def local_content_summary(p_index):
    
    find_wrong_collection_query = {"content_summary" : {"$regex" : "object"}}
    wrong_collection_list = list(collection.find(find_wrong_collection_query))
    
    for i in range(p_index, len(wrong_collection_list), PROCESS_COUNT):
        print("process : ", p_index)
        
        find_id_query = {"_id" : wrong_collection_list[i]['_id']}
        
        # try:
        #     if collection.find_one({"_id" : message.value['_id'], "news_content" : {"$exists" : True}}) != None:
        #         print("이미 뉴스 본문이 저장돼 있음")
        #         save_offset(partition, message.offset)
        #         continue
        # except Exception as ex:
        #     save_offset(partition, message.offset)
        #     print("뉴스 본문 조회하는데 문제")
        
        Text_data = wrong_collection_list[i]['news_content']

        content_summary = summary_content_process(Text_data)
        content_summary = ' '.join(content_summary.split())
        
        try:
            collection.update_one(find_id_query, {"$set" : {"content_summary" : content_summary}}, upsert=False)
            print("뉴스 기사 요약 내용 저장 완료")
        except Exception as ex:
            print("뉴스 기사 요약 내용 삽입하는데 문제")
            
def start_summary(process):
    summary_process = Process(target=local_content_summary, args=(process,))
    summary_process.start()
    return summary_process        

if __name__ == "__main__":
    
    processes = []
    
    # for partition in partitions:
    #     processes.append(start_summary(partition))
    
    for p_index in range(PROCESS_COUNT):
        processes.append(start_summary(p_index))
    
    # Wait for all processes to finish
    for process in processes:
        process.join()            
    
# producer가 실행될 때 topic consume
# asyncio.run(consumer_process())
