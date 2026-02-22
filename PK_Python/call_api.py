import json
import re
import time
import traceback
from collections import defaultdict

import openpyxl.reader.excel
import pandas as pd
import requests
import concurrent.futures
wb = openpyxl.reader.excel.load_workbook("API_Test.xlsx")


def replace_variables(text,environment):
    if not isinstance(text, str):
        return text
    def replacer(match):
        key = match.group(1)
        return str(environment.get(key, match.group(0)))  # Keep original if key is not found
    return re.sub(r"\$(\w+)\$", replacer, text)


def call_service(method,url,data,headers):
    if "POST"==method:
        data = json.loads(data)
        response = requests.post(url, headers=headers, json=data)
        return response
    elif "GET"==method:
        response = requests.get(url, data)
        return response
    elif "PATCH"==method:
        response = requests.patch(url, data)
        return response
    elif "DELETE"==method:
        response = requests.delete(url)
        return response
    elif "PUT"==method:
        response = requests.put(url,data)
        return response


def perform_test(thread_id):
    results = []
    headers = {
        'Content-Type': 'application/json',  # Ensure this header is set correctly
    }
    environment = {}
    for sheet in wb._sheets:
        for row1 in sheet.rows:
            name = (row1[0]).value
            if name=="API_Name": continue
            method = (row1[1]).value
            url = (row1[2]).value
            data = (row1[3]).value
            code = (row1[4]).value
            try:
                data = replace_variables(data,environment)
                # print(method,url,data,code,"\n")
                start_time = time.time()
                if url.startswith("http"):
                    response = call_service(method, url, data, headers)
                end_time = time.time()
                time_taken =end_time- start_time
                results.append([name,time_taken])
                if code: exec(code)
                # print(environment)
            except Exception as e:
                traceback.print_stack(e)
    return results


num_threads = 2
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = {executor.submit(perform_test, i): i for i in range(num_threads)}
    results = defaultdict(list)
    for future in concurrent.futures.as_completed(futures):
        for res in future.result():
            results[res[0]].append(res[1])
    results2 = []
    for api,lst in results.items():
        results2.append([api,sum(lst)/len(lst),max(lst),min(lst)])

    df = pd.DataFrame(results2, columns=["API_Name", "Avg_Time_Taken", "Max_Time_Taken", "Min_Time_Taken"])
    df.to_excel("Test_Results.xlsx", index=False)
    print("Excel file created successfully!")
