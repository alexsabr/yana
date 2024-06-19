import requests
import bs4
import typing
import abc
import re
import spacy
import time 
import logging
from . import models


logger= logging.getLogger(__name__)

class Article():
    """ Small Data Holder class for Articles, regardless of Source."""
     
    __article_nlp = spacy.load('fr_core_news_sm')
    __ARTICLE_SIMILAR_THRESHOLD_LEVEL=0.3
    __lefigaro =models.journal_db(name="Le Figaro", political = models.journal_db.R)
    __lemonde =models.journal_db(name="Le Monde", political = models.journal_db.L)
    

    def convert_to_db_article(self)->models.article_db:
        self.__lefigaro.save()
        self.__lemonde.save()
        return models.article_db(title=self.title,journal=Article.__lefigaro if self.source =="LEFIGARO" else Article.__lemonde ,condensed_text=self.condensed,)

    @classmethod
    def establish_link(cls,article_list1:list["Article"],article_list2:list["Article"]):
        article_db_list1:list["models.article_db"]=[ art.convert_to_db_article() for art in article_list1]
        article_db_list2:list["models.article_db"]=[ art.convert_to_db_article() for art in article_list2]
        for tosave  in article_db_list1 + article_db_list2: tosave.save()
        
        index_lst1=0
        index_lst2=0
        for artic_lst1 in article_list1 :
            index_lst2=0
            for artic_lst2 in article_list2:
                similarity=artic_lst1.articles_are_similar(artic_lst2)
                if (similarity[0] > 0.2 and similarity[1] > 0.2) or (similarity[0] > 0.4 or  similarity[1] > 0.4):
                    article_db_list1[index_lst1].linked_article.add(article_db_list2[index_lst2])
                index_lst2+=1
            index_lst1+=1



    def __init__(self,title,condensed,text,source):
        def purify_string(to_purify:str)->str:
            "remove french ticks which aren't processed correctly by the module right now"
            return to_purify.replace('’',"'").replace('«','"').replace('»','"')


        self.title:str = purify_string(title)
        self.condensed:str = purify_string(condensed)
        self.text:str=purify_string(text)
        self.source:str=source
        self.wordset= set()
        self.crunch_data()


    def crunch_data(self):
        """Analyzes words present in the Article."""
        spacydoc=self.__article_nlp(self.title +" "+self.condensed+" "+self.text)
        for token in spacydoc:
            if token.pos_ =="NOUN" or token.pos_ == "NUM" :self.wordset.add(token.text.lower())
    
    def articles_are_similar(self,artic:"Article"):
        """Do the articles have enough words in common to be deemed near ?"""
        intersection_size= len(self.wordset.intersection(artic.wordset))  
        return  (intersection_size/len(self.wordset), intersection_size/len(artic.wordset) ) #intersection_size/len(self.wordset)  > self.__ARTICLE_SIMILAR_THRESHOLD_LEVEL and intersection_size/len(artic.wordset)  > self.__ARTICLE_SIMILAR_THRESHOLD_LEVEL

    
    def __str__(self):
        return f" SOURCE={self.source} TITLE={self.title} \n CONDENSED={self.condensed} \n TEXT={self.text}"


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
        toret:list["str"] = [ cls.__extract_link(raw_article) for raw_article in result ]
        print(f"From link {url} scrapped {len(toret)}")
        return [e for e in set(toret)]
        #return toret
          
      

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
        generic_filter = lambda tag :    re.match(f"\s*{article_type}\s*",tag.text) is not  None    #tag.has_attr("class") and "article__type" in tag["class"] and article_type  in tag.text 
        return generic_filter


    @classmethod
    def __full_article_filter(cls,tag:bs4.Tag)-> bool:
        """ From the Main Page of Le Monde, ensures only press articles are extracted."""
        toret =cls.__filter_articles_only(tag)
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Tribune")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Chronique")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Éditorial")) is None
        toret = toret and tag.find(cls.__generate_filter_by_article_type("Entretien")) is None
        toret = toret and tag.find(cls.__filter_live) is None
        return toret      
    
    @classmethod
    def __filter_articles_only(cls,tag:bs4.Tag)-> bool: 
            return (tag.name=="div" and tag.has_attr('class') and "article" in tag["class"]) or (tag.name=="a" and tag.has_attr('class') and "article" in tag["class"] ) or  ( tag.name=="section" and tag.has_attr('class') and "teaser" in tag["class"])

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
        if filter(tag) :return tag["href"]
        else :return  tag.find(filter)["href"]


class Article_Scrapper_Le_Monde(Article_Scrapper):

    #========= Main interest function, must be implemented by all scrapers
    @classmethod
    def get_article(cls,url:str)->Article | None:
        """Given the URL of a Le Monde Article, converts it to an Article Object. Returns None if conversion fails."""
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
        try :
            artic_title=pagesoup.find(cls.__filter_title).text       
            artic_desc=pagesoup.find(cls.__filter_description).text
            artic_text=""
            for paragraph  in  pagesoup.find_all(cls.__filter_text_only) :
                paragraph:bs4.Tag
                artic_text+="\n"+ paragraph.text
            return Article(artic_title,artic_desc,artic_text,"LEMONDE")
        except  AttributeError as  e:
            print(f"Attribute Error {str(e)}")
            return None
    
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
        


