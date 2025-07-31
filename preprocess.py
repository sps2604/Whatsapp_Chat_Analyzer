import re
import pandas as pd

def preprocess(data):
    pattern = r"(\d{1,2}/\d{1,2}/\d{2,4}), (\d{1,2}:\d{2}\s?[APap][Mm]) - (.*)"
    matches = re.findall(pattern, data)
    df = pd.DataFrame(matches, columns=["Date", "Time", "Message"])
    df["DateTime"] = df["Date"] + " " + df["Time"]
    df = df[["DateTime", "Message"]]
    users = []
    messages = []
    for message in df['Message']:
        entry = re.split('([\w,\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users'] = users
    df['message'] = messages
    df.drop(columns=['Message'], inplace=True)

    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%d/%m/%y %I:%M %p")
    df['year'] = df['DateTime'].dt.year
    df['month'] = df['DateTime'].dt.month_name()
    df['month_num'] = df['DateTime'].dt.month
    df['only_date'] = df['DateTime'].dt.date
    df['day_name'] = df['DateTime'].dt.day_name()
    df['day'] = df['DateTime'].dt.day
    df['hour'] = df['DateTime'].dt.hour
    df['minute'] = df['DateTime'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

