import requests_html as rh

user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1'}

session = rh.HTMLSession()

request = session.get('https://www.sciencedirect.com/science/article/pii/S1369703X09003672', headers=user_agent)

print(request)
page = request.html
selector = 'div.abstract.author>div'

print(type(page))

abstract_elements = page.find(selector)
# print(dir(abstract_elements))
for abstract in abstract_elements:
	print(abstract.html.partition())

	print(dir(abstract.html))