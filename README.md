
## Deployment: 

### Step 1: Build the container based on ray worker image.
#### Build the image:

docker build -t <path-to-your-image> -f Dockerfile .

#### Push image to repo: 

docker push <path-to-your-image>

### Step 2: Set up a kubernetes cluster on GCP. 
#### -> e2-standard-16, 16 vCPU, 64 GB RAM

gcloud container clusters create ray-cluster-autoscaler \
    --num-nodes=1 --min-nodes 2 --max-nodes 11 --enable-autoscaling \
    --zone=us-central1-c --machine-type e2-standard-16

### Step 2:  Deploy the ray cluster on kubernetes with the KubeRay operator
#### Create the KubeRay operator:

kubectl create -k "github.com/ray-project/kuberay/ray-operator/config/default?ref=v0.3.0&timeout=90s"

#### Create a ray cluster with ray cluster manifest:
#### -> ensure that settings in manifest contain the following values
##### namespace: %your_name%
##### image:  %your_image%

kubectl apply -f {$RAY-CLUSTER-MANIFEST}


