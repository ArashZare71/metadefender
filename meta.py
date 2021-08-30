import hashlib
import requests


# dividing the file in chunks, calculating the hash of the file
def hash_file(file_name):
    block_s = 65536
    h_file = hashlib.md5()
    with open(file_name, 'rb') as file:
        file_block = file.read(block_s)
        while len(file_block) > 0:
            h_file.update(file_block)
            file_block = file.read(block_s)
    return h_file.hexdigest().upper()


# uploading the file
def upload_file(f_name, api):
    url = "https://api.metadefender.com/v4/file/"
    headers = {
         "apikey": api,
         "content-type": "application/octet-stream"
     }
    response = requests.request("POST", url, headers=headers, data=f_name)
    json_response = response.json()
    # handling the error codes
    if response.status_code != 200:
        print("Error: code %s, message %s" % (json_response["error"]["code"], json_response["error"]["messages"]))
        exit(1)
    return json_response["data_id"]


# looking up the results of the analysis by data ID
def analysis_result(dataId, api):
    url = "https://api.metadefender.com/v4/file/"
    url += dataId
    headers = {
        "apikey": api
    }
    response = requests.request("GET", url, headers=headers)
    json_response = response.json()
    # handling error messages
    if response.status_code != 200:
        print("Error: code %s, message %s" % (json_response["error"]["code"], json_response["error"]["messages"]))
        exit(1)
    return json_response


# Looking up the hash of the file in metadefender data base
def analyze_hash(h, api):
    url = "https://api.metadefender.com/v4/hash/"
    url += h
    headers = {
        "apikey": api
    }
    response = requests.request("GET", url, headers=headers)
    return response


def run():
    while True:
        api_key = "1e0110a6bd695ff3f9c9f831b339f04d"
        command = input("enter your command (e.g upload + file name)")
        command = command.split(" ")
        if command[0] == "upload":  # check to see if the input command is correct
            file_name = command[1]
            print("file name: " + file_name)
            h = str(hash_file(file_name))
            print("files hash: " + h)
            h_analyze = analyze_hash(h, api_key)
            h_analyze_json = h_analyze.json()
            if h_analyze.status_code == 200:   # check to see if the hash exist in metadefender data base:
                scan_d = h_analyze_json["scan_results"]["scan_details"]
                for value in scan_d:
                    print("engine: " + value)
                    # if the threat found in the engine
                    if h_analyze_json["scan_results"]["scan_details"][value]["threat_found"] != "":
                        print("threat found: " + h_analyze_json["scan_results"]["scan_details"][value]["threat_found"])
                    else:  # if no threat found in the engine
                        print("threat found = clean")
                    print("scan-results: " + str(h_analyze_json["scan_results"]["scan_details"][value]["scan_result_i"]))
                    print("def_time: " + h_analyze_json["scan_results"]["scan_details"][value]["def_time"])
                    print("")
            else:   # if there was no result of the hash file in metadefender, then upload the file
                print("clean")
                print("uploading the file ...")
                data_id = upload_file(file_name, api_key)
                analysis_r = analysis_result(data_id, api_key)
                while analysis_r["scan_results"]["progress_percentage"] != 100:  # check the status of the analysis
                    print(str(analysis_r["scan_results"]["progress_percentage"]) + "%")  # show the status of scan
                    analysis_r = analysis_result(data_id, api_key)
                # if no threat found in the data base
                if analysis_r["scan_results"]["scan_all_result_a"] == "No Threat Detected":
                    print("overall status: clean")
                scan_details = analysis_r["scan_results"]["scan_details"]
                for value in scan_details:  # show the result of the scan for each engine
                    print("engine: " + value)
                    if analysis_r["scan_results"]["scan_details"][value]["threat_found"] != "":
                        print("threat found: " + analysis_r["scan_results"]["scan_details"][value]["threat_found"])
                    else:
                        print("threat found = clean")
                    print("def_time: " + analysis_r["scan_results"]["scan_details"][value]["def_time"])
                    print("scan-results: " + str(analysis_r["scan_results"]["scan_details"][value]["scan_result_i"]))
                    print("")
        else: # if the input command is wrong, show the correct input command form
            print("try \" upload + {file name}")


run()


