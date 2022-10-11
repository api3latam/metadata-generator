import json
import os
import copy
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Initialize minting script')
    parser.add_argument('--file', '-f', type=str, default='standard.json',
                        help='Provide the specific file from base folder \
                            that you\'ll like to be processed.')
    parser.add_argument('--number', '-n', type=int, default=10, \
                        help="Provide the total number of files to produce.")
    parser.add_argument('--network', '-w', type=str, \
                        help="Provide the network name for the metadata.")
    
    args = parser.parse_args()

    base_route = os.getcwd()
    dest_file = args.file
    file_route = f'{base_route}/base/{dest_file}'

    with open(file_route) as f:
        data = json.load(f)

    range_init = [i for i in data['attributes'] 
        if i['trait_type'] == 'choice'][0]['value']
    init = int(range_init.split('#')[-1])

    data['attributes'] = [i for i in data['attributes']
        if i['trait_type'] not in ['chain', 'choice']]
    data['attributes'].append({'trait_type': 'chain', 
        'value': args.network})
    
    print(f"Baseline template: {data}\n")
    
    for i in range(init, init+args.number):
        temp = copy.deepcopy(data)
        temp['name'] = f"{temp['name']} #{i}"
        temp['attributes']\
                .append({'trait_type': 'choice',
                    'value': f'#{i}'})

        print(f'Writting file #{i}\n')
        with open(f'{base_route}/metadata/{i}', 'w+') as w:
            json.dump(temp, w)
    
    print("Done writting files!\n")
