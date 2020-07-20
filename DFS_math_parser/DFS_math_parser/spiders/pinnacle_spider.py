import json

import scrapy

from ..items import TeamLineItem


class TeamLineSpider(scrapy.Spider):
    """
    Spider which crawl for match-up pages and
    extract 'Teams' lines data.
    """
    name = 'teamlines'

    start_urls = ['https://www.qpk30mol.website/en/esports/matchups/highlights']

    headers = {
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://www.qpk30mol.website",
        "pragma": "no-cache",
        "referer": "https://www.qpk30mol.website/en/esports/matchups/highlights",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "x-api-key": "CmX2KcMrXuFmNg6YFbmTxE0y9CIrOi0R",
        "x-device-uuid": "2da38900-0f6d8ef4-487db364-51843a47",
    }

    def parse(self, response):
        """
        Method start first request to get event list data and
        pass it to parse_events_id() method
        """
        url = 'https://guest.api.arcadia.qpk30mol.website/0.1/sports/12/matchups/highlighted'

        request = scrapy.Request(
            url,
            callback=self.parse_events_id,
            headers=self.headers
        )

        yield request

    def parse_events_id(self, response):
        """
        Method collect and filter list of events id and forms
        links to pass it to parse_odd_names()
        """
        event_id_set = set()
        json_event_list = json.loads(response.body)

        for event in json_event_list:
            title = event['league']['name']

            # Checks that event id not duplicate and events is CS:GO match
            if event['id'] not in event_id_set and 'CS:GO' in title:
                event_id = event['id']

                # Links for two XHR data jsons, constructs with event id
                info_url = f'https://guest.api.arcadia.qpk30mol.website/0.1/matchups/{event_id}/related'
                values_url = f'https://guest.api.arcadia.qpk30mol.website/0.1/matchups/{event_id}/markets/related/straight'

                # Request for first XHR with headers and additional metadata
                # which will be passed to the parse_odds_info()
                request = scrapy.Request(
                    info_url,
                    callback=self.parse_odds_info,
                    headers=self.headers,
                    # This metadata passes to next method
                    meta={'values_url': values_url}
                )
                event_id_set.add(event_id)

                yield request

    def parse_odds_info(self, response):
        """
        Method filter odds to get only 'Teams' lines and then
        create a dict with base event data stored by map number
        """
        data_by_map = {}
        values_url = response.meta['values_url']
        odd_info_list = json.loads(response.body)

        # Delete blocks without 'Teams' category and 'special' field
        for info_block in odd_info_list[1:]:
            category = info_block['special']['category']
            if 'special' not in info_block or category != 'Teams':
                odd_info_list.remove(info_block)

        # Forms dict and fill in with title event data by map number
        for period in odd_info_list[0]['periods']:
            group = odd_info_list[0]['league']['group']
            name = odd_info_list[0]['league']['name']
            start_time = odd_info_list[0]['startTime']

            # Add only maps with 'open' status
            if period['status'] == 'open':
                map = period['period']
                data_by_map[map] = [
                    {'Group': group, 'Name': name, 'Start_time': start_time}
                ]

        # Request with created data_by_map dict and
        # other metadata, pass to the next method
        request = scrapy.Request(
            values_url,
            callback=self.parse_odd_values,
            headers=self.headers,
            dont_filter=True,
            # This metadata passes to next method
            meta={'odd_data_list': odd_info_list[1:],
                  'data_by_map': data_by_map}
        )

        yield request

    def parse_odd_values(self, response):
        """
        Last method parse odds values and forms values dict   *ex:{id: value}
        than unite odds 'names' and 'values' by id and fills
        data_by_map dict with it by map
        """
        price_dict = {}

        # Passed metadata
        data_by_map = response.meta['data_by_map']
        info_list = response.meta['odd_data_list']
        values_list = json.loads(response.body)

        # Here filtering and forming values dict *ex:{id: value}
        for value_block in values_list:
            for price in value_block['prices']:
                if 'participantId' in price:
                    price_dict[price['participantId']] = price['price']

        # Here forms keys and values for output dict item
        for info_block in info_list:
            map = info_block['periods'][0]['period']
            odd_dict = {}
            for participant in info_block['participants']:
                try:
                    odd_dict[participant['name']] = price_dict[participant['id']]
                # Exception to prevent KeyErrors for deleted keys(not 'Teams' category, etc)
                # dont know how to fix it fast, anyway dont affects 'Teams' lines data
                except KeyError:
                    continue
            description = info_block['special']['description']
            # Checks if dict is not Null -> fill dict item by map
            if odd_dict:
                data_by_map[map].append((description, odd_dict))

        yield data_by_map


# yields items in dict format with structure:
#                   *ex:{map_number : [
#                   {'Group': group, 'Name': name, 'Start_time': start_time}
#                   ('Odd description, {'name': 'value', 'name': 'value'})
#                   ('Odd description, {'over': '154', 'under': '-230'})
#                   ]
