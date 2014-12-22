import gdata.youtube
import gdata.youtube.service
import urlparse
from lxml import etree
from StringIO import StringIO
from xml.etree import cElementTree as ET
import urllib
import re
import nltk 

yt_service = gdata.youtube.service.YouTubeService()

comment_feed_url = "http://gdata.youtube.com/feeds/api/videos/%s/comments"

def WriteCommentFeed(video_id): #, data_file  
    url = comment_feed_url % video_id
    comment_feed = yt_service.GetYouTubeVideoCommentFeed(uri=url)

    try:
        while comment_feed:

            for comment_entry in comment_feed.entry:
                text_file = open("YT_Comment_Output.txt", "a")
                text_file.write(str(comment_entry.content.text))
                text_file.write('\n')
                text_file.close()	

            comment_feed = yt_service.Query(comment_feed.GetNextLink().href) 

    except:
            pass


def get_video_data(xml):
	results = []
	root = ET.fromstring(xml)
	print root
	print root.tag
	#to get add'l attributes from the videos, go for different child.tag's,  
	#### see http://docs.python.org/2/library/xml.etree.elementtree.html
	ns = '{http://www.w3.org/2005/Atom}'
	for child in root:
		if child.tag == (ns+'link'):
			 print child.tag, child.attrib
			 ##append the link of the video to the results list
			 results.append(child.attrib.get('href'))
			 break
	print results
	for link in results: 
		url_data = urlparse.urlparse(link)
		query = urlparse.parse_qs(url_data.query)
		video = query["v"][0]
		print video
		WriteCommentFeed(video)


def getTopVideo(searchTerm):
	yt_service = gdata.youtube.service.YouTubeService()
	query = gdata.youtube.service.YouTubeVideoQuery()
	query.vq = searchTerm
	query.orderby = 'relevance'
	query.racy = 'include'
	feed = yt_service.YouTubeQuery(query)
	#turn this on to mine the comments from just one video
	#xml = feed.entry[0]
	#get_video_data(str(xml))
	#turn this on to mine comments from all the top videos
	for xml in feed.entry:
		get_video_data(str(xml))

search_query = getTopVideo(searchTerm = 'alzheimers')
