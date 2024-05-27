import requests
import bs4

#1 DL la première page 
def scrap_main_page(url:str):
    """ returns None if URL is invalid / unreachable, else a tree of all beacons"""
    if url is None : return None
    result=requests.get(url)

    if not result.ok : return None
    tree = bs4.BeautifulSoup(result.text,features="html.parser")
    return tree 

 


def full_article_filter(tag:bs4.Tag)-> bool:
    return filter_articles_only(tag) and  tag.find(filter_article_type_tribune) is None and  tag.find(filter_article_type_chronique) is None  and  tag.find(filter_article_type_editorial) is None and tag.find(filter_article_type_entretien) is None
    # also add entretien !

def filter_articles_only(tag:bs4.Tag)-> bool: 
        return tag.name=="div" and tag.has_attr('class') and "article" in tag["class"] 

def filter_article_type_chronique (tag:bs4.Tag)-> bool:
    article_type = "Chronique"
    return  tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 

def filter_article_type_entretien (tag:bs4.Tag)-> bool:
    article_type = "Entretien"
    return   tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 

def filter_article_type_editorial (tag:bs4.Tag)-> bool:
    article_type = "Éditorial"
    return  tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 

def filter_article_type_tribune (tag:bs4.Tag)-> bool:
    article_type = "Tribune"
    return  tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 

def filter_extract_title(tag:bs4.Tag)-> bool:
    return tag.has_attr("class")and 'article__title' in tag["class"]

## chronique
## entretien 
## éditorial

if __name__=="__main__":
    tree = scrap_main_page("https://www.lemonde.fr")
    result:bs4.ResultSet[bs4.PageElement]= tree.find_all(full_article_filter)
    #result2 = result.find_all(filter_exclude_by_article_type_entretien)
    #result3 = result2.find_all(filter_extract_title)

    print(f"====NOMBRE ARTICLES {len(result)} ====")
    i = 0 
    for e in result :
        #print(type(e))
        e:bs4.element.Tag
        print(f" {i}==============\n {e.find(filter_extract_title).text}")
        i+=1
    
    




# 1bis scrap tous les liens d'articles "prioritaires"


# 2 extraire le texte des articles 
# - attention à ne pas prendre les éditos !


# 3 analyser pour récupérer les données intéressantes
# - date 
# - lieux 
# - protagonistes
# - actions
# - verbes

# 4 
# Tout compiler pour trouver les articles similaires 
# et les articles manquants


#5 présenter
