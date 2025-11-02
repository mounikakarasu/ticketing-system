Tickeying System 
A simple ticketing system running on Kubernetes, built to demonstrate: 
- Microservices architecture
- REST APIs
- Docker containers
- Kubernetes deployment and calling
- Persistent database storage
- Real API + Web UI integration
  
Architectural components and their purpose
- User Service (FastAPI python) creates and stores users
- Ticket Service (FASTAPI python) creates and stores tickets
- UI Service (Node/Express) provides Web UI where you view users and tickets
- Database (PostgreSQL + PVC) is a persistent data storage
- Kubernetes (Deployment+services) helps with orchestrationa and scaling

The system is run and after checking pods, UI opens at http://localhost:30080
I create the user and the ticket and work with the docker images for user service, ticket service and UI.
For Scaling demo,
kubectl scale deploy/user-service --replicas=3
kubectl scale deploy/ticket-service --replicas=3
and self healing,
kubectl delete pod <ticket-pod-name>

TO keep it secure,
-API only accessible locally
-K8s networking isolates services
-DB secured inside cluster (not public)
-It can be further improvd using JWT auth

Repository structure
ticketing-system/
 -user service/
 -ticket-service/
 -ui/
 -k8s/
 -Dockerfiles
 -requirements.txt

 This assignment demonstrates cloud-native microservices, stateless service design, stateful DB with Persistent Volume and horizontal pod autoscaling and fault tolerance and restart behavior.


