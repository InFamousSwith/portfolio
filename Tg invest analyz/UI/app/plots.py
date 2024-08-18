from typing import Callable, Text

import pandas as pd
import plotly.express as px
import streamlit as st


class BasePlot:
    def __init__(self) -> None:
        pass

    def draw_plot_with_head(self, header: Text, subheader: Text, func: Callable, **kwargs) -> None:
        st.subheader(header)
        if subheader:
            st.text(subheader)
        fig = func(**kwargs)
        st.plotly_chart(fig, use_container_width=True)


class Scatters(BasePlot):
    def __init__(self) -> None:
        super().__init__()

    def draw_all_points(self, df: pd.DataFrame) -> None:
        st.subheader("Распределение доходных и убыточных идей в зависимости от срока идеи")
        col1, col2 = st.columns(2)
        with col1:
            if_income = st.checkbox("Только доходные")
        with col2:
            if_loss = st.checkbox("Только убыточные")
        if if_income and not if_loss:
            df_copy = df[df["income"] == "Доход"]
        elif if_loss and not if_income:
            df_copy = df[df["income"] == "Убыток"]
        else:
            df_copy = df.copy()
        df_copy.loc[df_copy["income"]=="Убыток", "percentage"] = df_copy.loc[df_copy["income"]=="Убыток", "percentage"] *-1

        self.draw_plot_with_head(
            "",
            "",
            px.scatter,
            data_frame=df_copy,
            x="expectation_time",
            y="percentage",
            color="channel_name",
            color_discrete_map={  
                "Доход": "#66CDAA",
                "Убыток": "#FF6347",
            },
            labels={"expectation_time": "Период идеи", "percentage": "Процентный уровень", "income": "результат", "channel_name": "Название канала"},
            symbol="income",
            width=1400,
        )


