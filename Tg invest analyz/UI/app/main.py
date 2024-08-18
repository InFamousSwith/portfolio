import back
import config
import numpy as np
import plots
import streamlit as st
from psycopg2.extensions import AsIs, register_adapter
from sql_selector import SelectorDF


st.set_page_config(layout="wide")
register_adapter(np.int64, AsIs)

selector = SelectorDF(config.dbname, config.host, config.user, config.port)
channels = [el[0] for el in selector.simple_select(config.channels_query)]

st.sidebar.markdown("Выберите один или несколько вариантов:")

selected_channels = back.select_items_sidebar(channels, "Выберите каналы")
df = selector.build_df(config.sql_columns, config.sql_data, selected_channels)
df["year"] = df["message_date"].apply(lambda x: x.year)

back.empty_check(df)

selected_brances = back.select_items_sidebar(df["branch"].unique(), "Выберите отрасли")
brances_df = df[df["branch"].apply(lambda x: x in selected_brances)]
back.empty_check(brances_df)

selected_tickers = back.select_items_sidebar(brances_df["ticker"].unique(), "Выберите тикер")
brances_df = brances_df[brances_df["ticker"].apply(lambda x: x in selected_tickers)]
back.empty_check(brances_df)

selected_years = back.select_items_sidebar(df["year"].unique(), "Выберите год")
brances_df = brances_df[brances_df["year"].apply(lambda x: x in selected_years)]
back.empty_check(brances_df)

brances_df["income"] = brances_df["real_percent_profit"].apply(lambda x: "Доход" if x >= 0 else "Убыток")
brances_df = brances_df[brances_df["percentage"] < 250]
brances_df["real_percent_profit"] = round(brances_df["real_percent_profit"], 2)
brances_df["real_profit"] = round(brances_df["real_profit"], 2)

# st.dataframe(brances_df)


plots.Hists().draw_predictions(brances_df)
plots.Hists().draw_incomes(brances_df)
plots.Scatters().draw_all_points(brances_df)  # Распределение всех идей
plots.Hists().draw_branch_income(brances_df)  # Доходность идей по отраслям
plots.Hists().draw_branch_avg(brances_df)  # Средняя доходность идей по отраслям
plots.Hists().draw_branch_count(brances_df)  # Количество сбывшихся идей по отраслям
plots.Hists().draw_branch_channels(brances_df)  # Доходность по отраслям и каналам
plots.Hists().draw_year_bar_plot(brances_df)  # Доходность идей по годам
plots.Hists().draw_ticker_plot(brances_df)  # Доходность идей по компаниям
plots.Hists().draw_absolute_income(brances_df)  # Доходность если в куплена одна бумага на идею
plots.Areas().draw_price_income(brances_df)  # Зависимость доходности от цены
plots.Areas().draw_time_income(brances_df)  # Зависимость доходности от времени
plots.Areas().draw_perc_income(brances_df)  # Зависимость доходности от предсказанной доходности

st.stop()
