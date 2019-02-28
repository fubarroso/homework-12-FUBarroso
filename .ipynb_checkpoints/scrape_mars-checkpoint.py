from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

	#Create dictionary holding all data
	mars_data = {}

	browser = init_browser()

 	#Nasa - Mars News (latest news wont load)

	url_1 = 'https://mars.nasa.gov/news/'
	browser.visit(url_1)

	html = browser.html
	soup = bs(html, 'html.parser')

	news_title = soup.find('div', class_="content_title").text
	news_p = soup.find('div', class_="article_teaser_body").text

	#add to dictionary
	mars_data["news_title"] = news_title
	mars_data["summary"] = news_p

	#JPL Mars Images - Featured Image

	url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

	browser.visit(url_2)

	browser.click_link_by_partial_text('FULL IMAGE')

	html = browser.html

	soup2 = bs(html, 'html.parser')

	full_article =soup2.find('article', class_="carousel_item") 

	url = full_article.find('a', class_="button fancybox")['data-fancybox-href']

	featured_image_url = 'https://www.jpl.nasa.gov'+url

	#add to dictionary
	mars_data["featured_image_url"] = featured_image_url

	#Mars Weather

	url_3 = 'https://twitter.com/MarsWxReport?lang=en'

	response = requests.get(url_3)

	soup3 = bs(response.text, 'html.parser')

	tweets = soup3.find_all('p', class_="TweetTextSize")

	mars_weather = soup3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

	#add to dictionary
	mars_data["mars_weather"] = mars_weather

	#Mars Facts (done)

	url_4 = 'https://space-facts.com/mars/'

	data_table = pd.read_html(url_4)
	mars_table= data_table[0]
	mars_table.to_html('table.html', header=False, index=False)
	marsinfo = mars_table.to_html(classes='marsinformation')

	#add to dictionary
	mars_data["mars_table"] = marsinfo

	#Mars Hemispheres

	url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

	response = requests.get(url_5)

	soup5 = bs(response.text, 'html.parser')

	hemisphere_links = soup5.find_all('div', class_="item")   

	hemis_titles=[]
	hemis_links=[]



	for links in hemisphere_links:
		title = links.h3.text

		hrefs = links.a['href']
		link = 'https://astrogeology.usgs.gov'+hrefs

		response = requests.get(link)
		soup_2 = bs(response.text, 'html.parser')

		photo_link = soup_2.find('a', href=True, text='Original')['href']

		hemis_titles.append(title)
		hemis_links.append(photo_link)

	hemisphere_image_urls=[]

	for x in range(len(hemis_titles)):
		mydict = {}
		mydict["title"]=hemis_titles[x]
		mydict["img_url"]=hemis_links[x]

	hemisphere_image_urls.append(mydict)

	mars_data['mars_hemis'] = hemisphere_image_urls

	return mars_data
