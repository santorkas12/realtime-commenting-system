import base64

if __name__ == '__main__':
    credentials = input('Enter credentials in the form \'username:password\': ')

    base64_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    print(f'Encoded credentials: {base64_credentials}')