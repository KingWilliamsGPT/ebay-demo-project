import datetime
from ebaysdk.finding import Connection

try:
    api = Connection(config_file='ebay.yaml')
    response = api.execute('findItemsAdvanced', {'keywords': 'legos'})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

    print(item)

except ConnectionError as e:
    print(e)
    print(e.response.dict())