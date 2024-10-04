"""
Exploratory Data Analysis (EDA) Module
--------------------------------------
해당 모듈은 데이터셋에 대한 EDA 분석을 수행하는 모듈입니다.
Documentation 및 예시로 작성해둔 Jupyter Notebook 파일을 참고하여 분석을 진행하시면 됩니다.
"""

import matplotlib.pyplot as plt
import pandas as pd

def auto_eda():
    """
    sweetviz를 활용한 Auto EDA 리포트를 html로 생성
    """
    pass

def auto_eda_comparison():
    """
    sweetviz를 활용한 Auto EDA 비교 리포트(ex. 데이터프레임의 sub segment)를 html로 생성
    """
    pass

def plot_pie_chart(df, label_column, size_column=None, colors=None, title="Pie Chart"):
    """
    plot_pie_chart 생성
    """

    # size_column이 지정되지 않은 경우 각 범주의 빈도수로 크기 계산
    if size_column:
        sizes = df[size_column]
    else:
        sizes = df[label_column].value_counts()

    labels = df[label_column].unique()

    # 파이 차트 생성
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

    # 파이 차트가 동그랗게 보이도록 설정
    plt.axis('equal')

    # 타이틀 추가
    plt.title(title)

    # 차트 보여주기
    plt.show()

def plot_grouped_donut_pie_chart(df, group_column, value_column, colors=None, title_prefix="Distribution for"):
    """
    plot_grouped_donut_pie_chart 생성
    """
    # 그룹별로 파이 차트를 그리기
    groups = df[group_column].unique()

    # # value_column에 대한 고정된 색상 설정
    # if colors is None:
    #     colors = ['#ff9999', '#66b3ff']  #  주황색,  파란색으로 설정

    for group in groups:
        # 그룹별 데이터 필터링
        group_data = df[df[group_column] == group]
        value_counts = group_data[value_column].value_counts().sort_index()  # Sort by index to ensure 0, 1 order

        # 파이 차트에 사용할 레이블과 값 설정
        labels = value_counts.index
        sizes = value_counts.values

        # 파이 차트 생성
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)

        # 도넛 차트를 위한 중앙 원 생성
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        plt.gca().add_artist(centre_circle)

        # 파이 차트가 동그랗게 보이도록 설정
        plt.axis('equal')

        # 그룹에 따른 차트 타이틀 추가
        plt.title(f'{title_prefix} {group}')

        # 차트 보여주기
        plt.show()

def plot_stacked_column_chart(df, category_column, stack_column, colors=None):
    """
    plot_stacked_column_chart 생성
    """
    # 범주형 열(category_column)과 스택 열(stack_column)을 기준으로 교차표 생성
    cross_tab = pd.crosstab(df[category_column], df[stack_column])

    # 기본 색상 설정 (색상이 지정되지 않은 경우)
    if colors is None:
        colors = plt.get_cmap('tab20').colors[:len(cross_tab.columns)]

    # 누적 막대 차트 생성
    cross_tab.plot(kind='bar', stacked=True, figsize=(10, 6), color=colors)

    # x축, y축 레이블 추가
    plt.xlabel(category_column)
    plt.ylabel('Count')

    # 범례(legend) 추가
    plt.legend(title=stack_column, loc='upper right')

    # 차트 보여주기
    plt.show()


def plot_heatmap():
    """
    plot_heatmap 생성
    """
    pass

def plot_treemap():
    """
    plot_treemap 생성
    """
    pass

def plot_trend_line_chart():
    """
    plot_trend_line_chart 생성
    """
    pass

def plot_multi_line_chart():
    """
    plot_multi_line_chart 생성
    """
    pass

def plot_area_chart():
    """
    plot_area_chart 생성
    """
    pass

def plot_stacked_area_chart():
    """
    plot_stacked_area_chart 생성
    """
    pass

def plot_spline_chart():
    """
    plot_spline_chart 생성
    """
    pass

def plot_single_value_card():
    """
    plot_single_value_card 생성
    """
    pass

def plot_table_chart():
    """
    plot_table_chart 생성
    """
    pass

def plot_gauge_chart():
    """
    plot_gauge_chart 생성
    """
    pass

def plot_histogram():
    """
    plot_histogram 생성
    """
    pass

def plot_box_plot():
    """
    plot_box_plot 생성
    """
    pass

def plot_violin_plot():
    """
    plot_violin_plot 생성
    """
    pass

def plot_density_plot():
    """
    plot_density_plot 생성
    """
    pass

def plot_bar_chart():
    """
    plot_bar_chart 생성
    """
    pass

def plot_column_chart():
    """
    plot_column_chart 생성
    """
    pass

def plot_connected_scatterplot():
    """
    plot_connected_scatterplot 생성
    """
    pass

def plot_scatter_plot():
    """
    plot_scatter_plot 생성
    """
    pass

def plot_bubble_chart():
    """
    plot_bubble_chart 생성
    """
    pass

def plot_wordcloud():
    """
    plot_wordcloud 생성
    """
    pass

def plot_sankey_chart():
    """
    plot_sankey_chart 생성
    """
    pass

def plot_chord_chart_hv():
    """
    plot_chord_chart_hv 생성
    """
    pass

def visualize_wordcloud_chart():
    """
    visualize_wordcloud_chart 생성
    """
    pass

def plot_chord_chart():
    """
    plot_chord_chart 생성
    """
    pass

def plot_network_flow():
    """
    plot_network_flow 생성
    """
    pass