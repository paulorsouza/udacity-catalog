Udacity Pet Catalog
==

## Prerequisites

- [vagrant](https://www.vagrantup.com/)

## Install

```shell
git clone https://github.com/paulorsouza/udacity-catalog.git
cd udacity-catalog

vagrant up
vagrant ssh
```

### Run

```shell
cd /vagrant/catalog
python3 app.py
```

## App url

```
http://localhost:5000
```

## Rest endpoints

**List all families**
----
   This enpoint list all pet families.

* **URL**

  /family/data.json

* **HTTP Verb:**
  
  `GET`
  

* **Sample:**

  ```javascript
     fetch("http://localhost:5000/family/data.json", {
        method: "GET",
        headers: {
           "Accept": "application/json",
        },
     })
  ```

  ```shell
    curl -X GET -H "accept: application/json" http://localhost:5000/family/data.json
  ```


**List all types**
----
   This enpoint list all pet types by family.

* **URL**

  /family/{family_id}/type/data.json

* **HTTP Verb:**
  
  `GET`
  

* **Sample:**

  ```javascript
     fetch("http://localhost:5000/family/1/type/data.json", {
        method: "GET",
        headers: {
           "Accept": "application/json",
        },
     })
  ```

  ```shell
    curl -X GET -H "accept: application/json" http://localhost:5000/family/1/type/data.json
  ```


**Get type**
----
   This enpoint list get pet type by id.

* **URL**

  /type/id/data.json

* **HTTP Verb:**
  
  `GET`
  

* **Sample:**

  ```javascript
     fetch("http://localhost:5000/type/1/data.json", {
        method: "GET",
        headers: {
           "Accept": "application/json",
        },
     })
  ```

  ```shell
    curl -X GET -H "accept: application/json" http://localhost:5000/type/1/data.json
  ```
