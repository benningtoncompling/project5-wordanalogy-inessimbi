#!/usr/bin/python3
#
# word_analogy.py - building word analogy solver
# Author: <Ines Simbi>(inessimbi@bennington.edu)
# Date: <05.05.2019>

import sys, os
import numpy as np

file_name = sys.argv[1]
google_test_set = sys.argv[2]
out_file_name = sys.argv[3]
outfile_eval_file = sys.argv[4]
should_normalize = int(sys.argv[5])
similarity = int(sys.argv[6])
#file_name = "smaller_model.txt"
#out_file_name = "output_directory"
#outfile_eval_file = "output_eval.txt"
#google_test_set = "GoogleTestSet"


words_dict = {}
with open(file_name, 'r', encoding="utf-8") as in_file:
	for line in in_file:
		the_line = line.split(" ")
		the_key = the_line[0]
		value = np.array(the_line[1:], dtype=float) # getting values of the key
		words_dict[the_key] = value

def euclidean_similarity(vec1, vec2):
	return np.sqrt(np.sum((vec1-vec2)**2)) #taking elements of vec 1 and vec2

def manhattan_similarity(vec1, vec2):
	return np.sum(np.absolute(vec1-vec2))  # got the formula from numpy.org and docs.scipy.org

def cosine_similarity(vec1, vec2):
	return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)) #got it from program creek


def find_vector(should_normalize, similarity_type):
	with open(outfile_eval_file, 'w', encoding="utf-8") as output_eval_file:
		match_counter = 0
		negative_match_counter = 0
		for filename in os.listdir(google_test_set):
			if filename.startswith('.'):
				continue
			if not filename.endswith('.txt'):
				continue
			the_file_path = os.path.join(google_test_set, filename)
			file_path = os.path.join(out_file_name, filename)
			with open(the_file_path, 'r', encoding="utf-8") as open_file:
				with open(file_path, 'w', encoding="utf-8") as out_put_file:
					for line in open_file.readlines():
						a_line = line.split(" ")
						if a_line[0] not in words_dict:
							negative_match_counter +=1
							continue
						vec_a = words_dict[a_line[0]] # saving first word in line in word_vec_a list
						if a_line[1] not in words_dict:
							negative_match_counter +=1
							continue
						vec_b = words_dict[a_line[1]]
						if a_line[2] not in words_dict:
							negative_match_counter +=1
							continue
						vec_c = words_dict[a_line[2]]
						#vec_d = words_dict[a_line[3]]
						if should_normalize == 1:
							vec_a= vec_a/np.linalg.norm(vec_a) # learned this from stuck over flow
							vec_b = vec_b/np.linalg.norm(vec_b)
							vec_c = vec_c/np.linalg.norm(vec_c)
						the_estimate = vec_c + vec_b - vec_a
						temp_smallest = 1000 #for testing
						temp_max = -10000000000
						key_curr_candidate = " "
						distance = 0
						for key in words_dict.keys():
							if similarity_type == 0:
								distance = euclidean_similarity(the_estimate, words_dict[key])
							elif similarity_type == 1:
								distance = manhattan_similarity(the_estimate, words_dict[key])
							else:
								distance = cosine_similarity(the_estimate, words_dict[key])
							if distance < temp_smallest and similarity_type < 2:
								temp_smallest = distance
								key_curr_candidate = key
							if distance > temp_max and similarity_type == 2:
								temp_max = distance
								key_curr_candidate = key
						out_put_file.write(a_line[0] + " ")
						out_put_file.write(a_line[1] + " ")
						out_put_file.write(a_line[2] + " ")
						out_put_file.write(key_curr_candidate+ " "+ "\n")

						if key_curr_candidate == a_line[3]:
							match_counter += 1
						else:
							negative_match_counter += 1

			sum = match_counter + negative_match_counter
			accuracy_checker_correct = match_counter/sum
			#print("(", str(match_counter), "/", str(sum))
			output_eval_file.write(filename + "/n")
			output_eval_file.write(str(accuracy_checker_correct) + "%" + " " + "(" + str(match_counter) + "/" + str(sum) + ")" + "\n")

find_vector(should_normalize, similarity)




