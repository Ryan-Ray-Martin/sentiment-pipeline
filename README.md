## Deployment: 

### Step 1: Set up a kubernetes cluster on GCP. 
### -> e2-standard-16, 16 vCPU, 64 GB RAM

gcloud container clusters create gpu-cluster-1 \
    --num-nodes=1 --min-nodes 0 --max-nodes 1 --enable-autoscaling \
    --zone=us-central1-c --machine-type e2-standard-8

### Step 2:  Deploy the ray cluster on kubernetes with the KubeRay operator

##### Create the KubeRay operator:
kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

##### create a ray cluster with ray cluster manifest (your .yaml file):
kubectl apply -f {$RAY-CLUSTER-MANIFEST}
