from Helper import *
from Spider import *
import argparse
import json
"""parsing and configuration"""
def parse_args():
    desc = "China region hirearchical-Info"
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--results_path', type=str, default='results.json',
                        help='The path of the txt file which stores the results', required=False)

    return parser.parse_args()

def main():
     # parse arguments
    args = parse_args()
    if args is None:
      exit()

    resultsFilePath = args.results_path
    #resultsFile = open(resultsFilePath, 'w')

    regionUrl = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/index.html"
    regionUrlStarter = "http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2016/"
    spider = Spider(regionUrl, regionUrlStarter)
    spider.processData()
    print(spider.provinceList)
    province_dict = spider.provinceList[0]

    with open(resultsFilePath,"w") as f:
        json.dump(province_dict,f,ensure_ascii = False)
        print("加载入文件完成...")

if __name__ == '__main__':
    main()