import pandas as pd
from bertopic import BERTopic
import argparse
import sys
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
import random
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from hdbscan import HDBSCAN
from transformers import RobertaTokenizer, RobertaModel
import torch
from hdbscan import HDBSCAN
from umap import UMAP
from bertopic.representation import KeyBERTInspired
from bertopic.vectorizers import ClassTfidfTransformer
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import preprocess


# Load RoBERTa tokenizer & model
# tokenizer = RobertaTokenizer.from_pretrained('roberta-base')
# model = RobertaModel.from_pretrained('roberta-base')

# Function to get sentence embeddings
def get_roberta_embeddings(texts):
    encoded_input = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    # Use mean pooling to get sentence embeddings
    sentence_embeddings = model_output.last_hidden_state.mean(dim=1)
    return sentence_embeddings.numpy()


def topic_modeling(filename,outputfile):
    # Set random seeds
    # random.seed(41)
    # np.random.seed(41)
    # torch.manual_seed(41)

    # df = pd.read_csv(filename)
    # print(df.shape)
    # df = df[df['booktitle'] == 'ICSE']
    # print(df)
    # yearrange = list(range(2012, 2026, 1)) #[2000 to 2025]
    # df = df[df['year'].isin(yearrange)]
    df = preprocess.title_preprocess(filename)
    df['preprocessed_title']=df['preprocessed_title'].fillna("")
    titles = df.title.tolist()
    yearlist = df.year.tolist()
    preprocessed_titles = df.preprocessed_title.tolist()
    # preprocessed_titles = [preprocess_title(title) for title in titles]
    # print(preprocessed_titles)
    print(df.shape)
    '''
    vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english")
    # embedding_model = SentenceTransformer("paraphrase-mpnet-base-v2")
    # umap_model = UMAP(n_neighbors=5, n_components=5, min_dist=0.05, metric='cosine',random_state= 42)
    umap_model = UMAP(n_neighbors=5, n_components=5, min_dist=0.05, metric='cosine',random_state= 40)
    hdbscan_model = HDBSCAN(min_cluster_size=40, metric='euclidean', cluster_selection_method='eom',prediction_data=True)
    representation_model = KeyBERTInspired()
    sentence_model = SentenceTransformer("all-mpnet-base-v2")
    # sentence_model = SentenceTransformer("paraphrase-mpnet-base-v2")
    # Step 5 - Create topic representation
    ctfidf_model = ClassTfidfTransformer()

    
    
    # model = BERTopic(
    #     embedding_model=sentence_model,
    #     vectorizer_model=vectorizer_model,
    #     top_n_words=10,
    #     language='english', calculate_probabilities=True,
    #     verbose=True
    # )
    model = BERTopic(
        embedding_model=sentence_model,          # Step 1 - Extract embeddings
        umap_model=umap_model,                    # Step 2 - Reduce dimensionality
        hdbscan_model=hdbscan_model,              # Step 3 - Cluster reduced embeddings
        vectorizer_model=vectorizer_model,        # Step 4 - Tokenize topics
        ctfidf_model=ctfidf_model,                # Step 5 - Extract topic words
        representation_model=representation_model # Step 6 - (Optional) Fine-tune topic representations
    )
    '''
    # model.save("bertopic_model")
    model = BERTopic.load("/Users/shrabanighosh/UNCC/Spring_2025/plos_complex/dynamic_analysis/topic_modeling/bertopic_model")

    topics, probs = model.fit_transform(preprocessed_titles)
    timestamps = df.data.tolist()
 
    info_df = model.get_topic_info()
    print(info_df)
    info_df['Percentage'] = info_df['Count']*100/info_df['Count'].sum()
    info_df['Percentage'] = info_df['Percentage'].round(2)
    info_df = info_df[['Topic', 'Count', 'Name', 'Percentage','Representation','Representative_Docs']]
    info_df.to_csv(outputfile)
    print(info_df['Count'].sum(),df.shape)
    new_df = pd.DataFrame({
            'title':titles,
            'title_topic': topics,
            'year': yearlist
            # 'title_prob': title_prob,
        })
    new_df.to_csv('sw2.csv')
    htmlfile = model.visualize_barchart()
    htmlfile.write_html("topics_barchart.html")

    # spare_docs = new_df[new_df['title_topic'] == -1]['title'].tolist()

    # topics, probs = model.fit_transform(spare_docs)
    # print(model.get_topic_info())
    # info_df = model.get_topic_info()
    # info_df.to_csv('test3.csv')
    # new_df = pd.DataFrame({
    #         'title':spare_docs,
    #         'title_topic': topics,
    #         # 'title_prob': title_prob,
    #     })
    # new_df.to_csv('test4.csv')
    

    

    # topics_over_time = model.topics_over_time(docs, timestamps, nr_bins=20)
    # # model.visualize_topics_over_time(topics_over_time, topics=[9, 10, 72, 83, 87, 91])
    # # htmlfile = model.visualize_topics_over_time(topics_over_time, topics=[9, 10, 72, 83, 87, 91])
    # htmlfile = model.visualize_topics_over_time(topics_over_time, top_n_topics=30)

    # htmlfile.write_html("topics_over_time.html")



    # top = pd.DataFrame({'Topic Lable':tweet_topic,
    #     'Prob':prob})

    # top.to_csv('tweet_topic_with_prob_10.csv')
    # df1 = df.drop_duplicates(subset=['clean_tweet'])
    # #tweet_topic_df = pd.DataFrame(topics)
    # #tweet_topic_df.to_csv("topics_df_10.csv")
    # df_time = df[['created_at', 'text','clean_tweet']]
    # df_time.drop_duplicates(subset='clean_tweet').reser_index()
    # timestamps = df_time.created_at.to_list()
    # tweets = df_time.clean_tweet.to_list()
    # topics_over_time = model.topics_over_time(tweets, topics, timestamps, nr_bins=20)

    # fig = model.visualize_topics_over_time(topics_over_time)
    # fig.write_html("topics_over_time.html")

    # print(top.shape)
    # print(info_df.shape)
    # results = pd.DataFrame({"Doc": docs, "Topic": topics})
    # results.to_csv("docs_vs_topic.csv")
    print("execution ended")


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputfile",type = str)
    parser.add_argument("--outputfile", type=str)
    return parser.parse_args()

def main():
    inputs=parse_args()
    print(inputs.inputfile)
    print(inputs.outputfile)
    topic_modeling(inputs.inputfile,inputs.outputfile)

    

  

if __name__ == '__main__':
    main()



# /Users/shrabanighosh/UNCC/Spring\ 2025/plos\ complex/csvfiles/dblp_hpc_filtered_22.csv

    # sentence_model = SentenceTransformer("intfloat/e5-large-v2")
    # sentence_model = SentenceTransformer("nomic-ai/nomic-embed-text-v1", trust_remote_code=True)
    # model = BERTopic(embedding_model=sentence_model, hdbscan_model=hdbscan_model)
    # Create BERTopic model
    
    # model = BERTopic(low_memory=True)

# Train model

    # topics, probs = model.fit_transform(docs, embeddings)    
    # model = BERTopic(language="english", calculate_probabilities=True, verbose=True)
    #model = BERTopic.load("model_full")
    # model = BERTopic(verbose=True)

       # tweet_topic =[]
    # prob = []
    # for x in probs:
    #   y = x.tolist()
    #   max_index = y.index(max(y))
    #   tweet_topic.append(max_index)
    #   prob.append(max(y))
    # # print(topics)
    # for idx, x in enumerate(topics):
    #   prob.append(probs[idx][x])
        

    #model.save("model_full1")
    #model = BERTopic.load("model_full")