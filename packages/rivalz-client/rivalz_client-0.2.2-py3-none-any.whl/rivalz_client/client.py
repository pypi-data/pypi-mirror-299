import time

import requests
import base64
import os

RIVALZ_API_URL = "https://be.rivalz.ai"

RAG_API_URL = "https://rivalz-rag-be.vinhomes.co.uk"


class RivalzClient:
    def __init__(self, secret: str = ''):
        self.secret = secret or os.getenv('SECRET_TOKEN')

    def upload_file(self, file_path: str):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            headers = {
                'Authorization': f'Bearer {self.secret}'
            }
            res = requests.post(f"{RIVALZ_API_URL}/api-v1/ipfs/upload-file", files=files, headers=headers)
            res.raise_for_status()  # Raise an error for bad status codes
            return res.json()['data']

    def upload_passport(self, file_path: str):
        with open(file_path, 'rb') as file:
            files = {'file': file}
            headers = {
                'Authorization': f'Bearer {self.secret}'
            }
            res = requests.post(f"{RIVALZ_API_URL}/api-v1/ipfs/upload-passport-image", files=files, headers=headers)
            res.raise_for_status()  # Raise an error for bad status codes
            return res.json()['data']

    def download(self, upload_hash: str):
        headers = {
            'Authorization': f'Bearer {self.secret}'
        }
        res = requests.get(f"{RIVALZ_API_URL}/api-v2/ipfs-v2/download-file/{upload_hash}", headers=headers)
        res.raise_for_status()  # Raise an error for bad status codes        
        data = res.json()['data']
        file_data = data['file']['data']
        file_name = data['name']
        return file_data, file_name

    def delete_file(self, upload_hash: str):
        headers = {
            'Authorization': f'Bearer {self.secret}'
        }
        res = requests.post(f"{RIVALZ_API_URL}/api-v2/ipfs-v2/delete-file/{upload_hash}", headers=headers)
        res.raise_for_status()  # Raise an error for bad status codes
        return res.json()

    def __upload_file(self, file_path: str):
        request_presigned_url = RAG_API_URL + "/presigned-url"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        file_key = str(round(time.time() * 1000)) + "_" + os.path.basename(file_path)
        params = {
            'file_name': file_key
        }
        res = requests.get(request_presigned_url, headers=headers, params=params)
        res.raise_for_status()
        pre_signed_url = res.json()['url']
        # upload file
        with open(file_path, 'rb') as file:
            res = requests.put(pre_signed_url, data=file)
            res.raise_for_status()  # Raise an error for bad status codes
        return file_key

    def create_rag_knowledge_base(self, file_path: str, knowledge_base_name: str):
        file_key = self.__upload_file(file_path)
        create_knowledge_base_url = RAG_API_URL + "/knowledge-bases"
        payload = {
            'name': knowledge_base_name,
            'fileKey': file_key
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(create_knowledge_base_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def add_document_to_knowledge_base(self, file_path: str, knowledge_base_id: str):
        file_key = self.__upload_file(file_path)
        add_document_url = RAG_API_URL + "/knowledge-bases/add-file"
        payload = {
            'id': knowledge_base_id,
            'fileKey': file_key
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(add_document_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def delete_document_from_knowledge_base(self, file: str, knowledge_base_id: str):
        delete_document_url = RAG_API_URL + "/knowledge-bases/del-file"
        payload = {
            'id': knowledge_base_id,
            'fileKey': file
        }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(delete_document_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def get_knowledge_bases(self):
        get_knowledge_base_url = RAG_API_URL + "/knowledge-bases"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_knowledge_base_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_knowledge_base(self, knowledge_base_id: str):
        get_knowledge_base_url = RAG_API_URL + f"/knowledge-bases/{knowledge_base_id}"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_knowledge_base_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def create_chat_session(self, knowledge_base_id: str, message: str, session_id=None):
        create_chat_session_url = RAG_API_URL + "/chats"
        if session_id is None:
            payload = {
                'knowledge_id': knowledge_base_id,
                'message': message
            }
        else:
            payload = {
                'knowledge_id': knowledge_base_id,
                'message': message,
                'sessionID': session_id
            }
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.post(create_chat_session_url, headers=headers, json=payload)
        res.raise_for_status()
        return res.json()

    def get_chat_session(self, session_id: str):
        get_chat_session_url = RAG_API_URL + f"/chats/detail/{session_id}"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_chat_session_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_chat_sessions(self):
        get_chat_sessions_url = RAG_API_URL + "/chat-sessions"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_chat_sessions_url, headers=headers)
        res.raise_for_status()
        return res.json()

    def get_uploaded_documents(self):
        get_uploaded_documents_url = RAG_API_URL + "/files"
        headers = {
            'x-rivalz-api-key': self.secret
        }
        res = requests.get(get_uploaded_documents_url, headers=headers)
        res.raise_for_status()
        return res.json()
