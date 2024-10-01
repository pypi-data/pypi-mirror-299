from ab_py.exsited.auth.dto.token_dto import RequestTokenDTO


class CommonData:

    @staticmethod
    def get_request_token_dto():
        return RequestTokenDTO(
            grantType="client_credentials",
            clientId="NC5hYjFfMV0pLTVfYDVeMjkpXl0xMikwMDEzKTUxLzApM15iMzI0YC0tM11dKTUsLDQpM18zXzM=",
            clientSecret="LylcXSxaLFgkWGVcWltYMTgkWFhZYyQrMFosJC8nWVwkXCovXCgqKTBcXFgnJDAnJy8kWVknWy4=",
            redirectUri="https://banglafighter.com",
            exsitedUrl="https://api-stage.exsited.com",
        )
