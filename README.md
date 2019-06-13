# COEN 241 Project  
Machine learning application for the project **Adopting Kubernetes to Build an End-to-End IoT Model**.  
  
## Prerequisites:  
Set up the IoT simulation: [https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/iot-nirvana](https://github.com/GoogleCloudPlatform/professional-services/tree/master/examples/iot-nirvana)  
   
## How to run locally:  
Set the required environment variables:  
- ``OW_API_KEY``: API key from https://openweathermap.org/  
- ``DATASTORE_SERVICE_ACCOUNT``: Path to the Google Datastore service account JSON file generated through [GCP service accounts](https://cloud.google.com/iam/docs/service-accounts)  
  
Install the required libraries:  
- ```pip install -r requirements.txt```  
  Run:  
- ```python starter.py```  
