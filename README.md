# Hello!
"pinnacle-parser"

My test case parser  and db structure for pinnacle.com.

_______________________________________________________

Web spider based on scrapy framework.

# Instalation:

Pull repo, than:
        
        $ pip3 install -r requirements.txt
    
You can edit scraping links, spider have www.pinnacle.com mirror site links(www.qpk30mol.website), I cant get OK persponses from pinnacle even with proxy.

Proxy settings requered.

Dont forget TODO's.

# Structure:

spider: 
        
        spiders.pinnacle_spider.py

db connection settings(planned):
                
        models.py

I think SQLAlchemy really better in use here but I don't know how to handle him yet. 
Pipelines and items could be great realizen with SQLAlchemy so, next commit will be focused on it.

Django models db structure:
                
        django_models.py
        
I realized DB structure with django-ORM without django framework(proof of concept), so it have no pipelines.

# Using:

From project directory:
        
       $ scrapy crawl teamlines  +(-o data.json/csv optional)

