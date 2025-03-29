import re, sys, os

if len(sys.argv) != 3:
    sys.exit(f'\r\nSyntax: python3 {sys.argv[0]} <caption-file> <output-file>\r\n')

if not os.path.exists(sys.argv[1]):
    sys.exit('\r\nError! Caption file not found!\r\n')
else:
    try:
        with open(sys.argv[1], 'r', encoding='utf-8') as file:
            #convert text to lowercase
            text = file.read().lower()

            file.close()

        #remove all line-breaks and extra spaces
        text = re.sub(r'\s+', ' ', text).strip()

        #capitalize the first letter of each sentence
        sentences = re.split(r'(?<=[.!?]) +', text)  #split using punctuation as sentence boundaries
        processed_text = ' '.join(sentence.capitalize() for sentence in sentences)

        with open(sys.argv[2], 'w', encoding='utf-8') as output_file:
            output_file.write(processed_text)
            output_file.close()

        print(f"\r\nDone! Reformated: sys.argv[1]\r\n")
    
    except FileNotFoundError:
        print("\r\nError: File not found! Please check the file path and try again.\r\n")
    except Exception as e:
        print(f"\r\nError: {e}\r\n")