class Hists(BasePlot):
    def __init__(self) -> None:
        super().__init__()

    def draw_predictions(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp["if_good_idea"] = df_tmp["if_good_idea"].apply(lambda x: "Да" if x == True else "Нет")

        self.draw_plot_with_head(
            "Количество сбывшихся/не сбывшихся идей",
            "",
            px.histogram,
            data_frame=df_tmp,
            x="channel_name",
            y="if_good_idea",
            color="if_good_idea",
            barmode="group",
            height=400,
            histfunc="count",
            text_auto=True,
            color_discrete_map={
                "Нет": "#FF6347",
                "Да": "#66CDAA",
            },
            labels={"channel_name":"Название канала", "if_good_idea":"Реализация", "count": "количество"}
        )

    def draw_incomes(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()

        self.draw_plot_with_head(
            "Получен ли доход или убыток от вложений в идею",
            "Идея может не реализоваться, но от инвестиции в неё получен положительный результат",
            px.histogram,
            data_frame=df_tmp,
            x="channel_name",
            y="income",
            color="income",
            barmode="group",
            height=400,
            histfunc="count",
            # histnorm="percent",
            text_auto=True,
            color_discrete_map={
                "Убыток": "#FF6347",
                "Доход": "#66CDAA",
            },            
            labels={"channel_name":"Название канала", "if_good_idea":"Реализация", "income": ""}
        )

    def draw_branch_income(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp["if_income"] = df_tmp["real_percent_profit"].apply(lambda x: "Средний уровень дохода, %" if x >= 0 else "Средний уровень убытка, %")
        df_tmp.loc[df_tmp["if_income"]=="Средний уровень убытка, %", "real_percent_profit"] = df_tmp.loc[df_tmp["if_income"]=="Средний уровень убытка, %", "real_percent_profit"] *-1        
        df_tmp = df_tmp.sort_values(by="branch", ascending=False)

        self.draw_plot_with_head(
            "Средняя доходность/убыточность по пулам доходных/убыточных идей",
            "Посчитаны отдельно средняя доходность/убыточность только по доходным/убыточным идеям соответственно",
            px.histogram,
            data_frame=df_tmp,
            x="branch",
            y="real_percent_profit",
            color="if_income",
            barmode="group",
            height=400,
            histfunc="avg",
            color_discrete_map={
                "Средний уровень убытка, %": "#FF6347",
                "Средний уровень дохода, %": "#66CDAA",
            },
            labels={"if_income": "Доходность", "branch": "Отрасль", "real_percent_profit": "(Средний процент, %)"},
        )

    def draw_branch_avg(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp = df_tmp[["branch", "real_percent_profit"]].groupby(by="branch").mean().reset_index()
        df_tmp = df_tmp.sort_values(by="branch", ascending=False)

        self.draw_plot_with_head(
            "Общий результат инвестирования во все идеи по отраслям",
            "",
            px.histogram,
            data_frame=df_tmp,
            x="branch",
            y="real_percent_profit",
            barmode="group",

            height=400,
            histfunc="avg",
            labels={"if_income": "Доходность", "branch": "Отрасль", "real_percent_profit": "(Средний процент, %)"},
        )

    def draw_branch_count(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp["if_good_idea"] = df_tmp["if_good_idea"].apply(lambda x: "Да" if x == True else "Нет")
        df_tmp = df_tmp.sort_values(by="branch", ascending=False)

        self.draw_plot_with_head(
            "Доля сбывшихся идей по отраслям",
            "",
            px.histogram,
            data_frame=df_tmp,
            x="branch",
            y="if_good_idea",
            color="if_good_idea",
            barmode="group",
            height=400,
            histfunc="count",
            histnorm="percent",
            color_discrete_map={
                "Нет": "#FF6347",
                "Да": "#66CDAA",
            },            
            labels={"branch":"Отрасль", "if_good_idea":"Доля, %"}
        )

    def draw_branch_channels(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp = df_tmp.sort_values(by="branch", ascending=False)

        self.draw_plot_with_head(
            "Доходность идей по отраслям и каналам",
            "Общий результат инвестирования во все идеи по отраслям в каждом из каналов",
            px.histogram,
            data_frame=df_tmp,
            x="branch",
            y="real_percent_profit",
            color="channel_name",
            barmode="group",
            height=400,

            histfunc="avg",
            labels={"channel_name": "Название канала", "branch": "Отрасль", "real_percent_profit": "(Средняя доходность, %)"},
        )

    def draw_year_bar_plot(self, df: pd.DataFrame) -> None:
        df_tmp = df.copy()
        df_tmp["year"] = df_tmp["message_date"].apply(lambda x: x.year)

        self.draw_plot_with_head(
            "Доходность идей по годам",
            "",
            px.histogram,
            data_frame=df_tmp,
            x="year",
            y="real_percent_profit",
            color="channel_name",
            barmode="group",
            height=400,
            histfunc="avg",
            labels={"channel_name": "Название канала", "year": "Год", "real_percent_profit": "(Средняя доходность, %)"},
        )

    def draw_ticker_plot(self, df: pd.DataFrame) -> None:
        st.subheader("Самые доходные и убыточные идеи по компаниям")
        df_tmp = df.copy()
        df_tmp["year"] = df_tmp["message_date"].apply(lambda x: x.year)
        df_tmp = (
            df_tmp[["ticker", "real_percent_profit"]]
            .groupby("ticker", as_index=False)
            .mean()
            .sort_values(by="real_percent_profit", ascending=False)
        )
        df_tmp["income"] = df_tmp["real_percent_profit"].apply(lambda x: "Доходная идея" if x > 0 else "Убыточная идея")

        self.draw_plot_with_head(
            "",
            "",
            px.histogram,
            data_frame=df_tmp,
            x="ticker",
            y="real_percent_profit",
            color="income",
            color_discrete_map={
                "Убыточная идея": "#FF6347",
                "Доходная идея": "#66CDAA",
            },
            labels={
                "income": "Результат",
                "ticker": "Тикер",
                "real_percent_profit": "(Средняя доходность, %)",
            },
        )

    def draw_absolute_income(self, df: pd.DataFrame) -> None:
        df_tmp = df[["message_date", "real_profit", "channel_name"]].copy()
        df_tmp["year"] = df_tmp["message_date"].apply(lambda x: x.year)

        self.draw_plot_with_head(
            "Доходность идей в рублях",
            "График демонстрирует доход/убыток при инвестиции в каждую идею канала в размере стоимости 1 акции эмитента, который указан в идее",
            px.histogram,
            data_frame=df_tmp,
            x="year",
            y="real_profit",
            color="channel_name",
            barmode="group",
            height=400,
            histfunc="sum",
            color_discrete_map={
                0.0: "#FF6347",
                1.0: "#66CDAA",
            },
            labels={"real_profit": "Сумма дохода(убытка)", "year": "Год", "channel_name": "Название канала"},
        )


class Areas(BasePlot):
    def __init__(self) -> None:
        super().__init__()

    def draw_price_income(self, df: pd.DataFrame) -> None:
        df_temp = df.copy()

        self.draw_plot_with_head(
            "Зависимость доходности от цены",
            "Есть ли зависимость фактического дохода по идее от стоимости бумаги?",
            px.scatter,
            data_frame=df_temp.sort_values(by="real_percent_profit"),
            x="real_percent_profit",
            y="current_price",
            color="channel_name",
            color_discrete_map={
                0.0: "#FF6347",
                1.0: "#66CDAA",
            },
            labels={
                "real_percent_profit": "Доходность, %",
                "current_price": "Начальная цена",
                "channel_name": "Название канала"
            },
        )

    def draw_time_income(self, df: pd.DataFrame) -> None:
        df_temp = df.copy()

        self.draw_plot_with_head(
            "Зависимость доходности от времени",
            "Зависимость фактической доходности от срока идеи",
            px.scatter,
            data_frame=df_temp.sort_values(by="real_percent_profit"),
            x="expectation_time",
            y="real_percent_profit",
            color="channel_name",
            color_discrete_map={
                0.0: "#FF6347",
                1.0: "#66CDAA",
            },
            labels={
                "real_percent_profit": "Доходность, %",
                "expectation_time": "Период идеи, дни",
                "channel_name": "Название канала"
            },
        )

    def draw_perc_income(self, df: pd.DataFrame) -> None:
        df_temp = df.copy()

        self.draw_plot_with_head(
            "Зависимость прогнозируемой доходности от начальной стоимости",
            "",
            px.scatter,
            data_frame=df_temp.sort_values(by="percentage"),
            x="current_price",
            y="percentage",
            color="channel_name",
            labels={
                "percentage": "Процент",
                "current_price": "Начальная стоимость, руб.",
                "channel_name": "Название канала"
            },
        )
