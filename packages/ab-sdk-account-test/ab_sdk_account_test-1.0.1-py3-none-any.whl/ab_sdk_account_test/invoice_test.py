from ab_py.exsited.exsited_sdk import ExsitedSDK
from ab_py.common.ab_exception import ABException
from ab_py.common.sdk_conf import SDKConfig
from tests.common.common_data import CommonData
from ab_py.exsited.invoice.dto.invoice_dto import InvoiceCreateDTO, InvoiceDataDTO


def test_invoice_create_basic():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False
    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
    try:
        request_data = InvoiceCreateDTO(invoice=InvoiceDataDTO(invoiceNote="Created From Python SDK"))
        response = exsited_sdk.invoice.create(id="ORDER_ID_PLACEHOLDER", request_data=request_data)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_invoice_list():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.invoice.list()
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_invoice_details():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.invoice.details(id="INVOICE_ID_PLACEHOLDER")
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_invoice_details_against_order():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.invoice.invoice_details_against_order(order_id="ORDER_ID_PLACEHOLDER")
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_invoice_list_against_order():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.invoice.invoice_details_list_against_order(order_id="ORDER_ID_PLACEHOLDER")
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


# test_invoice_create_basic()
test_invoice_details()
