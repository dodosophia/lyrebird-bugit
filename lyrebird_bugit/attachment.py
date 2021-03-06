from pathlib import Path
import codecs
import lyrebird
import requests
import shutil
from lyrebird.application import config

BUGIT_STORAGE = lyrebird.get_plugin_storage()
ATTACHMENT_ROOT = Path(BUGIT_STORAGE)/'attachments'

EXPORT_URL = f'http://127.0.0.1:{config.get("mock.port")}/api/snapshot/export/event'

def _check_dir():
    if not ATTACHMENT_ROOT.exists():
       ATTACHMENT_ROOT.mkdir(parents=True, exist_ok=True)

def export_snapshot(snapshot):
    _check_dir()
    file_content = requests.post(EXPORT_URL,json=snapshot['eventObj'],stream=True).content
    with codecs.open(str(ATTACHMENT_ROOT / snapshot['name'])+'.lb', 'wb') as f:
        f.write(file_content)
    return {'id':snapshot['eventObj']['id'],'name':snapshot['name']+'.lb',
    'path':str(ATTACHMENT_ROOT / snapshot['name'])+'.lb'}

def remove_attach():
    if not ATTACHMENT_ROOT.exists():
        pass
    else:
        shutil.rmtree(ATTACHMENT_ROOT)
