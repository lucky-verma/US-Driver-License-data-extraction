# read all txt files and save them in a metadata.jsonl file

import os
import glob
import argparse
import json

def readTxt(dir_path):
    # read all txt files
    for file in glob.glob(dir_path + '/*.json'):
        # read jsonl file
        with open(file, 'r') as f:
            # print the name of the file
            print(file)
            # read the lines
            lines = f.readlines()
            # create a dictionary
            metadata = {}
            # add the name of the file
            metadata["file_name"] = file.split("/")[-1].split('json')[1][1:-1] + '.jpg'
            # add the text
            metadata['ground_truth'] = lines[0].strip()

            print(metadata)

            # append the metadata to the metadata.jsonl file on the directory
            with open(os.path.join(dir_path, 'metadata.jsonl'), 'a') as f:
                f.write(json.dumps(metadata) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', type=str, default='data')
    args = parser.parse_args()
    readTxt(args.dir_path)
