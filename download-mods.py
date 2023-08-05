import json
import requests
import urllib

# Path to manifest.json
manifest_path = ''

# Curseforge API key
api_key = ''

not_found_mods = []

def download_file(url):
    file_name = url.split('/')[-1].replace('%20', ' ')
    u = urllib.request.urlopen(url)
    file = open(file_name, 'wb')
    file_size = int(u.getheader('Content-Length'))
    print("Downloading: {} Bytes: {}".format(file_name, file_size))

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        file.write(buffer)
        status = '{0} B / {1} B [{2:.1f}%]'.format(file_size_dl, file_size,  file_size_dl * 100.0 / file_size)
        print(status, end='\r')

    print("")
    file.close()

file = open(manifest_path, mode='r')
manifest_content = file.read()
file.close()

manifest = json.loads(manifest_content)
print("Downloading {0} mods: ".format(len(manifest['files'])))
for file in manifest['files']:
    url = 'https://api.curseforge.com/v1/mods/{0}/files/{1}/download-url'.format(file['projectID'], file['fileID'])
    headers = {
        'Accept': 'application/type',
        'X-Api-Key': api_key
    }
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        not_found_mods.append('Project ID: {0}, File ID: {1}'.format(file['projectID'], file['fileID']))
        continue
    download_url = json.loads(r.text)['data']
    download_url = download_url.replace(' ', '%20')
    download_file(download_url)

if len(not_found_mods) > 0:
    print("Some mods could not be downloaded:")
    print("---------")
    for mod in not_found_mods:
        print(mod)
