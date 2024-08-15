import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
      page_title="Dasboard Loan", # mengubah judul nama tab
      page_icon="🤦‍♂️", # untuk ubah logo tab, teken logo windows dan titik
      layout='wide'
)

st.title("Financial Insights Dashboard: Loan Performance & Trends")

st.markdown("-------") # menambahkan garis

st.sidebar.header("Dashboard Filters and Features")

st.sidebar.markdown(
'''
- **Overview**: Provides a summary of key loan metrics.
- **Time-Based Analysis**: Shows trends over time and loan amounts.
- **Loan Performance**: Analyzes loan conditions and distributions.
- **Financial Analysis**: Examines loan amounts and distributions based on conditions.
'''
)

loan = pd.read_pickle('data_input/loan_clean')
loan['purpose']=loan['purpose'].str.replace("_", " ")

col1, col2 = st.columns(2) # mendefinisikan nama kolom
with st.container(border=True):
    with col1:
        st.metric('Total Loans', f"{loan['id'].count():,.0f}", help="Total Number of Loans")
        st.metric('Total Loans', f"{loan['loan_amount'].sum():,.0f}")

    with col2:
        st.metric('Average Interest Rate', f"{loan['loan_amount'].mean():,.2f}%")
        st.metric('Average Loan Amount', f"${loan['loan_amount'].mean():,.0f}")

tab1, tab2, tab3=st.tabs (['Loans Issued Over Time', 'Loan Amount Over Time', 'Issue Date Analysis'])

with tab1:
        loan_date_count = loan.groupby('issue_date')['loan_amount'].count()

        line_count=px.line(

        loan_date_count,
        markers=True,
        title="Number of Loans Issued Over Time",
        labels={
            'issue_date':'Issue Date',
            'value': 'number of loans'
        },
        ).update_layout(showlegend = False)
        st.plotly_chart(line_count)

with tab2:
        loan_date_sum = loan.groupby('issue_date')['loan_amount'].sum()
        line_sum=px.line(
        loan_date_sum,
        markers=True,
        labels={
            'value':'Number of Loans',
            'issue_date':'Issue Date'
        },
        template='seaborn',
        title="Loans Amount Over Time",
    ).update_layout(showlegend = False)
        st.plotly_chart(line_sum)

with tab3:
        loan_day_count = loan.groupby('issue_weekday')['loan_amount'].count()
        line_sum=px.bar(
        loan_day_count,
        category_orders= { # Mengatur urutan categori (hari)
            'issue_weekday': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        },
        title='Distribution of Loans by Day of the Week',
        labels={
            'value':'Number of Loans',
            'issue_weekday':'Day of the Week'
        },
        template='seaborn'
    ).update_layout(showlegend = False)
        st.plotly_chart(line_sum)

with st.expander("Click Here to Expand Visualization"):
        
    col3, col4 =st.columns(2)

    with col3:
        pie=px.pie(
        loan,
        names = 'loan_condition',
        hole = 0.4,
        title = "Distribution of Loans by Condition",
        template='seaborn'
    ).update_traces(textinfo='percent + value')
        st.plotly_chart(pie)

    with col4:
        grade = loan['grade'].value_counts().sort_index()
        pie=px.bar(
        grade,
        title= "Distribution of Loans by Grade",
        labels={
            'grade' : "Grade",
            'value' : "Number of Loans"
        }
    ).update_layout(showlegend = False)
        st.plotly_chart(pie)

condition=st.selectbox('Select Loan Condition', ['Good Loan', 'Bad Loan'])
loan_condition = loan[loan['loan_condition'] == condition]

with st.container(border=True):
    tab3, tab4 =st.tabs (['Loan Amount Distribution', 'Loan Amount Distribution by Purpose'])

    with tab3:
            Loan_Amount_Distribution=px.histogram(loan_condition,
                    x = 'loan_amount', color = 'term', nbins = 20,
                    title = 'Loan Amount Distribution',
                    template='seaborn',
            labels={
                'loan_amount':'Loan Amount',
                'term':'Loan Term'}
                    )
            st.plotly_chart(Loan_Amount_Distribution)

    with tab4:
            By_Purpose=px.box(
            loan_condition,
            x = 'purpose',
            y = 'loan_amount',
            color = 'term',
            color_discrete_sequence=['darkslateblue', 'tomato','lightblue'],
            title='Loan Amount Distribution by Purpose',
            labels={
                'loan_amount': 'Loan Amount',
                'term': 'Loan Term',
                'purpose': 'Loan Purpose'
            }
        )
            st.plotly_chart(By_Purpose)