from requestclient import RequestClient

if __name__ == '__main__':
    access_id = "C9A03CDED67C4564951DA9603DB5F352"
    secret_key = "FC958FC2B262E04B239771819DFD934AA815BA917210E036"
    client = RequestClient(access_id, secret_key)

    response = client.request('GET', '/v1/balance/')
    balance: dict = response.get('data')
    for key in balance.keys():
        coin: dict = balance[key]
        print(f"{key} => {coin['available']}")
