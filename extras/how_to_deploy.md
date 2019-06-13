## How to deploy on Google Kubernetes Engine  
  
### Dockerize and upload to Google Container Registry  
- ```docker build -t gcr.io/${GCP_PROJECT_ID}/iot-weather:v1 .```  
- ```docker push gcr.io/${GCP_PROJECT_ID}/iot-weather:v1```  
  
### Deploy to Kubernetes Engine  
- Create the cluster:   
```gcloud container clusters create iot-weather-cluster --num-nodes=2```  
- Deploy:  
```kubectl run iot-weather --image=gcr.io/${GCP_PROJECT_ID}/iot-weather:v1 --port 5000```  
- Check status: ```kubectl get pods```  
- Once running, expose the app:
```kubectl expose deployment iot-weather --type=LoadBalancer --port 80 --target-port 5000```  
- Get the external IP: ```kubectl get service```  
  
### Clean up  
- ```kubectl delete service```  
- ```gcloud container clusters delete iot-weather-cluster```