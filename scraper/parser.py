import re
from urllib.parse import unquote, urljoin, urlsplit

from core.config import ANIME_SHIELD_URL


class AnimeParser:
    def __init__(self, base_url=ANIME_SHIELD_URL):
        self.base_url = base_url

    def parse_anime_list(self, soup):
        if not soup:
            return []

        items = []
        seen_urls = set()
        for link in soup.find_all("a", href=True):
            anime_url = self._absolute_http_url(link.get("href"))
            if not anime_url or anime_url in seen_urls:
                continue

            card = self._find_card(link)
            image = card.find("img")
            has_heading = card.select_one(
                "h1, h2, h3, h4, .film-name, .anime-title, .film-title"
            )
            has_title = any(link.get(key) for key in ("title", "data-jname", "aria-label"))
            is_series_url = "/series/" in urlsplit(anime_url).path.lower()
            if not image and not has_heading and not has_title and not is_series_url:
                continue

            title = self._title_for(link, card, image, anime_url)
            if not title:
                continue

            items.append({
                "title": title,
                "url": anime_url,
                "image": self._image_url(image, card),
            })
            seen_urls.add(anime_url)

        print(f"Parsed {len(items)} anime items.")
        return items

    def _find_card(self, link):
        for parent in [link, *list(link.parents)[:5]]:
            if parent is link and parent.find("img"):
                return parent
            classes = set(parent.get("class", []))
            card_class = bool(
                classes.intersection({"card", "anime-item", "film-item", "flw-item", "bs", "poster"})
                or any(name.startswith("anime-card") for name in classes)
            )
            if parent.name in {"article", "li"} or (card_class and parent.find("img")):
                return parent
        return link

    def _title_for(self, link, card, image, anime_url):
        title = link.get("title") or link.get("data-jname") or link.get("aria-label")
        if not title:
            heading = card.select_one(
                "h1, h2, h3, h4, .film-name, .anime-title, .film-title"
            )
            if heading:
                title = heading.get_text(" ", strip=True)
        if not title and image:
            title = image.get("alt")
        if not title:
            title = link.get_text(" ", strip=True)

        title = re.sub(r"\s+", " ", title or "").strip()
        if (
            re.fullmatch(r"(?:season|episode|ep)\s*\d+", title, re.IGNORECASE)
            or re.search(r"[\u0900-\u097F]", title)
        ):
            title = ""
        if not title or title.lower() in {"watch", "watch now", "read more", "play"}:
            slug = unquote(urlsplit(anime_url).path.rstrip("/").split("/")[-1])
            title = re.sub(r"[-_]+", " ", slug).strip().title()
        return title

    def _image_url(self, image, card):
        if image:
            for attribute in (
                "data-poster-url", "data-poster", "data-src", "data-lazy-src",
                "data-original", "data-image", "src",
            ):
                image_url = self._absolute_http_url(image.get(attribute))
                if image_url:
                    return image_url
            for attribute in ("data-srcset", "data-lazy-srcset", "srcset"):
                image_url = self._first_srcset_url(image.get(attribute))
                if image_url:
                    return image_url

        source = card.select_one("source[srcset]")
        if source:
            return self._first_srcset_url(source.get("srcset"))
        return ""

    def _first_srcset_url(self, srcset):
        if not srcset:
            return ""
        candidate = srcset.split(",", 1)[0].strip().split()
        return self._absolute_http_url(candidate[0]) if candidate else ""

    def _absolute_http_url(self, value):
        if not value:
            return ""
        value = value.strip()
        if value.startswith("data:"):
            return ""
        absolute_url = urljoin(self.base_url, value)
        if urlsplit(absolute_url).scheme not in {"http", "https"}:
            return ""
        return absolute_url