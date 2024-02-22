import re
import pandas as pd


def preprocess(data):
    pattern = "\[\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}:\d{2}\s[APMapm]{2}\]"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    a = df['message_date'].astype("string").str.strip("[PMAM]")
    a = a.str.rstrip()
    df['message_date'] = pd.to_datetime(a, format='%d/%m/%y, %H:%M:%S')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # User name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['only_date'] = df['date'].dt.date
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['second'] = df['date'].dt.second

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + "-" + str('1'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df