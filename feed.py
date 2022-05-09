from typing import Iterator, Tuple
import feedparser
from ad import AdPreview


class Feed:
    def load_ads(self) -> Iterator[Tuple[AdPreview, Tuple[float, float]]]:
        d = feedparser.parse('https://www.kijiji.ca/rss-srp-apartments-condos/ville-de-montreal/'
                             '2+bedroom+den__2+bedrooms__3+bedroom+den__3+bedrooms__4+bedrooms/'
                             'c37l1700281a27949001?radius=9.0&ad=offering&price=800__1900'
                             '&minNumberOfImages=1&address=Montreal%2C+QC+H2T+2T1'
                             '&ll=45.518721,-73.587508&furnished=0&siteLocale=en_CA')

        for item in d['items']:
            yield AdPreview(item['link']), (item['geo_lat'], item['geo_long'])


'''
<item>
<title>...</title>
<link>https://www.kijiji.ca/v-appartement-condo/...</link>
<description>...</description>
<enclosure url="..." length="14" type="image/jpeg"/>
<pubDate>Sun, 01 May 2022 03:56:30 GMT</pubDate>
<guid>https://www.kijiji.ca/v-appartement-condo/...</guid>
<dc:date>2022-05-01T03:56:30Z</dc:date>
<geo:lat>44.5555</geo:lat>
<geo:long>-77.11111</geo:long>
<g-core:price>1000.0</g-core:price>
</item>
'''
