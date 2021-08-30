[+] This programm is based on Python 3.8.

[+] For python 2.7, change the function in line 62 from "input" to "raw_input"

[+] For test, put api-key value in line 62 for api_key

[+] request library needs to be installed prior to use:

	https://docs.python-requests.org/en/master/user/install/
	or
	$python -m pip install requests

[+] execute python file, and start your command by "upload + {file name}"

[+] the md5 hash of the file would be calculated and searched against metadefender cloud.

[+] if the hash doesn't exist the file would be uploaded.

[+] The status of the upload will be printed.

[+] After 100% of the file is uploaded, the result of the analysis will be printed.

[+] Any Error from the request, would be displayed along with the description of the error.