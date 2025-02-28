facebook_posts = [
	{'Likes': 21, 'Comments': 2},
	{'Likes': 13, 'Comments': 2, 'Shares': 1},
	{'Likes': 33, 'Comments': 8, 'Shares': 3},
	{'Comments': 4, 'Shares': 2},
	{'Comments': 1, 'Shares': 1},
	{'Likes': 19, 'Comments': 3}
]


def count_likes(posts):
	total_likes = 0
	for post in posts:
		try:
			total_likes = total_likes + post['Likes']
		except KeyError as e:
			print(f"Wrong {e} key!")
		pass
	return total_likes


print(count_likes(facebook_posts))