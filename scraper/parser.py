class AnimeParser:
    def __init__(self):
        print("Anime Parser initialized: Ready to extract content!")

    def parse_anime_list(self, soup):
        anime_items = []
        if not soup:
            return anime_items

        try:
            # animesalt.cx के हिसाब से सभी लिंक्स और कार्ड्स को टारगेट करते हैं
            links = soup.find_all("a", href=True)
            for link in links:
                title = link.get_text(strip=True)
                href = link['href']
                # अगर सही नाम और लिंक मिल रहा है तो लिस्ट में जोड़ लेंगे
                if title and len(title) > 2 and not href.startswith('#') and not href.startswith('javascript'):
                    anime_items.append({"title": title, "url": href})

            # डुप्लीकेट (Duplicate) डेटा हटाने के लिए
            seen = set()
            unique_items = []
            for item in anime_items:
                if item['url'] not in seen:
                    seen.add(item['url'])
                    unique_items.append(item)

            print(f"✅ Successfully parsed {len(unique_items)} anime items.")
            return unique_items
        except Exception as e:
            print(f"❌ Error during parsing: {e}")
            return anime_items

print("Parser script ready!")