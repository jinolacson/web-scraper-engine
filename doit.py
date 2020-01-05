from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts

import os,sys

client = Client('http://188.166.184.63/xmlrpc.php', 'admin', 'cgeek111')

datas = open("text").readlines()

counter = 0
for d in datas:
	vid = d.split(" ")[0]
	filename = "img/"+vid+".jpg"
	code = vid.split("_")[1]
	
	title = d.split('"')[1]

	iframe = '' % code

	# prepare metadata
	data = {
		'name': code+'.jpg',
		'type': 'image/jpeg',  # mimetype
	}
# read the binary file and let the XMLRPC library encode it into base64
	with open(filename, 'rb') as img:
        	data['bits'] = xmlrpc_client.Binary(img.read())
	response = client.call(media.UploadFile(data))
	# response == {
	#       'id': 6,
	#       'file': 'picture.jpg'
	#       'url': 'http://www.example.com/wp-content/uploads/2012/04/16/picture.jpg',
	#       'type': 'image/jpeg',
	# }
	attachment_id = response['id']
	post = WordPressPost()
	post.title = title
	post.content = iframe
	post.post_status = 'publish'
	post.thumbnail = attachment_id
	post.id = client.call(posts.NewPost(post))	        
	
	if counter > 6000:
		break
	counter = counter + 1
	print counter
exit()







