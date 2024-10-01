from ab_py.exsited.exsited_sdk import ExsitedSDK
from ab_py.exsited.order.dto.order_dto import OrderCreateDTO, OrderDataDTO
from ab_py.exsited.order.dto.usage_dto import UsageCreateDTO, UsageDataDTO
from ab_py.common.ab_exception import ABException
from ab_py.common.sdk_conf import SDKConfig
from order_usage_db.save_to_db import SaveToDB
from tests.common.common_data import CommonData
from ab_py.exsited.order.dto.order_nested_dto import OrderPropertiesDTO, OrderPurchaseDTO, POInformationDTO, \
    OrderItemPriceSnapshotDTO, OrderItemPricingRuleDTO, OrderLineDTO


def test_order_create_basic():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        request_data = OrderCreateDTO(
            order=OrderDataDTO(accountId="ACCOUNT_ID_PLACEHOLDER").add_line(item_id="ITEM_ID_PLACEHOLDER", quantity="1"))
        response = exsited_sdk.order.create(request_data=request_data)
        print(response)

        if response.order:
            account_id = response.order.accountId
            order_id = response.order.id
            for line in response.order.lines:
                if line.itemChargeType == 'METERED':
                    SaveToDB.process_order_data(_account_id=account_id, _order_id=order_id, _item_id=line.itemId,
                                     _item_name=line.itemName, _charge_item_uuid=line.chargeItemUuid)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_order_create_with_property():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False
    autobill_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
    try:
        order_properties = OrderPropertiesDTO(
            invoiceMode="AUTOMATIC",
            paymentMode="MANUAL",
        )
        order_data = OrderDataDTO(
            accountId="ACCOUNT_ID_PLACEHOLDER",
            id="ORDER_ID_PLACEHOLDER",
            properties=order_properties
        )
        order_data.add_line(item_id="ITEM_ID_PLACEHOLDER", quantity="1", price=400)
        request_data = OrderCreateDTO(order=order_data)
        response = autobill_sdk.order.create(request_data=request_data)
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_order_list_basic():
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.order.list()
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_order_details(id: str):
    SDKConfig.PRINT_REQUEST_DATA = False
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.order.details(id=id)
        print(response)
        return response
    except ABException as ab:
        error_code = None
        if ab.get_errors() and "errors" in ab.raw_response:
            error_code = ab.raw_response["errors"][0].get("code", None)
        print(f" {error_code}")


def test_order_cancel():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        response = exsited_sdk.order.cancel(id="ORDER_ID_PLACEHOLDER", effective_date="2024-10-11")
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_order_usage_add():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        request_data = UsageCreateDTO(
            usage=UsageDataDTO(chargeItemUuid="UUID_PLACEHOLDER",
                               chargingPeriod="2024-05-21-2024-06-20",
                               quantity="82",
                               startTime="2024-05-21 16:58:57",
                               endTime="2024-06-04 16:58:57",
                               type="INCREMENTAL",
                               )
        )
        response = exsited_sdk.order.add_usage(request_data=request_data)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_order_create_with_purchase_order():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False

    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())

    try:
        land_owner_purchase = OrderPurchaseDTO(createPo="true",
                                               poInformation=POInformationDTO(id="PO_ID_PLACEHOLDER", accountId="ACCOUNT_ID_PLACEHOLDER",
                                                                              currency="AUD", itemQuantity="1",
                                                                              itemPriceSnapshot=OrderItemPriceSnapshotDTO
                                                                                  (pricingRule=OrderItemPricingRuleDTO(
                                                                                  price="98.00"))))
        land_owner_line = OrderLineDTO(itemId="ITEM_ID_PLACEHOLDER", itemOrderQuantity="1",
                                       itemPriceSnapshot=OrderItemPriceSnapshotDTO
                                       (pricingRule=OrderItemPricingRuleDTO(price="100.00")),
                                       purchaseOrder=land_owner_purchase
                                       )

        software_owner_purchase = OrderPurchaseDTO(createPo="true",
                                                   poInformation=POInformationDTO(id="PO_ID_PLACEHOLDER", accountId="ACCOUNT_ID_PLACEHOLDER",
                                                                                  currency="AUD",
                                                                                  itemQuantity="1",
                                                                                  itemPriceSnapshot=OrderItemPriceSnapshotDTO
                                                                                      (
                                                                                      pricingRule=OrderItemPricingRuleDTO(
                                                                                          price="2.00"))))
        software_owner_line = OrderLineDTO(itemId="ITEM_ID_PLACEHOLDER", itemOrderQuantity="1",
                                           itemPriceSnapshot=OrderItemPriceSnapshotDTO
                                           (pricingRule=OrderItemPricingRuleDTO(price="0.00")),
                                           purchaseOrder=software_owner_purchase
                                           )

        order_properties = OrderPropertiesDTO(
            communicationProfile="",
            invoiceMode="AUTOMATIC",
            invoiceTerm="NET -7",
            billingPeriod="1 Week",
            paymentProcessor="Cash",
            paymentMode="MANUAL",
            paymentTerm="NET 30",
            paymentTermAlignment="BILLING_DATE",
            fulfillmentMode="MANUAL",
            fulfillmentTerm="Immediately"
        )

        request_data = OrderCreateDTO(
            order=OrderDataDTO(accountId="ACCOUNT_ID_PLACEHOLDER", name="renterSDKx", id="ORDER_ID_PLACEHOLDER",
                               billingStartDate="ORDER_START_DATE", orderStartDate="2024-09-04",
                               properties=order_properties,
                               lines=[land_owner_line, software_owner_line]))

        response = exsited_sdk.order.create_with_purchase(request_data=request_data)
        print(response)

    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


# test_order_create_with_property()
# test_order_create_basic()
# test_order_details()
test_order_cancel()
# test_order_create_with_purchase_order()
