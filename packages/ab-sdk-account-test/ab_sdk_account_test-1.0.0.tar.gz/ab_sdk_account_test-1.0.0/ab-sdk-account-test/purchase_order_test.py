from ab_py.exsited.exsited_sdk import ExsitedSDK
from ab_py.exsited.purchase_order.dto.purchase_order_dto import PurchaseOrderListDTO, PurchaseOrderDetailsDTO
from ab_py.common.ab_exception import ABException
from ab_py.common.sdk_conf import SDKConfig
from tests.common.common_data import CommonData

def test_purchase_order_list_basic():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.purchase_order.list()
        print(response)
        # ResponseToObj().process(response=response["purchase_orders"][0])
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_purchase_order_details():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.purchase_order.details(id='ORDER_ID_PLACEHOLDER')
        print(response)
        return response
        # ResponseToObj().process(response=response["purchase_order"])
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)

test_purchase_order_list_basic()
# test_purchase_order_details()
