# Kubernetes-based Event Driven Autoscaling with KEDA - A Practical Guide
This reposiory contains source code for the article [Kubernetes-based Event Driven Autoscaling with KEDA- A Practical Guide](https://linktoevoegen.com)

In the article, the basics of Kubernetes Event Driven Autoscaling (KEDA) are first explained. After this is described how to install a lightweight local K8S cluster called Minikube, in which KEDA is also installed. To then demonstrate how KEDA works in practice, a use case is considered for dynamically scaling based on a certain amount of .csv-files that need processing. After following the guide, a person should be able to get KEDA up and running and have a good understanding of the core concepts of it.

# Getting Started
To get started with KEDA in practice, simply follow the steps that are outlined in the article.

# Repository Structure
* The folder `manifests` contains a number of manifests for deploying K8S resources into the Minikube cluster:
  * `deployments/redis-deployment.yaml`: Contains definition for deploying a Redis server used as a dynamic scaling trigger.
  * `helpers/pvc-inspection.yaml`: Contains definition for an inspection pod
  * `jobs/csv-processor-scaled-jobs.yaml`: Contains the definition of ScaledJob used for aggregating CSV files. Central file for KEDA
  * `jobs/data-generator.yaml`: Contains definition for a job that generates raw CSV files that should be aggregated by the ScaledJob processes
  * `services/redis-service.yaml`: Contains definition for a Redis service that exposes the Redis deployment within the cluster
  * `volumes/data-pvc.yaml`: Contains definition for a Persitent Volume Claim used for storing and reading CSV data
* The folder `src` contains two .py-files that are used for creating raw CSV data and for aggregating the CSV data:
  * `src/data_generator.py`: Contains the code needed for generating the CSV files. Is used in the data-generator definition via the `data_generator.Dockerfile` image
  * `src/process_csv.py`: Contains the code needed for aggregating CSV files. Used in the ScaledJob definition via the `csv_processor.Dockerfile` image
* The root folder contains the definitions of the `data_generator.Dockerfile` and `csv_processor.Dockerfile`, which are used in the `jobs`

# Contributing
We welcome contributions from the community! If you find a bug or would like to suggest a new feature, please create a Github issue and we'll take a look.

# About the Author
The article was written by [Tim Molleman](https://www.linkedin.com/in/tim-molleman/), a Data Engineer at [Digital Power](https://digital-power.com/en/)

If you're interested in learning more about how we use other cloud and its services to build scalable, resilient solutions for our customers, please check out our website.