class Main_Page_Scrapper_Le_Figaro(Main_Page_Scrapper):

    # Main interest function, must be implemented by all Main page scrappers 
    @classmethod
    def get_article_links(cls,url:str)->list[str]:
        tree  = cls.__scrap_main_page(url)
        result:bs4.ResultSet[bs4.PageElement]= tree.find_all(cls.__full_article_filter)
        toret = [ cls.__extract_link(raw_article) for raw_article in result ]
        print(f"From link {url} scrapped {len(toret)}")
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
        """ From the Main Page of Le Figaro, ensures only press articles are extracted."""
        toret =cls.__filter_articles_only(tag)
        toret = toret and tag.find(cls.__filter_lefigaro_domain_only) 
        return toret      
    
    @classmethod
    def __filter_articles_only(cls,tag:bs4.Tag)-> bool: 
            return tag.name=="article" and tag.has_attr('data-content-name') and ( "newsflash" in tag["data-content-name"] or  "article" in tag["data-content-name"] ) 

    @classmethod
    def __filter_lefigaro_domain_only(cls,tag:bs4.Tag)-> bool: 
            domain_string="https://www.lefigaro.fr"
            return tag.name=="a" and tag["href"].find(domain_string,0,len(domain_string)) == 0

    @classmethod
    def __extract_title(cls,tag:bs4.Tag)-> str | None :
        """From the Main Page Le Figaro, extracts the Title of the given Article.  """
        filter :typing.Callable[[bs4.Tag],bool] = lambda searchtag : re.match("h\d",searchtag.name) is not None 
        return tag.find(filter).text
    
    @classmethod
    def __extract_link(cls,tag:bs4.Tag)-> str| None:
        """From the Main Page Le Figaro, extracts the link to the given Article.  """
        filter :typing.Callable[[bs4.Tag],bool] = lambda searchtag : searchtag.name == "a" 
        return tag.find(filter)["href"]


class Article_Scrapper_Le_Figaro(Article_Scrapper):

    #========= Main interest function, must be implemented by all scrapers
    @classmethod
    def get_article(cls,url:str)->Article | None:
        """Given the URL of a Le Figaro Article, converts it to an Article Object. returns None if conversion failed."""
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
    def __parse_page(cls,pagesoup:bs4.BeautifulSoup)->Article | None:
        """Returns None if the soup given is not a Figaro Article."""
        try :
            artic_title=pagesoup.find(cls.__filter_title).text       
            artic_desc=pagesoup.find(cls.__filter_description).text
            artic_text=""
        
            for paragraph  in  pagesoup.find_all(cls.__filter_text_only) :
                paragraph:bs4.Tag
                artic_text+="\n"+ paragraph.text
            return Article(artic_title,artic_desc,artic_text,"LEFIGARO")
        except AttributeError as e :
            return None
    
    # ======== filter functions to analyse the tree (helper lambdas  of the helper functions) ============
    @classmethod
    def __filter_text_only(cls,tag:bs4.Tag)-> bool: 
            return tag.name=="p" and tag.has_attr('class') and "fig-paragraph" in tag["class"] 
        
    @classmethod
    def __filter_description(cls,tag:bs4.Tag)-> bool: 
        return tag.name=="p" and tag.has_attr('class') and "fig-standfirst" in tag["class"] 

    @classmethod
    def __filter_title(cls,tag:bs4.Tag)-> bool: 
        return tag.name=="h1" and tag.has_attr('class') and "fig-headline" in tag["class"] 
        

    

def get_all_articles_Figaro()-> list[Article]:
    link_array=Main_Page_Scrapper_Le_Figaro.get_article_links("https://www.lefigaro.fr/")+Main_Page_Scrapper_Le_Figaro.get_article_links("https://www.lefigaro.fr/economie")+Main_Page_Scrapper_Le_Figaro.get_article_links("https://www.lefigaro.fr/actualite-france")
    article_array=[]
    for a_link in link_array:
        analysis_result =Article_Scrapper_Le_Figaro.get_article(a_link)
        if analysis_result is None : 
            continue
        article_array.append(analysis_result)
    return article_array


def get_all_articles_Monde()-> list[Article]:
    link_array=Main_Page_Scrapper_Le_Monde.get_article_links("https://www.lemonde.fr/economie-francaise/")
    link_array+=Main_Page_Scrapper_Le_Monde.get_article_links("https://www.lemonde.fr/")
    link_array+=Main_Page_Scrapper_Le_Monde.get_article_links("https://www.lemonde.fr/societe/")
    tempset = set(link_array)
    link_array = [lnk for lnk in tempset]

    article_array=[]
    for a_link in link_array:
        theartic = Article_Scrapper_Le_Monde.get_article(a_link)
        if theartic is None : continue
        article_array.append(theartic)
    return article_array 



def start_scraping():
    logger.critical("Starting scrap !")
    start_time = time.time()
    array_figaro:list["Article"] = get_all_articles_Figaro()
    logger.critical(f"crunched {len(array_figaro)} Figaro in {time.time()-start_time}")
    start_time = time.time()
    array_monde:list["Article"] = get_all_articles_Monde()
    logger.critical(f"crunched {len(array_monde)} Monde in {time.time()-start_time}")
    Article.establish_link(array_figaro,array_monde)
    logger.critical("everything in DB !")
    #toprint=""
    #for artic_fig in array_figaro :
    #    for artic_monde in array_monde:
    #        similarity=artic_fig.articles_are_similar(artic_monde)
    #        toprint += f"Figaro :{artic_fig.title}  \nMonde: {artic_monde.title} \nsimilarity:{similarity} \n\n" if (similarity[0] > 0.2 and similarity[1] > 0.2) or (similarity[0] > 0.4 or  similarity[1] > 0.4) else ""
    #with open("/home/alexandre/Desktop/results.txt","w") as fl:
    #    fl.write(toprint)

        
#if __name__=="__main__":
#    start_scraping()
    
    

    


    
    

    



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
