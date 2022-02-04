import requests, re, sys, os

countries = ["argentina", "australia", "belarus", "belgium", "brazil", "canada", "czech_republic", "estonia", "finland", "france", "germany", "greece", "iraq", "ireland", "italy", "japan", "korea", "malta", "mexico", "netherlands", "paraguay", "portugal", "russia", "san_marino", "slovakia", "slovenia", "spain", "sweden", "switzerland", "turkey", "uk", "ukraine", "zz_movies", "zz_news_en", "zz_news_es"]

def download_m3u(country):
    r = requests.get("https://raw.githubusercontent.com/Free-TV/IPTV/master/" + country + ".md")
    if r.status_code == 200:
        pattern = r'\|[ ]+([0-9]+)[ ]+\|([^\|]+)+\|[\[\]>x ]+[\(]*([^ ]+)[ \|]*<img[^.]+src="([^"]+)'
        matches = re.findall(pattern, r.text)
        output = "#EXTM3U\n"

        for channel_id, channel_name, channel_url, channel_pic in matches:
            if channel_url[:-1] != "": output = output + '#EXTINF:-1 tvg-id="' + channel_name.strip() + '" tvg-chno="' + channel_id + '" tvg-logo="' + channel_pic + '",' + channel_name.strip() + "\n" + channel_url[:-1] + "\n\n"

        with open("m3u/" + country.capitalize() + ".m3u", "wb") as f: f.write(output.encode('utf-8')) 
        return country.capitalize() + ".m3u"
    else:
        print("\nCan't reach follow website to retrive URL:\n\thttps://github.com/Free-TV/IPTV/blob/master/" + country +  ".md\nCheck if you can reach it using your web browser; if it works open me a GitHub issue.\nCheers")
        return False

def single_country():
    output = "| "
    for c in countries:
        output = output + c.capitalize() + " | "
    print("Available options:\n" + output + "\n")
    country = input("> Insert country you wanna download [i.e. italy] ").lower().replace(" ", "_")
    downloaded = download_m3u(country)
    if downloaded: 
        print("\nSuccesffully downloaded m3u playlist: " + downloaded)
        exit(0)

def all_countries():
    for c in countries:
        downloaded = download_m3u(c)
        if downloaded: print("Succesffully downloaded m3u playlist: " + downloaded)
    exit(0)

def logo():
    print('''\n
    ███████╗██████╗ ███████╗███████╗██╗██████╗ ████████╗██╗   ██╗    ████████╗ ██████╗     ███╗   ███╗██████╗ ██╗   ██╗
    ██╔════╝██╔══██╗██╔════╝██╔════╝██║██╔══██╗╚══██╔══╝██║   ██║    ╚══██╔══╝██╔═══██╗    ████╗ ████║╚════██╗██║   ██║
    █████╗  ██████╔╝█████╗  █████╗  ██║██████╔╝   ██║   ██║   ██║       ██║   ██║   ██║    ██╔████╔██║ █████╔╝██║   ██║
    ██╔══╝  ██╔══██╗██╔══╝  ██╔══╝  ██║██╔═══╝    ██║   ╚██╗ ██╔╝       ██║   ██║   ██║    ██║╚██╔╝██║ ╚═══██╗██║   ██║
    ██║     ██║  ██║███████╗███████╗██║██║        ██║    ╚████╔╝        ██║   ╚██████╔╝    ██║ ╚═╝ ██║██████╔╝╚██████╔╝
    ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝        ╚═╝     ╚═══╝         ╚═╝    ╚═════╝     ╚═╝     ╚═╝╚═════╝  ╚═════╝ \n\n\t-cttynul\n''')

def menu():
    logo()
    choice = input("\t[1] Download single country playlist\n\t[2] Download all countries playlists\n\t[0] Exit\n\n> ")
    if choice == "1": single_country()
    if choice == "2": all_countries()
    else: exit(0)

if __name__ == "__main__":
    try: os.mkdir("m3u")
    except: pass

    try: arg = sys.argv[1]
    except: arg = None
    if arg == "--auto" or arg == "-a": all_countries()
    else: menu()    
