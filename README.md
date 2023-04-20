# SII

###### _Created on: 17/03/2023_

### Project execution 

---

#### **Prerequisites**
1.- install docker [DOCKER](https://www.docker.com/)

2.- execute the command:

        docker-compose build

3.- execute the command

        docker-compose up

4.- enter redis

        docker exec -it redis_sii redis-cli

5.- set a key or obtain a value

        SET hello word
        GET hello

#### **Execute test**

        pytest tests/test_service.py

# NOTE
to use this project is required to install docker in the machine
