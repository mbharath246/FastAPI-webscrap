from typing import Literal
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, status, Depends

from src.endpoints.webscrap.helper_func import WebScrap
from src.endpoints.webscrap import genralize, count_stop_words, searching_keyword
from src.auth.jwt_token_verify import JwtBearer

router = APIRouter(
    tags=["Web-Scrap"],
    prefix="/blogs",
    dependencies=[Depends(JwtBearer())]
    )


@router.post("/{pages}", status_code=status.HTTP_201_CREATED)
def pages_you_want_to_scrap(pages: int):
    titles_list = []
    urls_list = []
    images_list = []
    descriptions_list = []

    url = "https://thehackernews.com/"
    for _ in range(pages):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        titles_list += [title for title in WebScrap.scrap_title(soup)]
        urls_list += [url for url in WebScrap.scrap_urls(soup)]
        images_list += [img for img in WebScrap.scrap_images(soup)]
        descriptions_list += [desc for desc in WebScrap.scrap_description(soup)]

        next_page = soup.find("a", class_="blog-pager-older-link-mobile")["href"]
        url = next_page
    WebScrap.scrap_webpage(titles_list, urls_list, images_list, descriptions_list)
    genralize.genralise_description()
    count_stop_words.create_count_stop_words()

    return {"message": f"{pages} pages scrapped successfully"}


@router.get("/{column}")
def get_blog_details(column: Literal["heading", "url"]):
    headings = WebScrap.show_data_blogs(column)
    return {f"{column}": headings}


@router.get("/desc/{column}")
def get_blogs_description(column: Literal["description", "url", "image"]):
    headings = WebScrap.show_blog_description(column)
    return {f"{column}": headings}


@router.get('/generalise/desc/')
def get_generalised_decription(column:str = "description"):
    description = WebScrap.get_generalise_blog(column)
    if column != "description":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="column not found")
    return {f"{column}" : description}


@router.get('/keyword/{keyword}')
def searching_keyword_urls(keyword:str):
    urls = searching_keyword.search_keyword(keyword)
    if not urls:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Keyword")
    return {"urls":urls}

@router.get('/stopwords/count')
def get_stop_words():
    words = WebScrap.get_stop_words_count()
    return{"count_stop_words":words}