import nltk 
from nltk import FreqDist
import matplotlib
import string

exclude = set(string.punctuation)

with open("YT_Comment_Output.txt", "rb") as f:
	lines = [line.rstrip() for line in f]
	splits = [line.split() for line in lines]
	some_upper = [item for sublist in splits for item in sublist]
	#replace BOM w known stopword
	BOM_gone = [word.replace('\xef\xbb\xbf', 'i') for word in some_upper]
	punct_gone = []
	for word in BOM_gone: 		
		punct_gone.append(''.join(ch for ch in word if ch not in exclude))
	YT_comment_words = [word.lower() for word in punct_gone]

with open('stopwords.txt', 'rb') as f:
    stopwords = [line.rstrip() for line in f]

print YT_comment_words[:10]
print stopwords[:10]

filtered_words = [w for w in YT_comment_words if not w in stopwords]

print filtered_words[:10]

fd = FreqDist(filtered_words)
print fd.values()[:10]
print fd
fd.plot(30)
