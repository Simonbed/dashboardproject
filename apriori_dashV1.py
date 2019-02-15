import pandas as pd

### With this apriori/mlxtend package, we can extract the support of the different items
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


### HERE WE PUT THE VALUES WE WANT TO SEE. We put the support and confidence threshold and we ask to arrange by lift if we want to see the end result.
support_threshold = 0.015
confidence_threshold = 0.01
value_arranged_by = "lift"  # "confidence" or "lift" strings work well here


database2 = pd.read_sas("data_du_menager.sas7bdat")
#print(database2)

dt = database2.groupby(["no_transaction"])["item"].apply(list) ## Group the items in transactions
#print(dt)


#### Apriori Algorithm - (Agrawal et Srikantt 1994)
#### STEP 1 - Fix minimal support and get a list for all mixes of items
te = TransactionEncoder()
te_data = te.fit(dt).transform(dt)
te_df = pd.DataFrame(te_data, columns=te.columns_)
support = apriori(te_df, min_support = support_threshold, use_colnames = True)

#print(support)  #prints out all of the supports we calculated.


#Prints out the top supports
resultsupport = support.sort_values(by=["support"], ascending = False) ### WE have the top support at the begining, but they are for single items
#print(resultsupport.head())

###Adding a lenght value in the result Pandas Database. This is useful as we will take the values above 1.
resultsupport['length'] = resultsupport['itemsets'].apply(lambda x: len(x))

### Now we can take the itemsets (2 or more together) that have high support enough
resultsupportmin2 = resultsupport[(resultsupport["length"]>=2)]
#print(resultsupportmin2)  ### This prints out the correct list of items


### I don't see the whole data, so we have to reformat PANDAS - This script works wonders for examining data
### =====This code I found online and did not write it, it has the perk of making print_full(pandasDF) show everything
def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 2000)
    pd.set_option('display.float_format', '{:20,.2f}'.format)
    pd.set_option('display.max_colwidth', -1)
    print(x)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
    pd.reset_option('display.width')
    pd.reset_option('display.float_format')
    pd.reset_option('display.max_colwidth')
###====


## This is the line that uses the confidence we have set at the start
from mlxtend.frequent_patterns import association_rules
confidence_support = association_rules(support, metric="confidence", min_threshold=confidence_threshold)
#print_full(confidence_support)

#This prints out the results by the top value arranged how we have set it.
resultsconfidence_support = confidence_support.sort_values(by=[value_arranged_by], ascending=False)

resultsconfidence_support['antecedents'] = resultsconfidence_support['antecedents'].astype(str)
resultsconfidence_support["consequents"] = resultsconfidence_support["consequents"].astype(str)

#print((resultsconfidence_support.to_dict("records")))


import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import dash.dependencies
from dash.dependencies import Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H2('Apriori Results'),
    dt.DataTable(
        id='my-datatable',
        rows=resultsconfidence_support.to_dict("records"),
        editable=False,
        row_selectable=True,
        filterable=True,
        sortable=True,
        selected_row_indices=[]
    ),
    html.Div(id='selected-indexes'),
    dcc.Graph(
        id='datatable-subplots'
    )
], style={'width': '100%'})

#app.layout = html.Div(children=[
#    html.Div(children='''
#        Enter the value you want to sort by:
#    '''),
#    dcc.Input(id='input', value='lift', type='text'),
#    html.Div(id='output-graph'),
#])

#@app.callback(
#    Output(component_id='output-graph', component_property='children'),
#    [Input(component_id='input', component_property='value')]
#)

#def update_value(input_data):
#    df = resultsconfidence_support

#    html.H1("Apriori Results"),
#    return dcc.Graph(
#        id="graph_one",
#        figure = {
#            "data" : [{"x": df.index.sort_values(by=[input_data]), "y": df.lift, "type" : "bar", "name" : "lift" }],
#            'layout': {
#                'title': input_data
#                }
#        })


if __name__ == "__main__":
    app.run_server(debug=True)
