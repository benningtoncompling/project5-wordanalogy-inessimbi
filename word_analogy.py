#!/usr/bin/python3
#
# word_analogy.py - building
# Author: <Ines Simbi>(inessimbi@bennington.edu)
# Date: <05.05.2019>./word_analogy.py <vector_file> <input_directory> <output_directory> <eval_file>
# <should_normalize> <similarity_type>



#import sys
import sys, os
import numpy as np
import gensim
from gensim.models import Word2Vec

file_name = sys.argv[1]
google_test_set = sys.argv[2]
out_file_name = sys.argv[3]
output_eval_file = sys.argv[4]


file_name = "smaller_model.txt"
out_file_name = "output_directory"
output_eval_file = "eval.txt"
google_test_set = "GoogleTestSet"


words_dict = {}
with open(file_name, 'r', encoding="utf-8") as in_file:
	with open(out_file_name, 'w', encoding="utf-8") as out_file:
		for line in in_file:
			the_line = line.split(" ")
			the_key = the_line[0]
			value = np.array(the_line[1:]) # getting values of the key
			words_dict[the_key] = value



def find_vector(the_file_path, should_normalize, similarity_type):
	for filename in os.listdir(google_test_set):
		for file_name in os.listdir(out_file_name):
			if filename.startswith('.') or file_name.startswith('.'):
				continue
			if not filename.endswith('.zip') and file_name.endwith(' '):
				continue
			the_file_path = os.path.join(google_test_set, filename)
			file_path = os.path.join(out_file_name, file_name)
			with open(the_file_path, 'r', encoding="utf-8") as open_file:
				with open(file_path, 'w', encoding="utf-8") as out_put_file:
					for line in open_file.readlines():
						a_line = line.split(" ")
						vec_a = words_dict[a_line[0]] # saving first word in line in word_vec_a list
						vec_b = words_dict[a_line[1]]
						vec_c = words_dict[a_line[2]]
						vec_d = words_dict[a_line[3]]
						if should_normalize == 1:
							vec_a= vec_a/np.linalg.norm(vec_a) # learned this from stuck over flow
							vec_b = vec_b/np.linalg.norm(vec_b)
							vec_c = vec_c/np.linalg.norm(vec_c)
						the_estimate = vec_c + vec_b - vec_a
						temp_smallest = 1000 #for testing
						key_curr_candidate = " "
						distance = 0
						for key in words_dict.keys():
							if similarity_type == 0:
								distance = euclidean_similarity(the_estimate, words_dict[key])
							elif similarity_type == 1:
								distance = manhattan_similarity(the_estimate, words_dict[key])
							else:
								distance = cosine_similarity(the_estimate, words_dict[key])
							if distance < temp_smallest:
								temp_smallest = distance
								key_curr_candidate = key
						out_put_file.write(a_line[0])
						out_put_file.write(a_line[1])
						out_put_file.write(a_line[2])
						out_put_file.write(key_curr_candidate)


def euclidean_similarity(vec1, vec2):
	return np.sqrt(np.sum((vec1-vec2)**2, axis=1)) #taking elements of vec 1 and cev element

def manhattan_similarity(vec1, vec2):
	return np.sqrt(np.sum(np.absolute(vec1-vec2), axis=1))  # got the formula from numoy.org and docs.scipy.org
def cosine_similarity(vec1, vec2):
	return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)) #got it from program creek
#def accuracy(vec1, vec2):


