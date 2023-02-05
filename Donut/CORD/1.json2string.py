# convert json to single line string from all the folders where json is present

import os
import json
import glob
import argparse

def json2string(dir_path):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.json'):
                with open(os.path.join(root, file), 'r') as f:
                    # print the name of the file
                    print(file)
                    data = json.load(f)
                    data = json.dumps(data)
                    
                    # add double quotes to the string
                    data = '"' + data + '"'
                    print(data[:5])

                    # write to file
                    with open(os.path.join(root, file), 'w') as f:
                        f.write(data)

            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir_path', type=str, default='.', help='Directory path')
    args = parser.parse_args()
    json2string(args.dir_path)
