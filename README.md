# Introduction

For this test assignment, I have chosen a 3rd party library, FastAPI to create the Cake API, for its speed and ease of use, The endpoints could easily be used by React.js and other frontend web frameworks. 


# Assumptions

1. I have created the cake collection as an in-memory collection. If I had more time, I would like to persist the data in a database such as Postgres or MongoDB (NOSQL)

2. I have implemented authenticaion and included the api-key in the main.py. In the actual production, this will be a dangerous practice as the api-key should never be checked into github.

In the production environment, I would put the api-key in a .env file,  then add the .env file in the gitignore, so 
I would write something like the following to retrieve the api-key in the .env file.

a. pip install python-dotenv

b. create .env file with the following:
api_key="12345"

c. In main.py    
     
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("api_key")

3. I have also written some unit tests using Pytest. 
The tests are in tests/test_cakes.py

To run it: issue the following command in the tests directory
pytest -v test_cakes.py

All tests are passed.

4. Testing the app locally

I have run the app locally by issuing the following command:

uvicorn main:app --reload

On the Chrome browser, I entered https://127.0.0.1:8000/docs, it directed me to the Swagger frontend where I can test my Cake api. 
After entering the authenticaion api-key "12345", I could then sucessfully test all GET, PUT, POST, DELETE operations

5. Testing the app in Docker

I have also run the app in Docker by issuing the following command:

Spin up the Docker desktop demon

# Build image
docker build -t cake-api .

# Run container
docker run -p 8000:8000 cake-api

By entering https://localhost:8000/docs in the Chrome browser, it directed me to the Swagger frontend, I could do exactly what I have done in point 4 above.

6. Deployment to cloud / Scalability / In the even of failure / Future extensions

Deploying the cake app in Docker to the cloud so it runs the same way everywhere. and can be easily moved to any cloud provider like AWS or Google Cloud.

For scaling, use Kubernetes, which automatically spins up more copies of the cake app when traffic gets heavy and spreads them across different data centers so if one goes down, the cake app stays up. It watches things like CPU and memory usage to decide when to scale.

To make it resilient, set up health checks so the system knows if the cake app is healthy or needs restarting.

For future extension, split the cake app into smaller independent services (microservices) so different teams can work on and scale parts separately without breaking the whole system.
