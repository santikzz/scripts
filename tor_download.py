import os
from requests_tor import RequestsTor
import sys

def format_file_size(size_in_bytes):
    KB = 1024
    MB = 1024 * KB
    GB = 1024 * MB
    if size_in_bytes < KB:
        return f"{size_in_bytes} bytes"
    elif size_in_bytes < MB:
        return f"{size_in_bytes / KB:.2f} KB"
    elif size_in_bytes < GB:
        return f"{size_in_bytes / MB:.2f} MB"
    else:
        return f"{size_in_bytes / GB:.2f} GB"

def download_file(url, chunk_size=1024):
    
    # connect to tor
    print('[+] Connecting to tor relays...')
    rt = RequestsTor()

    filename = os.path.basename(url)
    
    while True:

        if os.path.exists(filename):
            # if the file already exists, get the file size
            print(f'[+] Resuming download of \'{filename}\' ...')
            file_size = os.path.getsize(filename)
            headers = {'Range': f'bytes={file_size}-'}
            mode = 'ab'
            downloaded = file_size

        else:
            # if the file does not exist, start from the beginning
            print(f'[+] Downloading \'{filename}\' ...')
            headers = {}
            mode = 'wb'
            downloaded = 0

        with open(filename, mode) as f:
            
            response = rt.get(url, headers=headers, stream=True)
            total_size = int(response.headers.get('content-length', 0))
                    
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    progress = (downloaded / total_size) * 100
                    print(f"\rDownloading \'{filename}\' -> {progress:.2f}% ({format_file_size(downloaded)} / {format_file_size(total_size)})", end='', flush=True)

        if (response.status_code == 200 and downloaded == total_size):
            print("\n[+] Download completed successfully!")
            break
        else:
            print(f"\nServer responded with error {response.status_code}, retrying...\n")


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print(f'[!] Usuage: python {sys.argv[0]} https://example.onion/myfile.pdf')
        input()
        exit()

    url = sys.argv[1]
    download_file(url)

    input()
    exit()
    
    # TODO: multithreaded download manager to download multiple files concurrently