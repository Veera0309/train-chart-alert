import requests
import json
import time
from twilio.rest import Client
import os

def check_train_chart_status(train_number, journey_date, boarding_station_code):
    url = "https://www.irctc.co.in/online-charts/api/trainComposition"

    payload = {
        "trainNo": train_number,
        "jDate": journey_date,
        "boardingStation": boarding_station_code
    }

    headers = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9,ta;q=0.8,hi;q=0.7',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://www.irctc.co.in',
        'priority': 'u=1, i',
        'referer': 'https://www.irctc.co.in/online-charts/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
        'Cookie': 'ext_name=ojplmecpdpgccookcobabopnaifgidhf; _cc_id=85f42dda8402b82d5748d732307fb447; _ga_SHTZYKNHG2=GS2.1.s1758702931$o2$g1$t1758703780$j60$l0$h0; _vdo_ai_uuid=66508c21-a5a3-4d45-b5f5-9c60086980e2; _ga_8J9SC9WB3T=deleted; _ga_HXEC5QES15=GS2.1.s1762413469$o6$g0$t1762413469$j60$l0$h0; _ga_7K0RMWL72E=GS2.1.s1763609647$o7$g0$t1763609647$j60$l0$h0; _ga_JSTMKS9Y3J=GS2.1.s1764164088$o7$g0$t1764164088$j60$l0$h0; _ga_8J9SC9WB3T=GS2.1.s1764164087$o8$g0$t1764164088$j60$l0$h0; _clck=1p435h7%5E2%5Eg1c%5E0%5E2025; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%22d5e3437c-afcb-40d6-97c1-b5c8bb53b3d9%5C%22%2C%5B1762153934%2C25000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol89Kq9dF33iqrcIR2blW3e8oMK3VhBQSOpYDuM4UOy0gr54QV3sgpnJDX4WEVr90RL3uIl5HdTl0YTYbBAOWCcCx7Sht1-CfSqv9L9xV6PNxAE1vgwnzrQxEE8iP0d8AbOQZIqutXTDGJAXrMzwsEZgTXvo-Q%3D%3D%22%5D%5D; cto_bundle=je92TF84OXppS2RHQlpxY2pEUUNjSzNtSVNQaW82bEsyUmhPTG1nUVUlMkZpTGhGQmt3dXFaciUyRkhOZXBhdzRTTWg5YjR4RiUyRk85QkpUSUJwb21EVlhWTzNGMDN0MlE4Y2ttZ05HVFI4SE80SFJleTlYeGx2bHJ4enpnUVJWcVBQSjlISkJmcU9Rdk9HcWFCUnhoYzBWaWU2YVh5a3lLQWlINDI5dFNTUDVkT002RjA5M21VTTgzMlh6RjlhZ0IwOEd5OVU5eTAwZGlpTTVRSlNxNmowdHY4azlmU2xRJTNEJTNE; __gads=ID=470e81d2ec08e427:T=1752858158:RT=1764170421:S=ALNI_MbfJjKdWm4ScjOAcz06zy4N67-NdA; __gpi=UID=00001168ad01900f:T=1752858158:RT=1764170421:S=ALNI_MZYLuVQT3zQsdwB7xoGBmmsUdt_uQ; _ga_8PFRHJTYEY=GS2.1.s1764170426$o8$g0$t1764170426$j60$l0$h0; _ga_NFN218243Z=GS2.1.s1764170426$o10$g0$t1764170426$j60$l0$h0; TS018d84e5=01d83d9ce7958c7fc76f2d72b1fa19de383da5adf46710243af090b91197134428722918d26f4d5b78059cc1e254630f5105feae9c; bm_ss=ab8e18ef4e; et_appVIP1=990006794.16927.0000; PIM-SESSION-ID=zpSMc1f0ww9guNn0; bm_lso=25A9EE1F29B87EDDFDA839C739CF49D50AA16B2A5F204E0589247DC5EBF0B5AB~YAAQh0PHFyz2HMObAQAAoY9QxwboAofPVjypezPH6cefg3Nq9NhhVRch5XxfWVQ7PHd9QCHrQxx5nPqk8EzqvCijdmEKAIlRsfuFby9xf2yVZWN/vXgYww16OnZ5K2nhSNPDdnml4NKwTwes/aBomnAEqXbXd95oamr6ERgpSpJAcwOEkrrUYB30n/Sf6Eenfi7HYZKtTNps+kHNJtaADeXm2lyknvQPlxHXYBIoGkPFcIIT+5iJ09amLjn2ncnl1huAZ1V/m6VL+muIh5eF7EklOZfIqWeOSKblhq57s651e5J7m6CGsb4qQjQfxEEwDzAsVhy3cLv5f7zzJllht45afkDIADj7LvmJ02Xz2IUWzIelK2EQVeNTNQ61azbuq3XGx3J/gjtOoEYzJBgC/3VkUbK8jvtlsnD5niTOYPN3ZJgI02wbosnau/jRCEFzwcd6ZX78XQRAHnoJ8vj8rDb/6kJWqQxfMsNQIppkHmePXZDnaSGKejg=~1768575504754; _ga_E963V1KB9F=GS2.1.s1768575504$o1$g0$t1768575504$j60$l0$h0; _ga=GA1.3.447292215.1752858154; _gid=GA1.3.899074788.1768575505; RT="z=1&dm=www.irctc.co.in&si=1bb6027a-9793-48af-a4e0-259473f2e127&ss=mkh06wgw&sl=1&tt=wo&rl=1&ld=173"; ngetAppId=aaTHUkoFhmyeEkBxgsKtsmOuCvLqpZpYl6kAux-BDojbx-gHykOP!1423192836; bm_s=YAAQhkPHFwpyZMKbAQAA2H9SxwRCnGYcfGB9y48hW6ziSPRnIZqWAKRI7axprrbKB91lnUTdBuXBfzNz7m4PjVeGnxjYfFvQwrMe3WGNnecMm3VJVE+CRulE/fc7CUVEMeqpEIWBn/o1a2MRDGvickmbVpqyX2gHEmF1XQ5HSpl1OMn3pIRxG35QQk/dBNz4Ivow8NekNlsNb6vzdl63UBjFxHjeWRxtVD/dAp20XVI71a0maCRVf5vVOK/GXhCqX7WkbaDBRKBwRonWtjSuXjkx5TQ9jaVHWWFnjQjymvmyEtuaZXIo1LSWe+mBaVoomGqnHRittCj9EOKrkZQm4lvdW+c27/+s/6A1vmToQmhqTeauPdYsegfrvcPiRS/o8sB6TzYFhAIuvaYAiURQNobhdV9rzGgXbBVqqXPdCB3CuWYOYHPTLhOQ7q66ZF0zOxTPAf5s2IVU5vo8YYMedxx63kpEIfkbDcD8/3xC7Hje4DzWHBEv/s2q6sU5AfarFeDufIexUasGb77Kd/HUkoHRhYau54IhcZBfgHt4xx48xUk31qCjfFS1HXuNmerUJBnoAL66/gP8B3VA3D1XI2wLcR1PNgXxkLog1XEH47dfeOn5ouiSqYEzpt7J/SvIMiI619QVng==; bm_so=96B05E8A73EA48F6CEE013AFBC4B2A659194ADAF9ECF9EC1AF60661C801F48FE~YAAQhkPHFwtyZMKbAQAA2H9SxwabRgXIqt5PJslaHKIKlYjbc/mKGQYHQfLPM5CwdBGQdVoqoWyhEAu2BJK0RXxnNo7tekne+X9qTkctP0IaLb5y3RTE1Vci35hFhYqvCX0DVBqHvkVpEM6GjITA8PR227JLYUqpXtM6MArfWY5WF6HcSYYVLOtFkm7/A/g3HbQP6DHZla5RUjMSrPjlyAXvv/i4ScG6E+Phs/O1HKCt/MlgYc/IaFQqX6EeKjsWK89RjEAjKOQ4aHD5LrwIZcSyCYPp0HbC5XEBDcHm3L9Qr9ZoFVyvseJpPbzSTQzHjGib344gXJeYyYjm+EReGtLulXIOIs6jaXNS9c09ueLduWp9vGvTBySB3wApbzk4TvH/FwmFC0xVDwlw5W2bNAeDgb88Bf2myk8vxZTGy8QrcEsklAMxe/h9qc5W44FdyyhhUZicIZv+B8xeQrIfODlCszvHw1X2BQCAwi7l5ii16PIrbkTZJ0U=; bm_sz=76F5663A162CDEEE75C1FEDC07E7A584~YAAQhkPHFwxyZMKbAQAA2H9Sxx5+edDNRtsDrEdV5cAClTK840Cg39YKyP587JLsYLTf58IYHBGCarZXb2n6XKsl+d9M5ha1ZwDYpfre+3vnMGnJhbzCmP6RH0HfwZcNolVK1Zn4f1ozbH/CCS/728fLV7MNkE+r1X586P0JG8/nXCntUlwO4Yb7vQMdGX8CE6n58RgYT1hWcTS3Kcf/12YEN3xMR8MgGCTgpWCz9OMhQFzjWWJ1xBOqGh+qSKTLVazcQ+bPKia2RVezv+ppBbRmH1leytupUccQUjOA3+nC475iRd6CGZu+m0JO1tfGmw2sfzZCZqZ/4y7891VL+ORJ3m6Kixrgf8a6XRNpnBttGWL0tIMPMsJEVof+T7XZSkXvTa5zvjWZTQeeVe2tQaKPCpV+Rr9Z2My8mhcRfnqfUmzwaq8Zp6+HLsqBaYMbBjXpPrdp~4408385~4473651; _abck=90351CC3BEB7322AB96F410C1D892D8B~-1~YAAQhkPHFzqoZMKbAQAAL3NTxw+JEXNKrMfwz7gRZn3ciYtjlBNE5AVZr48GVHyjS6SxxewqAsP3mCRGftHhCPe0+7i6PUPPyhYLUsUtD9WOtWns1YcoHMoa+gkw4iz7WAuDq4SC2IekJAmF3o+x8fAXoulF6c+kkhK6R9PsnT6zIHroF82hV0tMq9p79wCuEMwpqYwcLsVSz9uNBxqMYG/lJEb4V+4Xod7Fhhc0VS3FF/gB5KPeBa+3qW+vfvmYX2/jyLodzpHQ6iN6FWuGnfRynMu2AwdkN/Sffz227BlaJNhk3eTMNYHBS+STYPM8y8D8qLmvcnwfXUG9PcX5VHEHHNJHoQhJHXqakcnz86Hu+o3BJS5MklFg6a5NmjqX2Uz3eq2JRJkIpLDdK9BO4ylHl6lPKFyHmkM1dim7vLtBHXCIKC8DzBK7RQTQ7XqllWv+2107S0N/xwT+dMLUxsEGcuZ7Ly/30eDantMDQVzYVcQEofyNSHx3oN5JPco3Ec6qmlYrq0kNyGgfupXwlRL+yzK0oRT4f5930TriOc5jyEA6UTvcLkxsHF9vROHHBzqjbA5U8UuH1h+RfNbf9H0m3O7a4DJZ6rPlL3ttR9jxvVdECMNPvJ6jK3o0vfmBY0tlW/TftOHRmoaBoU+xLPTFMPufZnT4AOkik5lpywZMhd06XEEBuAS/jGWsxq/JCeJYbkT7XAyDqarI2Z/hyQ5zHMhZC6J0DPVyEWHEqmoLkzDp8Ofq9dUmW0hlq30shSF5Xzc2lmh42Vx/UXKceerbKTSLyJZDCvFlmYhteqy6uPd8oyCtGx3sEy8iohfr3wNxJiHuMaUDZfsqc9p+ha0jN53KrWPgrCnjVekuQTwiXesdB4cDa2atJ6/bQXr9L4WTL2Nn0wiW3wBb6+L0H5v68WUiulVXGVfrkc4Zq5mhkgf9EBf6X88wbb/MwoZw~-1~-1~1768579105~AAQAAAAF%2f%2f%2f%2f%2f1+2szAD3TCxXL%2fmnO+Dlb8xf0y%2fx5wvuiVGLSAWYv+zc2kqF%2fRTFN5o%2fr3CGoImbPJqGEmThQcg1npr4rudrfyD2QxM3kQl0rtNBBVk9Ela%2fOxvNgCQSJOH7bhge1oGnt+3nno%3d~1768575753; TS018d84e5=01d83d9ce71331193a020faa1f864a37fcb39a0d7bc7bcaf51b11c1ae11048c1701befaf7b2e3a053643195125b361de9eb0ba0cc8; _abck=90351CC3BEB7322AB96F410C1D892D8B~-1~YAAQdEPHF823obubAQAA0aOBxw/83lQNBmgiMbLdtWlsPxEMI2J4EX/08HEjo0fhrQMhutL8qcZr6n1KyhrPtPKiiohqDOP31xZ0inhekcQ07oUna8x8IRHYwKMfAFLrujVZgPOhpoXW53HYEU60E/He4dpnR8f8UG01UQPVmEvoAIaFAMLlra9SjI2J2q1QGct4YuJXdFiJCGzhN7uO12WJ1Tkgkftm5Z+oujzxTirKa3XqwoHBEeSmiskJ1vzYnUOTWncdPAdxGCZBS2YMXiq05R1lmV60hCXh+j0bcoz4kAKr93JPSQCdoAyxjMGSE6tsBm5xuKGHIzic5w4piN+3CvrO2HPDPqhQAq8oaP7nu7X3lAWO8m11sWKO/gi2XRSy9mKEL9gSokHuOHVSlEJKkJeRLi2IzVu1k7PCoRM5NpKE4YdKb6wQonxqBRKHNEc/Q3DqDJ52K5ru6/mPEWP5Dz8R5uRqhLaMo2FGXR5XlKQSeIi5c3vYl4n8I5/hP2e91gXDQMdbyquTN2KcPyUckMVcZVpZV3oRpF0ao19wKl2J1TYZuTqFqy7jP0n5HM++/Vw6llLNqMNSt6DQJLA0bLyeKf5t6NLBZdvMVNFxPQ7zgk5wnOqVHTONQYu5WV/CeJsZbJB0Be73+XxujJbrcG3g6nhvD+N4zlFcfn2OijWw5YlMNUyoWSNuYzHurpZCObzxasCcWuarcaXFzuuJBKRsi/QPAxqhApRQupMOolZZQGfF3VCTQ/Q/xqQBGXnPNEaDvJD+xDDq8J9eQDsOy0Eum2kyYGdPEmTEAm0WKG4NpKDm+rq6lIJOnYGtbNFL97CIM1q0MfSwKr7HwtLQzUYAHbxcbe1B0a3i5lYi8c5AgD9BUnQ185we1R+RnM0sceGPdTLORhraqQ5xTZZam52224dJ/Qz3u+k/iZSpQLGNIV88Sp2ay3rrSjPc~-1~-1~1768579105~AAQAAAAF%2f%2f%2f%2f%2f1+2szAD3TCxXL%2fmnO+Dlb8xf0y%2fx5wvuiVGLSAWYv+zc2kqF%2fRTFN5o%2fr3CGoImbPJqGEmThQcg1npr4rudrfyD2QxM3kQl0rtNBBVk9Ela%2fOxvNgCQSJOH7bhge1oGnt+3nno%3d~1768575753'
    }
    
    return requests.post(url, json=payload, headers=headers, timeout=15)

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

