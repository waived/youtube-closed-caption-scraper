import re, os, sys
import urllib.request
import xml.etree.ElementTree as ET

def scrape(vid_id, cc):
    #closed-caption format is set for WebVVT
    
    #WebVTT is a World-Wide-Web Consortium standard for displaying timed text
    #in connection with the HTML5 <track> element.

    #Build YouTube video URL. Compatible with Youtube-Short videos
    video_url = f"https://www.youtube.com/watch?v={vid_id}"

    #Get HTML source of video
    try:
        #establish HTTP headers
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'}
        
        #send request
        req = urllib.request.Request(video_url, headers=headers)
        
        #pull response
        with urllib.request.urlopen(req) as response:
            html = response.read().decode()
            
    except Exception as ex:
        sys.exit(f'\r\nError: {ex}\r\n')

    #attempt to extract embedded caption URL
    match = re.search(r'"captions":\{"playerCaptionsTracklistRenderer":\{"captionTracks":\[(.*?)\]', html)
    
    if not match:
        print("\r\nNo closed-captions found for this video!")
    else:
        captions_data = match.group(1)
        
        match_url = re.search(r'"baseUrl":"(https://[^"]+)"', captions_data)
        
        if match_url:
            caption_url = match_url.group(1).replace('\\u0026', '&')  # Fix escaped characters
        
            #download closed-caption XML
            with urllib.request.urlopen(caption_url) as response:
                caption_xml = response.read().decode()

            #parse XML and extract raw-text
            root = ET.fromstring(caption_xml)
            transcript_text = "\n".join([line.text for line in root.findall(".//text") if line.text])

            #dump to directory
            with open(cc, "w", encoding="utf-8") as file:
                file.write(transcript_text)
                file.close()

            print(f"\r\nDownloaded @ {cc}")
        else:
            print("\r\nCould not extract embedded closed-caption URL!\r\n")
        
def main():
    #display banner    
    print('\r\n' * 20 + '''

            __   __        _        _                       
            \ \ / /__ _  _| |_ _  _| |__  ___               
             \ V / _ \ || |  _| || |  _ \/ -_)              
              |_|\___/\___|\__|\___|____/\___|              
   ___ _                _      ___           _   _          
  / __| |___ ___ ___ __| |___ / __|__ _ ____| |_(_)___ ___  
 | (__| / _ (_-</ -_) _  |___| (__/ _` |  _ \  _| / _ \   \ 
  \___|_\___/__/\___\____|    \___\__,_|  __/\__|_\___/_||_|
               ___                     |_|                  
              / __| __ ___ __ _ ____  ___ ___              
              \__ \/ _|  _/ _` |  _ \/ -_)  _|             
              |___/\__|_| \__,_|  __/\___|_|               
                               |_|         
''')

    #capture user input
    
    cc = ''
    try:
        
        vid_id = input('Video ID (ex: F2R2Xeo8HX8): ')
        
        filename = input('Output filename: ')
        
        path = input('Path to download into: ')
        
        if not os.path.exists(path):
            sys.exit('\r\nError: path does not exist!\r\n')
        else:
            cc = os.path.join(path, filename)
        
    except Exception as ex:
        sys.exit(f'\r\nError: {ex}\r\n')
    
    scrape(vid_id, cc)
    
    sys.exit('\r\nDone.\r\n')

if __name__ == '__main__':
    main()
