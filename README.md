# sOrTES
A Supportive Tool for Stochastic Scheduling of Manual Integration Test Cases

## Scope
sOrTES is a web-based decision support system for prioritization of test cases with dependencies, known time according to a certain score (often requirement coverage).

## Structure
The program is written as two separate apps, backend and frontend. It is recommended that the backend app is deployed to a server which can locally be accessed on the network.

## Installation
### Backend

The program is written with python3. Hence, a valid installation of python3 is required.

The following packages are also required:
 - flask (http://flask.pocoo.org/docs/1.0/installation/)
 - graphviz (https://pypi.org/project/graphviz/)
 - python-igraph (http://igraph.org/python/)

These can be installed by the following command:

<code> pip3 install {package name} </code>

### Frontend
The frontend app is built with Node.js, hence a valid installation of node is required to make any changes to the app. The additional necessary packages which is required to compile the app can be installed with the following command while being inside the frontend directory:

<code> npm install </code>

If any changes are done, one must run the following command:

<code>npm run build </code>
## Usage
Please note that the usage is different if deployed to a server. If used locally:
1.	Open a terminal
2.	Access the backend folder
3.	Run <code>python3 main.py</code>

