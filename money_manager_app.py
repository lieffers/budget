import pandas as pd
import streamlit as st
import plotly.express as px

excel_file = 'Luke Money 2022.xlsx'
transactions_df = pd.read_excel(excel_file, sheet_name='Transactions', header=3, engine='openpyxl')
transactions_df = transactions_df.dropna(subset=['Account', 'Date'])
transactions_df['Date'] = pd.to_datetime(transactions_df['Date'])

st.sidebar.header("Filters")
selected_accounts = st.sidebar.multiselect("Select Account(s)", options=transactions_df['Account'].unique(), default=transactions_df['Account'].unique())
start_date = st.sidebar.date_input("Start Date", value=transactions_df['Date'].min())
end_date = st.sidebar.date_input("End Date", value=transactions_df['Date'].max())

filtered_df = transactions_df[
    (transactions_df['Account'].isin(selected_accounts)) &
    (transactions_df['Date'] >= pd.to_datetime(start_date)) &
    (transactions_df['Date'] <= pd.to_datetime(end_date))
]

st.title("💰 Money Manager App")
st.subheader("📋 Filtered Transaction History")
st.dataframe(filtered_df[['Account', 'Date', 'Category', 'PAYMENT', 'DEPOSIT']])

st.subheader("📊 Summary by Category")
summary_df = filtered_df.groupby('Category')[['PAYMENT', 'DEPOSIT']].sum().reset_index()
summary_df['Net'] = summary_df['DEPOSIT'] - summary_df['PAYMENT']
st.dataframe(summary_df)

fig = px.bar(summary_df, x='Category', y='Net', title='Net Amount by Category', labels={'Net': 'Net Amount', 'Category': 'Category'})
st.plotly_chart(fig)
