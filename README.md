
# Deployment: 

## Step 1: Build the container based on ray worker image.
### Build the image:

docker build -t [path-to-your-image] -f Dockerfile .

docker build -t gcr.io/intrinsic-research-capital/sentiment-pipeline:kuberay -f Dockerfile .

### Push image to repo: 

docker push [path-to-your-image]

docker push gcr.io/intrinsic-research-capital/sentiment-pipeline:kuberay

## Step 2: Set up a kubernetes production cluster on GCP. 
### -> e2-standard-16, 16 vCPU, 64 GB RAM

gcloud container clusters create ray-cluster \
    --num-nodes=1 --min-nodes 2 --max-nodes=11 --enable-autoscaling \
    --zone=us-central1-c --machine-type e2-standard-16

 
gcloud container node-pools create ray-cluster-node-pool \
    --num-nodes=1 --min-nodes 2 --max-nodes=11 --enable-autoscaling \
    --zone=us-central1-c --cluster ray-cluster --machine-type e2-standard-16 \
    --location-policy=ANY

## Note: For a demo Kubernetes cluster on GCP
# Create a node-pool for a CPU-only head node
# e2-standard-8 => 8 vCPU; 32 GB RAM
gcloud container clusters create ray-cluster \
    --num-nodes=1 --min-nodes 0 --max-nodes 1 --enable-autoscaling \
    --zone=us-central1-c --machine-type e2-standard-8

# Create a node-pool for GPU. The node is for a GPU Ray worker node.
# n1-standard-8 => 8 vCPU; 30 GB RAM
gcloud container node-pools create ray-node-pool \
  --zone us-central1-c --cluster ray-cluster \
  --num-nodes 1 --min-nodes 0 --max-nodes 1 --enable-autoscaling \
  --machine-type n1-standard-8

## Step 3:  Deploy the ray cluster on kubernetes with the KubeRay operator
### Create the KubeRay operator:

kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

kubectl get deployments -n ray-system

kubectl get pods -n ray-system

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




serve build finbert_serve:sentiment -k -o sentiment_config.yaml