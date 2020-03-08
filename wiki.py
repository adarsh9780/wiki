from bs4 import BeautifulSoup
import requests
import argparse

def get_soup(search_term):
	try:
		source = requests.get(f'https://en.wikipedia.org/wiki/{search_term}').text
	except requests.exceptions.ConnectionError:
		print(f'Error: Network Error')
	else:
		soup = BeautifulSoup(source, 'lxml')
		match = soup.find('div', class_='mw-parser-output')
		try:
			all_match = match.find_all('p')
		except AttributeError:
			print(f'Error: Wikipedia does not have any articles on {search_term}')
		else:
			with open(f'{search_term}.txt', 'w') as ofile:
				for para in all_match:
					# print(para.text, file=ofile)
					# print('\n', file=ofile)
					ofile.write(para.text)
					ofile.write('\n')

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-n", "--name",
		help="artice to search on wikipedia",
		type=str)
	args = parser.parse_args()
	if args.name:
		search_term = '_'.join(args.name.split())
		get_soup(search_term)
	else:
		print('No keywords passed; nothing to search')
