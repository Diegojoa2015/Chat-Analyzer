# analyzer.py

import pandas as pd

def filter_by_date_range(df, start_date=None, end_date=None):
    """Filtra mensajes por rango de fechas (inclusive start, exclusivo end)."""
    if start_date is not None:
        df = df[df["timestamp"] >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[df["timestamp"] < pd.to_datetime(end_date)]
    return df

def filter_by_month(df, months):
    """Filtra mensajes por lista de meses (número 1-12)."""
    return df[df["timestamp"].dt.month.isin(months)]

def filter_by_year(df, years):
    """Filtra mensajes por lista de años."""
    return df[df["timestamp"].dt.year.isin(years)]

def filter_by_hour_range(df, start_hour=None, end_hour=None):
    """Filtra mensajes por franja horaria. [start_hour, end_hour)"""
    if start_hour is not None and end_hour is not None:
        hour = df["timestamp"].dt.hour
        return df[(hour >= start_hour) & (hour < end_hour)]
    return df

def filter_by_users(df, users):
    """Filtra mensajes por una lista de usuarios."""
    return df[df["sender"].isin(users)]

def filter_singleline_messages(df):
    """Devuelve solo mensajes de una línea."""
    return df[~df["message"].str.contains('\n', regex=True)]

def filter_multiline_messages(df):
    """Devuelve solo mensajes multilínea."""
    return df[df["message"].str.contains('\n', regex=True)]

# Combinador genérico
def filter_chat(
    df,
    start_date=None,
    end_date=None,
    months=None,
    years=None,
    start_hour=None,
    end_hour=None,
    users=None,
    single_line_only=False,
    multiline_only=False
):
    filtered = df.copy()
    if start_date or end_date:
        filtered = filter_by_date_range(filtered, start_date, end_date)
    if months:
        filtered = filter_by_month(filtered, months)
    if years:
        filtered = filter_by_year(filtered, years)
    if start_hour is not None and end_hour is not None:
        filtered = filter_by_hour_range(filtered, start_hour, end_hour)
    if users:
        filtered = filter_by_users(filtered, users)
    if single_line_only:
        filtered = filter_singleline_messages(filtered)
    if multiline_only:
        filtered = filter_multiline_messages(filtered)
    return filtered

# Estadísticas comunes (todas sobre el DataFrame ya filtrado)
def count_messages(df):
    return len(df)

def messages_per_month(df):
    df = df.copy()
    df["month"] = df["timestamp"].dt.to_period("M")
    return df.groupby("month").size()

def messages_per_day(df):
    df = df.copy()
    df["date"] = df["timestamp"].dt.date
    return df.groupby("date").size()

def messages_per_hour(df):
    df = df.copy()
    df["hour"] = df["timestamp"].dt.hour
    return df.groupby("hour").size()

def messages_per_user(df):
    return df["sender"].value_counts()

def average_message_length(df):
    return df["message"].str.len().mean()
