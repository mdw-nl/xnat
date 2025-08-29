import requests
from requests.auth import HTTPBasicAuth
import json
import xml.etree.ElementTree as ET
import time

"""This class is made for when XNAT is booted up to automatically configure the whole site. The configure_site is there to setup the settings of the site.
Configure_SCP is for automatically making the SCP receivers. The configure_project is for making the projects. If you would like to make different configurations
you need to change the files in the XNAT_configure folder. It is important that AE title and the project id are the same."""

class XNAT_configure:

    def __init__(self):
        self.json_headers = {"Content-Type": "application/json"}
        self.project_headers = {"Content-Type": "application/xml"}

    def configure_site(self, site_setup_path, site_url, username, password):
        
        with open(site_setup_path, "r") as json_data:
            site_data = json.load(json_data)
        
        response = requests.post(site_url, json=site_data, headers=self.json_headers, auth=HTTPBasicAuth(username, password))
        print("Status site-setup:", response.status_code)
        
    def configure_SCP(self, SCP_receiver_path, SCP_url, username, password):
        
        # Standard defined SCP receiver first needs to be deleted
        delete_id = {"id": 1}
        requests.delete(f"{SCP_url}/1", json=delete_id, headers=self.json_headers, auth=HTTPBasicAuth(username, password))
        
        with open(SCP_receiver_path, "r") as json_data:
            SCP_dataset = json.load(json_data)

        for data in SCP_dataset:
            response = requests.post(SCP_url, json=data, headers=self.json_headers, auth=HTTPBasicAuth(username, password))
            print("Status SCP-receivers:", response.status_code)

    def configure_project(self, project_path, project_url, username, password):
        
        with open(project_path, 'r', encoding='utf-8') as file:
            xml_dataset = file.read()
            
        root = ET.fromstring(xml_dataset)
        namespaces = {'xnat': 'http://nrg.wustl.edu/xnat'}

        for project in root.findall('xnat:projectData', namespaces):
            project_data = ET.tostring(project, encoding='unicode')
            response = requests.post(project_url, data=project_data, headers=self.project_headers, auth=HTTPBasicAuth(username, password))
            print("Status projects:", response.status_code)
            
    def configure_DICOM_routing(self, routing_path, routing_url, username, password):
        print("yaaaahhhahhhhhh")
        while True:
            try:
                check_url = requests.get(routing_url, auth=HTTPBasicAuth(username, password))
                if check_url.status_code == 200:
                    print("XNAT routing endpoint is ready")
                    break
                else:
                    print("XNAT routing endpoint is not yet ready")
                    time.sleep(5)
                    
            except requests.exceptions.RequestException as e:
                print(f"XNAT not reachable yet: {e}")
                
            time.sleep(10)
        
        with open(routing_path, "r") as json_data:
            routing_data = json.load(json_data)
        
        response = requests.put(routing_url, json=routing_data, headers=self.json_headers, auth=HTTPBasicAuth(username, password))
        print("Status custom DICOM routing:", response.status_code)
        print("Response body:", response.text)

if __name__ == "__main__":
    scp_url = "http://localhost:8080/xapi/dicomscp"
    project_url = "http://localhost:8080/data/projects"
    site_url = "http://localhost:8080/xapi/siteConfig"
    dicom_routing_url = "http://localhost/data/config/dicom/sessionRules"
    
    scp_receiver_path = "/XNAT_conf/XNAT_configure/SCP_receiver.json"
    project_path = "/XNAT_conf/XNAT_configure/project.xml"
    site_setup_path = "/XNAT_conf/XNAT_configure/site_setup.json"
    dicom_routing_path = "/XNAT_conf/XNAT_configure/DICOM_routing.json"
    
    username = "admin"
    password = "admin"

    configure = XNAT_configure()
    configure.configure_site(site_setup_path, site_url, username, password)
    configure.configure_SCP(scp_receiver_path, scp_url, username, password)
    configure.configure_project(project_path, project_url, username, password)
    configure.configure_DICOM_routing(dicom_routing_path, dicom_routing_url, username, password)