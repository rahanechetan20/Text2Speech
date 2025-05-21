import PyPDF2
import pyttsx3

def extract_text_from_pdf(pdf_path, start_page):
    """Extracts non-empty text from specified page to end"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        if start_page < 1 or start_page > len(reader.pages):
            raise ValueError(f"Invalid start page. PDF contains {len(reader.pages)} pages.")
        
        full_text = []

        # raw_text = reader.pages[start_page-1].extract_text()
        # cleaned_text = raw_text.strip()
        # if cleaned_text:  # Skip empty pages/whitespace
        #     full_text.append(cleaned_text)

        for page_num in range(start_page - 1, len(reader.pages)):
            raw_text = reader.pages[page_num].extract_text()
            cleaned_text = raw_text.strip()
            if cleaned_text:  # Skip empty pages/whitespace
                full_text.append(cleaned_text)
            else:
                print('Page number',page_num,'is empty')
        
        full_text = "\n".join(full_text)
        full_text = full_text.replace('\t', ' ')
        # print(full_text)
        return full_text


def read_pdf_aloud(pdf_path, start_page):
    """Main function with enhanced whitespace handling"""
    try:
        text = extract_text_from_pdf(pdf_path, start_page)
        if text:
            engine = pyttsx3.init()
            current_rate = engine.getProperty('rate')
            engine.setProperty('voice','com.apple.voice.compact.en-US.Samantha') # SIRI
            engine.setProperty('rate', current_rate - 50)
            engine.say(text)
            engine.runAndWait()
        else:
            print("No readable text found from specified page onwards")
    except Exception as e:
        print(f"Error: {str(e)}")

# Example usage:
pdf_name = ''
starting_page_number = 1
read_pdf_aloud(pdf_name, starting_page_number)
