from ab_py.exsited.exsited_sdk import ExsitedSDK
from ab_py.common.ab_exception import ABException
from ab_py.common.sdk_conf import SDKConfig
from tests.common.common_data import CommonData
from ab_py.exsited.payment.dto.payment_dto import PaymentCreateDTO, PaymentDataDTO, PaymentAppliedDTO, \
    CardDirectDebitPaymentAppliedDTO, CardDirectDebitPaymentDataDTO, CardDirectDebitPaymentCreateDTO
from ab_py.exsited.payment.dto.payment_dto import CardPaymentCreateDTO, CardPaymentDataDTO, CardPaymentAppliedDTO


def test_payment_create_basic():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False
    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
    try:
        payment_applied = PaymentAppliedDTO(processor="Cash", amount="20.00", reference="REFERENCE_PLACEHOLDER")
        payment_data = PaymentDataDTO(date="2024-08-10", payment_applied=[payment_applied], note="NOTE_PLACEHOLDER")
        request_data = PaymentCreateDTO(payment=payment_data)
        response = exsited_sdk.payment.create(invoice_id="INVOICE_ID_PLACEHOLDER", request_data=request_data)
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


def test_payment_create_card():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False
    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
    try:
        card_payment_applied = CardPaymentAppliedDTO(
            processor="Stripe card",
            amount="1.00",
            cardType="Visa",
            token="TOKEN_PLACEHOLDER",
            cardNumber="XXXXXXXXXXXX4242",
            expiryMonth="12",
            expiryYear="2025",
            additionalFields={"host_ip": "IP_ADDRESS_PLACEHOLDER"}
        )
        card_payment_data = CardPaymentDataDTO(date="2024-08-19", paymentApplied=[card_payment_applied], note="NOTE_PLACEHOLDER")
        request_data = CardPaymentCreateDTO(payment=card_payment_data)
        response = exsited_sdk.payment.create_card(invoice_id="INVOICE_ID_PLACEHOLDER", request_data=request_data)
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)

def test_payment_create_direct_debit():
    SDKConfig.PRINT_REQUEST_DATA = True
    SDKConfig.PRINT_RAW_RESPONSE = False
    exsited_sdk: ExsitedSDK = ExsitedSDK().init_sdk(request_token_dto=CommonData.get_request_token_dto())
    try:
        card_direct_debit_applied = CardDirectDebitPaymentAppliedDTO(
            processor="Stripe Direct Debit",
            amount="1",
            reference="REFERENCE_PLACEHOLDER",
        )
        card_direct_debit_data = CardDirectDebitPaymentDataDTO(
            date="2024-03-30",
            paymentApplied=[card_direct_debit_applied]
        )
        request_data = CardDirectDebitPaymentCreateDTO(payment=card_direct_debit_data)
        response = exsited_sdk.payment.create_direct_debit(invoice_id="INVOICE_ID_PLACEHOLDER",
                                                           request_data=request_data)
        print(response)
    except ABException as ab:
        print(ab)
        print(ab.get_errors())
        print(ab.raw_response)


# Call the test function
test_payment_create_card()
# test_payment_create_basic()
# test_payment_create_direct_debit()
