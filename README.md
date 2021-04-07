# Introduction
This lab is a simulated vulnerable Uptime Checks featrue from Google Cloud Monitoring. Here's the video that covers the theory of $31k blind SSRF that was found there:

[$31,000 Google Cloud blind SSRF + HANDS-ON labs](https://youtu.be/ashSoc59z1Y)

The lab is only a simulation and it allows you to try your skills in writing the exploit with advanced techniques of blind data exfiltration, covered in the video. 

There's one exposed service that simulates the GCP console's Uptime Checks functionality and another one, not exposed from the container, that simulates the GCP metadata endpoints (a few of them to be precise).

The application is free, but not bug-free. There are surely some unhandled exceptions and so on. If you encounter an interesting problem, create an issue.
# Installation
## Option 1: git clone + docker 
```
git clone https://github.com/gregxsunday/uptime-checks-ssrf.git
cd uptime-checks-ssrf
docker build -t gcp-ssrf .
docker run --rm -p 8000:8000 --name gcp-ssrf gcp-ssrf
```
To terminate
```
docker kill gcp-ssrf
```
## Option 2: dockerhub
```
docker run --rm -p 8000:8000 gregxsunday/gcp-ssrf:latest
```
To Terminate
```
docker ps -a
docker kill {CONTAINER_ID}
```
# Usage
The app is exposed by default on http://localhost:8000
## Important - metadata address
The **IP address 169.254.169.254 doesn't work**. You must use `metadata.google.internal` domain.
## Exploring GCP metadata endpoints
Before leaking the data unique for different instances, I suggest leaking common data first. There are two endpoints with common data in the simulated GCP service:
#### /computeMetadata/v1/instance/cpu-platform
Always returns
```
Intel Broadwell
```
#### /computeMetadata/v1/instance/service-accounts/default/scopes
Always returns
```
https://www.googleapis.com/auth/devstorage.read_only
https://www.googleapis.com/auth/logging.write
https://www.googleapis.com/auth/monitoring.write
https://www.googleapis.com/auth/servicecontrol
https://www.googleapis.com/auth/service.management.readonly
https://www.googleapis.com/auth/trace.append
```

You can, of course, also exfiltrate the directory listing (simulated, with only few endpoints)

### Access tokens
Are available only under 
```
/computeMetadata/v1/instance/service-accounts/default/token
```
endpoint. By default, it returns JSON in such form:
```
{"access_token":"' + key + '","expires_in":3600,"token_type":"Bearer"}
```
where `key` is by default 64 characters long (length can be changed) string from lowercase and uppercase letters, digits and `._\`. 
### Configuring key length and number of instances
```sh
export KEY_LENGTH=64
export NO_INSTANCES=4
```
By default, all tokens are 64 characters long and there are only 4 instances, opposed to 213 characters and 54 instances in real-life. The reason is, that, of course, there's only a simulation (namely `random.choice`) of load balancing. In reality, all the traffic goes to one backend instance. Thus, when 54 instances are simulated it takes much longer than it took in real-world, with requests being distributed. However, those parameters can be modified accoring to your preference and machine parameters. You can change those values in the `.env` file. You can't change this when using dockerhub image.
# Differences between this lab and real Uptime Checks
Of course, this is not 1:1 replicated and there are no real GCP instances running. The task is simulated so you can check if you would be able to write the exploit for it. Differences between the real-world include:
* **important** - 169.254.169.254 address doesn't work. To reach the metadata endpoints use `metadata.google.internal` domain
* front-end - it's not beautiful, but if you want to solve the task, you shouldn't care about it,
* token length - by default 64 characters, instead of 213. You can change it in `.env` file
* number of metadata instances - by default 4 instances, instead of 54. You can change it in `.env` file
* not all options from real Uptime Checks are considered, only the relevant parameters are implemented
* only a few endpoints from GCP metadata service are implemented, as described in former chapter. 


# Note
This web application is not secure and you should not expose anywhere besides your local network where only you can access it.
