import re
import webbrowser

from bs4 import BeautifulSoup
from bs4.formatter import HTMLFormatter

HTML_TABLE_CONTENT = '<table class="table events"><thead><tr><th scope="col">Veranstaltung</th><th scope="col">Datum</th><th scope="col">Ort</th><th scope="col">Stream</th></tr></thead><tbody>{events}</tbody></table>'
HTML_EVENT_STRING = "<tr><td>{sport}<br/>{title}</td><td>{date}</td><td>{location}</td><td>{stream}</td></tr>"
HTML_EVENT_STRING_A_TAG = '<tr><td>{sport}<br/>{title}</td><td>{date}</td><td>{location}</td><td><a href="{url}">{stream}</a></td></tr>'

def formatter(s):
    # remove whitesapce from <td> Tag
    modified_html = re.sub(r'(<td>)(\s+)', r'\1', s)
    modified_html = re.sub(r'(\s+)(</td>)', r'\2', modified_html)

     # remove whitesapce from <th> Tag
    modified_html = re.sub(r'(<th .*>)(\s+)', r'\1', modified_html)
    modified_html = re.sub(r'(\s+)(</th>)', r'\2', modified_html)

     # remove whitesapce from <a> Tag
    modified_html = re.sub(r'(<a .*>)(\s+)', r'\1', modified_html)
    modified_html = re.sub(r'(\s+)(</a>)', r'\2', modified_html)

    return modified_html

def read_text_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file.readlines():
            # Splitting each line into Title, Date, Location, Stream and URL
            if line[0] == '#' or line == '\n':
                continue
            try:
                sport, title, date, location, stream, url = map(str.strip, line.strip().split(';'))
                data.append({
                    'Sport': sport,
                    'Title': title,
                    'Date': date,
                    'Location': location,
                    'Stream': stream,
                    'URL': url
                    }
                )
                print(f'Sport: {sport}, Title: {title}, Date: {date}, Location: {location}, Stream: {stream}, URL: {url}')
            except ValueError:
                sport, title, date, location, stream = map(str.strip, line.strip().split(';'))
                data.append({
                    'Sport': sport,
                    'Title': title,
                    'Date': date,
                    'Location': location,
                    'Stream': stream
                    }
                )
                print(f'Sport: {sport}, Title: {title}, Date: {date}, Location: {location}, Stream: {stream}')
            
    
    return data

def data_to_html(data_list):
    html_string = ""
    for event in data_list:
        if event["Stream"] == "TBD":
            html_string = html_string + HTML_EVENT_STRING.format(
                sport=event["Sport"],
                title=event["Title"],
                date=event["Date"],
                location=event["Location"],
                stream=event["Stream"],
            )
        else:
            html_string = html_string + HTML_EVENT_STRING_A_TAG.format(
                sport=event["Sport"],
                title=event["Title"],
                date=event["Date"],
                location=event["Location"],
                stream=event["Stream"],
                url=event["URL"],
            )

        
    return HTML_TABLE_CONTENT.format(events=html_string)

def is_valid_and_format(html_string):
    soup = BeautifulSoup(html_string, "html.parser")
    if html_string == str(soup):
        return soup.prettify(formatter="html")
    else:
        return False

def update_events(input_file, new_events):
    with open(input_file, 'r+') as file:
        old_content = file.read()
        soup = BeautifulSoup(old_content, "html.parser")
        soup.table.replace_with(BeautifulSoup(new_events, "html.parser"))

        a = formatter(soup.prettify())

        file.seek(0) 
        file.truncate()
        file.write(a)

    
if __name__ == "__main__":
    file_path = "scripts/events.txt"  
    new_event_data = read_text_file(file_path)
    html_new_event_data = data_to_html(new_event_data)
    valid_html = is_valid_and_format(html_new_event_data)

    if not valid_html:
        print("No valid HTML!")
        exit(1)

    update_events("events.html", valid_html)

    webbrowser.open("events.html")


    


