class AnimeParser:
    def __init__(self):
        print("Anime Parser initialized: Ready to extract content!")

    def parse_anime_list(self, soup):
        anime_items = []
        if not soup:
            return anime_items

        try:
            # वेबसाइट के कार्ड्स या लिंक्स को टारगेट करते हैं
            cards = soup.find_all(['a', 'div'], class_=True)
            for card in cards:
                title_elem = card.find("h3") or card.find("h4") or card.find("span")
                link_elem = card if card.name == 'a' else card.find("a", href=True)
                img_elem = card.find("img")

                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    href = link_elem.get('href', '#')
                    img_url = img_elem.get('src') or img_elem.get('data-src') if img_elem else ""

                    if title and len(title) > 2 and not href.startswith('#'):
                        anime_items.append({
                            "title": title, 
                            "url": href,
                            "image": img_url
                        })

            # डुप्लीकेट डेटा हटाने के लिए
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