def send_whatsapp_message(phone_numbers, message):
    for number in phone_numbers:
        try:
            client.messages.create(
                from_="whatsapp:+14155238886",   # Twilio sandbox
                to=f"whatsapp:{number}",
                body=message
            )
            print(f"WhatsApp sent to {number}")
        except Exception as e:
            print(f"Failed for {number}: {e}")


def format_vacant_coaches(vacant_coaches):
    return "\n".join(
        f"{c['coachName']} ({c['classCode']}): {c['vacantBerths']} berths"
        for c in vacant_coaches
    )

def main():
    train_numbers = [12602, 16231]
    journey_date = "2026-01-17"
    boarding_station_code = "ED"
    receiver_phone_number = ["+918667380449","+916381799681"]

    pending_trains = set(train_numbers)

    while pending_trains:
        for train_number in list(pending_trains):
            try:
                response = check_train_chart_status(
                    train_number,
                    journey_date,
                    boarding_station_code
                )

                if response.status_code != 200:
                    continue

                data = response.json()

                if data.get("error"):
                    print(f"{train_number}: Chart not prepared yet")
                    continue

                vacant_coaches = [
                    coach for coach in data.get("cdd", [])
                    if coach.get("vacantBerths", 0) > 0
                ]

                message = (
                    f"*Alert!* Sent from Railway\n\n"
                    f"Chart Prepared for Train {train_number}\n\n"
                    f"{format_vacant_coaches(vacant_coaches) if vacant_coaches else 'No vacant berths available'}"
                )

                send_whatsapp_message(receiver_phone_number, message)
                pending_trains.remove(train_number)

            except Exception as e:
                pending_trains.clear()
                print(f"Error for train {train_number}: {e}")
        
        if not pending_trains:
            print("All trains processed. Exiting loop.")
            break
        
        time.sleep(600)

if __name__ == "__main__":
    main()
