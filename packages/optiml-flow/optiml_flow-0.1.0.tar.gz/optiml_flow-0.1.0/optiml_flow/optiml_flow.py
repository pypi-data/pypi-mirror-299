import json
import requests
from datetime import datetime
from codecarbon import EmissionsTracker


class OptiMLFlow:
    def __init__(self, server_uri, pod_name, namespace):
        self.server_uri = server_uri
        self.pod_name = pod_name
        self.namespace = namespace

    
    def tracker_start(self, project_name):
    
        uri = self.server_uri+'mlco-start' if self.server_uri.endswith("/") else self.server_uri+'/mlco-start'
        payload = json.dumps({
            "project_name": project_name
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", uri, headers=headers, data=payload)
        project_exists = response.json()['projectExists']
        
        if project_exists:
            print("A project with the same name already exists. Please try with a different name!")
        else:
            self.code_carbon_tracker = EmissionsTracker(project_name=project_name, tracking_mode='process')
            
            # Starting the Prometheus tracking for different metrics like GPU, CPU, and memory consumed by the experiment:
            self.project_start_time = datetime.now()
            
            # Starting the Code Carbon's tracker:
            self.code_carbon_tracker.start()
            print("The tracking of the experiment has started successfully....")

    def tracker_stop(self):
        # Stopping the Code Carbon's tracker:
        emissions = self.code_carbon_tracker.stop()
    
        # Stopping the Prometheus tracking for different metrics like GPU, CPU, and memory consumed by the experiment:
        project_end_time = datetime.now()
    
        data = {
            "timestamp": self.code_carbon_tracker.final_emissions_data.timestamp,
            "project_name": self.code_carbon_tracker.final_emissions_data.project_name,
            "run_id": self.code_carbon_tracker.final_emissions_data.run_id,
            "duration": self.code_carbon_tracker.final_emissions_data.duration,
            "emissions": self.code_carbon_tracker.final_emissions_data.emissions,
            "emissions_rate": self.code_carbon_tracker.final_emissions_data.emissions_rate,
            "cpu_power": self.code_carbon_tracker.final_emissions_data.cpu_power,
            "gpu_power": self.code_carbon_tracker.final_emissions_data.gpu_power,
            "ram_power": self.code_carbon_tracker.final_emissions_data.ram_power,
            "cpu_energy": self.code_carbon_tracker.final_emissions_data.cpu_energy,
            "gpu_energy": self.code_carbon_tracker.final_emissions_data.gpu_energy,
            "ram_energy": self.code_carbon_tracker.final_emissions_data.ram_energy,
            "energy_consumed": self.code_carbon_tracker.final_emissions_data.energy_consumed,
            "country_name": self.code_carbon_tracker.final_emissions_data.country_name,
            "country_iso_code": self.code_carbon_tracker.final_emissions_data.country_iso_code,
            "region": self.code_carbon_tracker.final_emissions_data.region,
            "cloud_provider": self.code_carbon_tracker.final_emissions_data.cloud_provider,
            "cloud_region": self.code_carbon_tracker.final_emissions_data.cloud_region,
            "os": self.code_carbon_tracker.final_emissions_data.os,
            "python_version": self.code_carbon_tracker.final_emissions_data.python_version,
            "codecarbon_version": self.code_carbon_tracker.final_emissions_data.codecarbon_version,
            "cpu_count": self.code_carbon_tracker.final_emissions_data.cpu_count,
            "cpu_model": self.code_carbon_tracker.final_emissions_data.cpu_model,
            "gpu_count": self.code_carbon_tracker.final_emissions_data.gpu_count,
            "gpu_model": self.code_carbon_tracker.final_emissions_data.gpu_model,
            "longitude": self.code_carbon_tracker.final_emissions_data.longitude,
            "latitude": self.code_carbon_tracker.final_emissions_data.latitude,
            "ram_total_size": self.code_carbon_tracker.final_emissions_data.ram_total_size,
            "tracking_mode": self.code_carbon_tracker.final_emissions_data.tracking_mode,
            "on_cloud": self.code_carbon_tracker.final_emissions_data.on_cloud,
            "pue": self.code_carbon_tracker.final_emissions_data.pue,
            "project_start_time": self.project_start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "project_end_time": project_end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
            "pod_name": self.pod_name,
            "pod_namespace": self.namespace
        }
    
        uri = self.server_uri+'mlco-stop' if self.server_uri.endswith("/") else self.server_uri+'/mlco-stop'
        payload = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", uri, headers=headers, data=payload)
        data_stored = response.json()['dataStored']
        if data_stored:
            print("The data is stored successfully!")
        else:
            print("The data could not be stored!")