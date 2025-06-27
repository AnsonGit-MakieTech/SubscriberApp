
import requests
import threading
import time
import os
import base64

from utils.app_utils import has_internet

class Communications:
    server = "http://192.168.10.118:8400/"
    function_path = "test_action/"
    token = None
    data = {}
    threads = []
    has_thread_running = False
    session = None
    is_login = False
    
    key_running = []


    def __init__(self):
        self.session = requests.Session()


    def kill_all_threads(self):
        for thread in self.threads:
            thread.join()
        self.threads.clear()

    def get_and_remove(self, key : str):
        if key in self.data:
            value = self.data[key]
            del self.data[key]
            return value
        return None
    
    def is_running(self):
        if len(self.threads) > 0:
            return True
        return False

    def create_session(self, need_data = {}):
        key = "CHECK_PIN"
        def event(self_thread):
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)

            if not has_internet():
                self.data[key] = {"result" : False, "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            need_data['action'] = "technical_register_system_user" 
             
            url = self.server + self.function_path
            headers = {
                "Content-Type": "application/json", 
                "User-Agent": "KivyApp/1.0.0",
            } 
            try:
                response = self.session.post(url, headers=headers, json=need_data)
                if response.ok:
                    data = response.json()
                    message = data.get("text", "")
                    return_data = data.get("data", {})
                    self.data[key] = {"result" : True, "message" : message , "data" : return_data}
                else:
                    # print(response.text)
                    data = response.json()
                    message = data.get("text", "")
                    self.data[key] = {"result" : False, "message" : message }
                
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)

            if self_thread in self.threads:
                self.threads.remove(self_thread)
            
        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()


    def get_data_action(self, need_data = {} , key = "" , action = ""): 
        # This use for get data from server only that need to have a return data as possible
        def event(self_thread):
            
            while self.has_thread_running:
                time.sleep(0.5)
                print("Waiting for thread to finish")
            self.has_thread_running = True
            self.key_running.append(key)
            
            if not has_internet():
                self.data[key] = {"result" : False, "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            need_data['action'] = action

            url = self.server + self.function_path 
            headers = {
                "Content-Type": "application/json", 
                "User-Agent": "KivyApp/1.0.0",
            } 
            try:
                response = self.session.post(url, headers=headers, json=need_data)
                if response.ok: 
                    data = response.json()
                    message = data.get("text", "")
                    return_data = data.get("data", {})
                    self.data[key] = {"result" : True, "message" : message , "data" : return_data} 
                else: 
                    data = response.json()
                    message = data.get("text", "")
                    self.data[key] = {"result" : False, "message" : message }  
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()




    def post_data_action(self, need_data = {} , key = "" , action = ""): 
        # This use for post data to server only that not need to have a return data as possible
        def event(self_thread):
            
            while self.has_thread_running:
                time.sleep(0.5)
            self.has_thread_running = True
            self.key_running.append(key)
            
            if not has_internet():
                self.data[key] = {"result" : False, "message" : "No Internet Connection"}
                self.has_thread_running = False
                self.key_running.remove(key) 
                if self_thread in self.threads:
                    self.threads.remove(self_thread) 
                return

            need_data['action'] = action

            url = self.server + self.function_path
            headers = {
                "Content-Type": "application/json", 
                "User-Agent": "KivyApp/1.0.0",
            } 
            try:
                response = self.session.post(url, headers=headers, json=need_data)
                if response.ok:
                    data = response.json()
                    message = data.get("text", "")
                    return_data = data.get("data", {})
                    self.data[key] = {"result" : True, "message" : message , "data" : return_data}
                else:
                    # print(response.text)
                    data = response.json()
                    message = data.get("text", "")
                    self.data[key] = {"result" : False, "message" : message } 
            except Exception as e:
                    self.data[key] = {"result" : False, "message" : "Error: " + str(e)}
            self.has_thread_running = False
            self.key_running.remove(key)
            if self_thread in self.threads:
                self.threads.remove(self_thread)

        
        thread = threading.Thread(target=lambda: event(thread))
        self.threads.append(thread)
        thread.start()

















