import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SIMANWSpider(CrawlSpider):
    name = "simanw_noticias"

    allowed_domains = ["portal-noticias.com"]
    start_urls = ["https://portal-noticias.com/noticias/"]

    rules = (
        Rule(
            LinkExtractor(allow=r"/noticias/"),
            callback="parse_noticia",
            follow=True
        ),
    )

    custom_settings = {
        "DOWNLOAD_DELAY": 2,
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": 4,
        "FEED_FORMAT": "json",
        "FEED_URI": "noticias_simanw.json",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    def parse_noticia(self, response):
        for articulo in response.css("article.noticia"):
            yield {
                "titulo": articulo.css("h2::text").get(),
                "cuerpo": articulo.css("p.cuerpo::text").get(),
                "fecha": articulo.css("span.fecha::text").get(),
                "autor": articulo.css("span.autor::text").get(),
                "categoria": articulo.attrib.get("data-categoria"),
                "url": response.url,
            }