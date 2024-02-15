import requests
import json

# URL of the PHP script
php_script_url = "http://localhost/folder_parser/username.php"  # Update the URL accordingly
data = {
    'email': 'example@example.com',
    'row_newfile': 0,
    'row_oldfile': 5,
    'row_duplicate': 6
}

response = requests.post(php_script_url, data=json.dumps(data))
if response.status_code == 200:
    result = response.json()
else:
    print("Error communicating with PHP script. Status code:", response.status_code)
                          