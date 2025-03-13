#!/usr/bin/env python
import os
import csv
import xmltodict 
import argparse
import sys
import pandas as pd
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from tqdm import tqdm  


def parse_dblp(inputpath,outputpath):

#  inputpath = "/content/sample_data/files"
  dir_list = os.listdir(inputpath)
  for filename in dir_list:
    if (filename.endswith(".xml") == False):
      continue
    else:
      print(filename)
      filen = inputpath +'/' + filename
      with open(filen, 'r') as file:
        filedata = file.read()
        data_dict = xmltodict.parse(filedata)
        keysList = list(data_dict['dblp']['inproceedings'])
        print(len(keysList))

        orcidid = []
        orcidname = []
        orcidbooktitle = []

        mdate = []
        name = []
        orcid = []
        title = []
        crossref = []
        pages = []
        year = []
        key = []
        ee = []
        url = []
        date = []
        booktitle = []
        # data = []
        for index in tqdm(range(len(keysList))):
            flag = 0
            authors_name = []
            authors_orcid = []
            if 'author' in keysList[index]:
                authorlist = keysList[index]['author']
                
                if type(authorlist) is list:   
                    for authors in authorlist:
                        if isinstance(authors, dict):  # Check if the item is a dictionary
                                authors_name.append(authors['#text'])  # Append the value of '#text' key
                                flag = 1
                                authors_orcid.append(authors['@orcid'])
                                orcidid.append(authors['@orcid'])
                                orcidname.append(authors['#text'])
                                orcidbooktitle.append(keysList[index]['booktitle']) if 'booktitle' in keysList[index] else orcidbooktitle.append('')

                        else:
<<<<<<< HEAD
                                authors_name.append(authors) 
                                authors_orcid.append('')
=======
                                authors_name.append(authors)
                                authors_orcid.append('DA')
>>>>>>> 3d8b4f1f7e2c0534fe3c804db44e08d000e7466b
                else:
                    if isinstance(authorlist, dict):
                        authors_name.append(authorlist['#text'])
                        flag = 1
                        authors_orcid.append(authorlist['@orcid'])
                        orcidid.append(authorlist['@orcid'])
                        orcidname.append(authorlist['#text'])
                        orcidbooktitle.append(keysList[index]['booktitle']) if 'booktitle' in keysList[index] else orcidbooktitle.append('')
                    else:    
                        authors_name.append(authorlist)
<<<<<<< HEAD
                        authors_orcid.append('')
=======
                        authors_orcid.append('DA')
>>>>>>> 3d8b4f1f7e2c0534fe3c804db44e08d000e7466b
                        #print('authors',authors_name)
            else:
                #print(index)
                authors_name.append('')
                authors_orcid.append('')
                #print('authors',authors_name)
            name.append(authors_name)
            orcid.append(authors_orcid)
<<<<<<< HEAD
            print(len(name),len(orcid))
=======
>>>>>>> 3d8b4f1f7e2c0534fe3c804db44e08d000e7466b
            title.append(keysList[index]['title']) if 'title' in keysList[index] else title.append('')
            #venue.append(keysList[index]['info']['venue']) if 'venue' in keysList[index] else venue.append('')
            pages.append(keysList[index]['pages']) if 'pages' in keysList[index] else pages.append('')
            year.append(keysList[index]['year']) if 'year' in keysList[index] else year.append('')
            date.append(keysList[index]['@mdate']) if '@mdate' in keysList[index] else date.append('')
            #access.append(keysList[index]['info']['access']) if 'access' in keysList[index] else access.append('')
            key.append(keysList[index]['@key']) if '@key' in keysList[index] else key.append('')
            #doi.append(keysList[index]['info']['doi']) if 'doi' in keysList[index] else doi.append('')
            ee.append(keysList[index]['ee']) if 'ee' in keysList[index] else ee.append('')
            url.append(keysList[index]['url']) if 'url' in keysList[index] else url.append('')
            booktitle.append(keysList[index]['booktitle']) if 'booktitle' in keysList[index] else booktitle.append('')
            crossref.append(keysList[index]['crossref']) if 'crossref' in keysList[index] else crossref.append('')
            #if flag == 1:
             #   orcidname.append(keysList[index]['booktitle']) if 'booktitle' in keysList[index] else .append('')
                #orcidbooktitle.append(keysList[index]['booktitle']) if 'booktitle' in keysList[index] else orcidbooktitle.append('')

        new_file_name = filename.replace('.xml', '.csv') 
        new_file_name = outputpath + '/' +  new_file_name
        print(new_file_name) 
        # df = pd.DataFrame({'score':score, 'id':id, 'authors_pid': pid,'authors_name':name, 'title':title, 'venue':venue, 'pages': pages, 'year':year, 'type':typ, 'access':access, 'key':key, 'doi':doi, 'ee':ee, 'url':url})
<<<<<<< HEAD
        df = pd.DataFrame({'authors_name':name,'authors_orcid':orcid ,'title':title,'pages': pages, 'year':year,'data':date,'key':key,'ee':ee, 'url':url,'booktitle':booktitle,'crossref':crossref})
        df2 = pd.DataFrame({'orcid':orcidid,'authors_name':orcidname, 'title':orcidbooktitle})
        df.to_csv(new_file_name)
        # df2.to_csv('orcid_name_id.csv')
=======
        df = pd.DataFrame({'authors_name':name,'authors_orcid':orcid,'title':title,'pages': pages, 'year':year,'data':date,'key':key,'ee':ee, 'url':url,'booktitle':booktitle,'crossref':crossref})
        df2 = pd.DataFrame({'orcid':orcidid,'authors_name':orcidname,'booktitle':orcidbooktitle})
        df.to_csv(new_file_name)
        #df2.to_csv('orcid_name_id.csv')
>>>>>>> 3d8b4f1f7e2c0534fe3c804db44e08d000e7466b


def parse_args():
   
    parser = argparse.ArgumentParser(description="Read File")

    parser.add_argument("--inputdirectory",type = str)
    parser.add_argument("--outputdirectory",type = str)
    
    return parser.parse_args()

def main():
    inputs=parse_args()
    print(inputs.inputdirectory)
    print(inputs.outputdirectory)
    parse_dblp(inputs.inputdirectory,inputs.outputdirectory)
  

if __name__ == '__main__':
    main()
