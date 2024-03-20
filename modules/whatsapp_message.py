from whatsapp_api_client_python import API


greenAPI = API.GreenAPI(
    "7103904545", "2acc2a2fc4c44981bbc7680c56fb2a78afc02b2ae36942dab7"
)


def proxy():
    response = greenAPI.sending.sendMessage("919773774261@c.us", "bhai mera aaj proxy laga de")

    print(response.data)


if __name__ == '__main__':
    proxy()