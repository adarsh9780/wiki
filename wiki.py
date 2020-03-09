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
					text = text + para.text
					# if take_input():
					# 	continue
					# else:
					# 	break
				# pretty print
				size = os.get_terminal_size()
				cols, lines = size.columns, size.lines
				total_chars = cols*lines-cols
				print(text[:total_chars])
				counter = total_chars
				while counter < len(text):
					end = counter+cols # index of last charcter to be printed
					# if last char is not space
					while (text[end] != ' ') or (text[end] != '\n'):
						end = end-1
					# print one line at a time
					print(text[counter: end], end='')
					counter = end
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
