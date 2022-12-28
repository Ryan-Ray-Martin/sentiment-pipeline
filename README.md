
# Deployment: 

## Step 1: Build the container based on ray worker image.
### Build the image:

docker build -t [path-to-your-image] -f Dockerfile .

docker build -t gcr.io/intrinsic-research-capital/sentiment-pipeline:kuberay -f Dockerfile .

### Push image to repo: 

docker push [path-to-your-image]

docker push gcr.io/intrinsic-capital-research/sentiment-pipeline:kuberay

## Step 2: Set up a kubernetes cluster on GCP. 
### -> e2-standard-16, 16 vCPU, 64 GB RAM

gcloud container clusters create example-cluster \
    --num-nodes=2 \
    --zone=us-central1-a \
    --node-locations=us-central1-a,us-central1-b,us-central1-f \
    --enable-autoscaling --min-nodes=2 --max-nodes=11 \
    --machine-type e2-standard-16


gcloud container clusters create ray-cluster-autoscaler \
    --num-nodes 1 --min-nodes 2 --max-nodes 11 --enable-autoscaling \
    --zone us-central1-c --machine-type e2-standard-16

## Step 3:  Deploy the ray cluster on kubernetes with the KubeRay operator
### Create the KubeRay operator:

kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

### Create a ray cluster with ray cluster manifest:

kubectl apply -f [ray-cluster-manifest.yaml]

### -> note: ensure that settings in manifest contain the following values
#### namespace: %your_name%
#### image:  %your_image%

### -> check out cluster with the following commands:

kubectl get pods -n [user-name]

### -> verify that service endpoints are created: 

kubectl get services -n [user-name]


# raycluster-autoscaler-head-svc 



