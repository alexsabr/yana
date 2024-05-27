import requests
import bs4
import typing
import abc


class Article():
    def __init__(self,title,condensed,text):
        self.title = title
        self.condensed = condensed
        self.text=text
    
    def __str__(self):
        return f" TITLE={self.title} \n CONDENSED={self.condensed} \n TEXT={self.text}"


class Main_Page_Scrapper(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_article_links(cls,url:str)->list[str]:
        """ Return a list of url to  all articles on the main page."""
        pass


class Article_Scrapper(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_article(cls,url:str)->Article:
        """ Return The Scrapped Conctent from the URL of an Article."""
        pass


class Main_Page_Scrapper_Le_Monde(Main_Page_Scrapper):

    # Main interest function, must be implemented by all Main page scrappers 
    @classmethod
    def get_article_links(cls,url:str)->list[str]:
        tree  = cls.__scrap_main_page(url)
        result:bs4.ResultSet[bs4.PageElement]= tree.find_all(Main_Page_Scrapper_Le_Monde.__full_article_filter)
        toret = [ cls.__extract_link(raw_article) for raw_article in result ]
        return toret
          
      

    @classmethod
    def __scrap_main_page(cls,url:str) -> bs4.BeautifulSoup:
        """ returns None if URL is invalid / unreachable, else a BeautifulSoup of all beacons"""
        if url is None : return None
        result=requests.get(url)
        if not result.ok : return None
        tree = bs4.BeautifulSoup(result.text,features="html.parser")
        return tree 

    @classmethod
    def __generate_filter_by_article_type(cls,article_type:str) -> typing.Callable[[bs4.Tag],bool]:
        """ Returns a filter function which can be used in beautifulSoup find* function,
         to filter Articles of Le Monde main's page based on the type of article"""
        generic_filter = lambda tag :   tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 
        return generic_filter


    @classmethod
    def __full_article_filter(cls,tag:bs4.Tag)-> bool:
        toret =cls.__filter_articles_only(tag)
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Tribune")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Chronique")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Éditorial")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Entretien")) is None
        toret = toret and tag.find(cls.__filter_live) is None
        return toret      
    
    @classmethod
    def __filter_articles_only(cls,tag:bs4.Tag)-> bool: 
            return tag.name=="div" and tag.has_attr('class') and "article" in tag["class"] 

    @classmethod
    def __filter_live(cls,tag:bs4.Tag)-> bool: 
            return tag.name=="span" and tag.has_attr('class') and "flag-live-cartridge" in tag["class"]

    @classmethod
    def __extract_title(cls,tag:bs4.Tag)-> str | None :
        """From the Main Page Le Monde, extracts the Title of the given Article.  """
        filter :typing.Callable[[bs4.Tag],bool] = lambda searchtag : searchtag.has_attr("class")and 'article__title' in searchtag["class"]
        return tag.find(filter).text
    
    @classmethod
    def __extract_link(cls,tag:bs4.Tag)-> str| None:
        """From the Main Page Le Monde, extracts the link to the given Article.  """
        filter :typing.Callable[[bs4.Tag],bool] = lambda searchtag : searchtag.name == "a" 
        return tag.find(filter)["href"]


class Article_Scrapper_Le_Monde(Article_Scrapper):

    #========= Main interest function, must be implemented by all scrapers
    @classmethod
    def get_article(cls,url:str)->Article:
        """Given the URL of a Le Monde Article, converts it to an Article Object."""
        tree:bs4.BeautifulSoup = cls.__download_page(url)
        if tree is None : raise RuntimeError("Unable to Access the requested web page or to convert it into a soup.")
        return cls.__parse_page(tree)

    # ================ helper functions  ===================
    @classmethod
    def __download_page(cls,url:str)-> bs4.BeautifulSoup | None:
        """ Downloads the Page at the given URL and converts it into a Soup."""
        if url is None : return None
        result=requests.get(url)
        if not result.ok : return None
        return  bs4.BeautifulSoup(result.text,features="html.parser")
   
    @classmethod
    def __parse_page(cls,pagesoup:bs4.BeautifulSoup):       
        artic_title=pagesoup.find(cls.__filter_title).text       
        artic_desc=pagesoup.find(cls.__filter_description).text
        artic_text=""
        for paragraph  in  pagesoup.find_all(cls.__filter_text_only) :
            paragraph:bs4.Tag
            artic_text+="\n"+ paragraph.text
        return Article(artic_title,artic_desc,artic_text)
    
    # ======== filter functions to analyse the tree (helper lambdas  of the helper functions) ============
    @classmethod
    def __filter_text_only(cls,tag:bs4.Tag)-> bool: 
            return tag.name=="p" and tag.has_attr('class') and "article__paragraph" in tag["class"] 
        
    @classmethod
    def __filter_description(cls,tag:bs4.Tag)-> bool: 
        return tag.name=="p" and tag.has_attr('class') and "article__paragraph" in tag["class"] 

    @classmethod
    def __filter_title(cls,tag:bs4.Tag)-> bool: 
        return tag.name=="h1" and tag.has_attr('class') and "article__title" in tag["class"] 
        


    


if __name__=="__main__":
    link_array=Main_Page_Scrapper_Le_Monde.get_article_links("https://www.lemonde.fr/")
    article_array=[]
    for a_link in link_array:
        print(a_link)
        article_array.append(Article_Scrapper_Le_Monde.get_article(a_link))
    print(len(article_array))
    
    

    
    
    



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
