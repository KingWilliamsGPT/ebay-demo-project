import pprint

from ebaysdk.finding import Connection as Finding
from ebaysdk.shopping import Connection as Shopping
from ebaysdk.exception import ConnectionError


CONFIG_FILE = 'ebay.yaml'

from ebay_config import CONFIG



def _get_response(Connection, method, kwdict={}, **more_stuff):
    api = Connection(**CONFIG, **more_stuff)
    res = api.execute(method, kwdict)

    return api, res



class Page:
    def __init__(self, page_dict):
        self._page_dict = page_dict
        self.pageNumber = page_dict.get('pageNumber', '')
        self.entriesPerPage = page_dict.get('entriesPerPage', '')
        self.totalPages = page_dict.get('totalPages', '')
        self.totalEntries = page_dict.get('totalEntries', '')


class Response:
    def __init__(self, con_res):
        self._res = con_res         # probably useful later
        self.res = con_res = con_res.dict()
        self.page = Page(con_res.get('paginationOutput', {}))
        
        self.version = con_res.get('version', '')
        self.timestamp = con_res.get('timestamp', '')
        self.ack = self.response_code = con_res.get('ack', '')
        self.serchURL = con_res.get('itemSearchURL', '')

        search_result = con_res.get('searchResult', {})
        self.search_res = search_result.get('item', [])
        self.search_res_count = search_result.get('_count', '')

        self.items = list(self.get_items())

    def get_items(self):
        for item in self.search_res:
            yield Item(item)


class Item:
    def __init__(self, item):
        
        self.dict = pprint.pformat(item)
        self.galleryURL = item.get('galleryURL', '')
        
        self.title = item.get('title', '')
        self.subtitle = item.get('subtitle', '')
        
        self.productId = item.get('itemId', '')
        self.globalId = item.get('globalId', '')

        self.location = item.get('location', '')    # where it's selling from
        self.detailURL = item.get('viewItemURL', '')
        self.isTopRated = item.get('topRatedListing', '') == 'true'
        
        _sp = item.get('sellingStatus', {}).get('currentPrice', {})
        self.sellingPrice = f"{_sp.get('_currencyId', '')}{_sp.get('value', '')}"
        
        _ct = item.get('primaryCategory', {})
        self.category = _ct.get('categoryName', '')
        self.categoryId = _ct.get('categoryId', '')

        _si = item.get('shippingInfo', {})
        self.shippingDest = _si.get("shipToLocations", '')
        _sc = _si.get("shippingServiceCost", {})
        self.shippingCurrency = _sc.get('_currencyId', '')
        self.shippingCost = _sc.get('value', '')
        self.shippingType = _sc.get('shippingType', '')
        
        _cd = item.get('condition', {})
        self.condition = _cd.get('conditionDisplayName', '')
        self.conditionId = _cd.get('conditionId', '')

        self.isReturnable = item.get('returnsAccepted', '') == 'true'

        def is_free_shipping(self):
            return self.shippingType == 'Free'

    
class Api:
    def __init__(self):
        pass

    
    def do_find(self, keyword=''):
        try:
            api, res = _get_response(Finding, 'findItemsAdvanced', {'keywords': keyword})
            return Response(res)

        except ConnectionError as e:
            print(e)
            print(e.response.dict())
            return 

    def do_find_product_by_id(self, product_id):
        try:
            api, res = _get_response(Shopping, 'GetSingleItem', {'ItemID': product_id})

            return res
        except ConnectionError as e:
            print(e)
            return None