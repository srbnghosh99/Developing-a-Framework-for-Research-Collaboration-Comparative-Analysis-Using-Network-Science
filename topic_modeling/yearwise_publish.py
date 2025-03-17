import matplotlib.pyplot as plt
import pandas as pd
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import argparse

def func(inputfile):
    df = pd.read_csv(inputfile)
    timeframe = list(range(2012, 2025, 1))
    data = df[df['year'].isin(timeframe)]
    print(data.shape)
    data = df['year'].value_counts().reset_index()


    # Create DataFrame
    # data = {
    #     'year': [2021, 2020, 2019, 2024, 2023, 2022, 2018, 2017, 2016, 2015, 2013, 2014, 2012],
    #     'count': [2773, 2510, 2404, 2335, 2303, 2213, 1944, 1782, 1541, 1297, 1273, 1181, 1074]
    # }
    # df = pd.DataFrame(data)
    #
    # # Sort DataFrame by year

    data = data.sort_values(by='year')
    print(data.shape)

    print(data)


    # Plot histogram
    plt.figure(figsize=(10,6))
    plt.bar(data['year'], data['count'], color='skyblue', edgecolor='black')
    plt.xlabel('Year')
    plt.ylabel('Number of Papers')
    plt.title('Computer Vision No of Papers by Year')
    plt.xticks(data['year'], rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.savefig('figure/sw_hist.png')
    # plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description="Read File")
    parser.add_argument("--inputfile", type=str)
    # parser.add_argument("--outputfile", type=str)
    return parser.parse_args()


def main():
    inputs = parse_args()
    print(inputs.inputfile)
    print(inputs.inputfile)
    func(parse_args().inputfile)



if __name__ == '__main__':
    main()