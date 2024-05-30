from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
X = np.array([1,2])
Y = np.array([2,2])
Z = np.array([2,4])

# calculate cosine similarity between [X] and [Y,Z]
# sending input as arrays would allow for calculating both cosine_sim(X,Y) and cosine_sim (X,Y)
cos_sim = cosine_similarity([X], [Y, Z])
print(cos_sim)

# calculate the entire cosine similarity matrix among X, Y, and Z
cos_sim = cosine_similarity([X, Y, Z])
print(cos_sim)
print()