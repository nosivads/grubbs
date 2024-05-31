import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

from pathlib import Path

physical_df = pd.read_pickle('Extracted-Text-from-Photographs_vectors.pickle')
digital_df = pd.read_pickle('desktop_grubbs_assistant_vectors.pickle')
most_similar_df = pd.DataFrame(columns=['folder', 'filename', 
                                        'cosine similarity', 'sim_folder', 'sim_filename', 
                                        'euclidean distance', 'dist_folder', 'dist_filename'])

for i in range(len(physical_df)):

    #physical_df.loc[i, "folder"], physical_df.loc[i, "filename"], physical_df.loc[i, "embedding"]
    #digital_df.loc[j, "folder"], digital_df.loc[j, "filename"], digital_df.loc[j, "embedding"]

    cos_sim, euc_dis, sim_pos, dis_pos = 0, 1000, 0, 0
    sim_fold, sim_file, dis_fold, dis_file  = '', '', '', ''

    for j in range(len(digital_df)):

        similarity = cosine_similarity(np.array(physical_df.loc[i, "embedding"]).reshape(1, -1), 
                                       np.array(digital_df.loc[j, "embedding"]).reshape(1, -1))[0][0]
        
        if similarity > cos_sim:
            cos_sim = similarity
            sim_fold = digital_df.loc[j, "folder"]
            sim_file = digital_df.loc[j, "filename"]

        distance = euclidean_distances(np.array(physical_df.loc[i, "embedding"]).reshape(1, -1), 
                                       np.array(digital_df.loc[j, "embedding"]).reshape(1, -1))[0][0]
        
        if distance < euc_dis:
            euc_dis = distance
            dis_fold = digital_df.loc[j, "folder"]
            dis_file = digital_df.loc[j, "filename"]

        print(i, j)
    
    most_similar_df.loc[len(most_similar_df.index)] = [physical_df.loc[i, "folder"],
                                                       physical_df.loc[i, "filename"],
                                                       cos_sim,
                                                       sim_fold,
                                                       sim_file,
                                                       euc_dis,
                                                       dis_fold,
                                                       dis_file] 
    
most_similar_df.to_csv('most_similar.csv')
most_similar_df.to_pickle('most_similar.pickle')
     





