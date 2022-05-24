# Behavox ML Infra test task

In this test task you'll need to build a solution that runs different tasks using scheduler in microservice fashion. 

Build these services:
* scheduler service:
  * should have asyncronous API, meaning that it contains at least these endpoints:
    * endpoint to receive POST request with task specs to run, and responds immediately with task ID;
    * endpoint to receive POST request with task ID and responds immediately with task status ("NOT RUN YET", "IN FLIGHT", "FAILED", "DONE");
    * endpoint to receive POST request with task ID to query the result of the task execution. If the task is "FAILED" then the result should contain exception and stack trace. If it is "DONE" then results of calculation;
  * additional endpoints to implement:
    * workers status
  * should have the field with worker affinity in task specs request (e.g. it should be told which worker should run the task);
  * extra: state with task statuses should be pushed to SQL/NOSQL DB by your choice.
* worker service should be able to receive the task from the scheduler and run it in it's own environment.

Task to run by the workers should be loaded with dill, please check out the provided examples. Function to run has the name 'run' and accepts keyword arguments x,y and z. 

Worker #1 should run task in python=3.6.13 environment with correspondent requirements installed (check out provided repo instructions).

Worker #2 should run task in python=3.8.13 environment wit correspondent requirements installed (check out provided repo instructions).

Feel free to extend/change the provided examples. Requirements in correspondent workers directories are minimal sufficient to run the pickled "run" functions.

# DOD:

* docker-compose.yml file that can start all needed services, at least scheduler, worker_36, worker_38 or more if needed.
* scheduler binds to 8081 port and provide API with endpoinds listed above
* scheduler API can execute task request with specified worker
* repo contains README.md file with at least examples of execution of scheduler API requests using curl

Extra points are added for:

* scheduler tasks resiliency: if it has task for py36 worker and worker is not started, then it can tolerate this situation for a couple of minutes and only after that put "FAILED" status in the task 
* API's structure for scheduler and workers. Keep in mind such future possible improvements as: API extensibility, possibility to add UI, possibility to add metrics endpoint, more different workers, etc.
* scheduler state pushed to DB

# Examples

### Minimal example for worker #1 (python=3.6.13)

```
cd py36_worker;docker build . -t py36w;docker run py36w:latest python child_task.py
```

### Minimal example for worker #2 (python=3.8.13)

```
cd py38_worker;docker build . -t py38w;docker run py38w:latest python child_task.py
```
