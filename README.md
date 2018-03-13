### create venv
* python3 -m venv venv
* source venv/bin/activate
* pip install -r requirements.txt

### launch crawler
* add chrome driver in crawler/bin 
* set credentials in crawler/secret.py
* python crawler-main.py -t photography -u https://www.instagram.com/explore/locations/127963847/madrid-spain/
* python crawler-main.py -t photography

### launch viewer
* python manager.py runserver


### example queries

```
query{
  allSocialUsers(username_Icontains: "rr", engagement_Gt: 0.03){
  edges {
      node {
        id,
        username,
        engagement
      }
    }
  }
}
```

```
query{
  allSocialUsers(engagement_Gt: 0.03, hashtags: "cocina"){
  edges {
      node {
        id,
        username,
        engagement
      }
    }
  }
}
```