import pickle
import os
import json

def main():
    with open('Biomaterials.pkl', 'rb') as file:
        journal = pickle.load(file)
    for article in journal['articles'][0:4]:
        for structure in article:
            print(structure, ': ', article[structure])
        print('\n\n\n')

if __name__ == '__main__':
    main()