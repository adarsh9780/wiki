from bs4 import BeautifulSoup
import requests
import argparse
import os

def get_soup(search_term, action=None):
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
			if action is None:
				print('action is None')
				with open(f'{search_term}.txt', 'w') as ofile:
					for para in all_match:
						ofile.write(para.text)
						ofile.write('\n')
			elif action:
				print('action is not none')
				text = ''
				for para in all_match:
					text = text + '\n' + para.text

				# print first screen completely
				size = os.get_terminal_size()
				cols, lines = size.columns, size.lines
				# no. of chars that can be accomodated one screen space
				total_chars = cols*(lines-1)
				start = 0
				end = get_end_index(text[start:total_chars])
				# print(f'Outside; start: {start}, end: {end}')
				print(text[start:end])
				# print(f'start: {start}, end: {end}')

				# print rest of the charcters, one line at a time
				while end < len(text):
					start = end
					end = get_end_index(text[0:end+cols])
					# print(f'start: {start}, end: {end}')
					print(text[start:end], end='')
					if take_input():
						continue
					else:
						break

def take_input():
	ipt = input()
	if ipt == '':# Empty Line
		return True
	else:
		return False

def get_end_index(sub_str):
	for i in range(len(sub_str)-1, -1, -1):
		if (sub_str[i] == '\n') or (sub_str[i] == ' '):
			return i

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	# --name
	parser.add_argument('-n', '--name', help='artice to search on wikipedia', type=str)
	# --print
	parser.add_argument('-p', '--print', help='print the result, instead of saving', action='store_true')
	args = parser.parse_args()
	if args.name:
		search_term = '_'.join(args.name.split())
		if args.print:
			get_soup(search_term, action=args.print)
		else:
			get_soup(search_term)
	else:
		print('No keywords passed; nothing to search')
