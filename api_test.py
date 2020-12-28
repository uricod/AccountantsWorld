import requests
import json
from secrets import client_secret, client_id, api_key


def auth():
    url = 'https://qa-auth.accountantsoffice.com/connect/token'

    payload = {'Grant_Type': 'client_credentials',
               'client_id': client_id,
               'client_secret': client_secret,
               'scope': 'payroll_api'
               }

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    txt = json.loads(response.text)
    access_token = txt['access_token']

    print(access_token)
    print(response.headers['Date'])

    return access_token


def accountants_world_api(url, access_token, api_key, payload=None):
    headers = {'Url': url,
               'authorization': "Bearer " + access_token,
               'x-api-key': api_key
               }

    if payload is not None:
        response = requests.request("GET", url, headers=headers, params=payload)
    else:
        response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        print('Success')
        js = response.json()
    else:
        js = ''
        print('Error')
        print(response.headers)
        print(response.text)

    return js


def pull_pay_schedules(access_token):
    base_url = 'https://qa-api.payrollrelief.com/integration/'
    full_url = base_url + 'payroll/PaySchedules'

    payload = {'start': '01/01/2019', 'end': '12/31/2019'}

    txt = accountants_world_api(full_url, access_token, api_key, payload=payload)

    scheduleid = txt[0]['payScheduleId']

    return scheduleid


def pull_pay_data(scheduleid, access_token):
    base_url = 'https://qa-api.payrollrelief.com/integration/'
    full_url = base_url + f'payroll/getnextpayrolldata/{scheduleid}'

    txt = accountants_world_api(full_url, access_token, api_key)

    payrollid = txt['keyData']['payrollId']
    startdate = txt['keyData']['payPeriod']['startDate']
    enddate = txt['keyData']['payPeriod']['endDate']
    paydate = enddate = txt['keyData']['payPeriod']['payDate']
    payroll_data = txt['timeData']

    print(payrollid, startdate, enddate, paydate)

    pay_list = []

    for i in payroll_data:
        emp_id = i['empId']
        emp_num = i['empName']
        loc = i['locationCode']
        dep = i['deptCode']
        reg = i['payTypes'][0]['hours']
        ot = i['payTypes'][1]['hours']
        spec = i['payTypes'][2]['hours']
        vac = i['payTypes'][3]['hours']
        sick = i['payTypes'][4]['hours']
        personal = i['payTypes'][5]['hours']
        hol = i['payTypes'][6]['hours']
        bon = i['payTypes'][7]['hours']
        auto = i['payTypes'][8]['hours']
        remb = i['payTypes'][9]['hours']

        pay_list.append([emp_id, emp_num, loc, dep, reg, ot, spec, vac, sick, personal, hol, bon, auto, remb])

    return pay_list


if __name__ == '__main__':
    a_token = auth()
    s_id = pull_pay_schedules(a_token)
    data = pull_pay_data(s_id, a_token)
    print(data)


