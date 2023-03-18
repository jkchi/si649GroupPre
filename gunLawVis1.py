#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import altair as alt
import streamlit

#violenceLaw = pd.read_csv('GunViolenceLaw.csv',index_col=0)
#state_map = data.us_10m.url
#state_id = data.population_engineers_hurricanes()[['state', 'id']]
#violenceLaw = pd.merge(state_id, violenceLaw, how='inner', on = 'state')
#violenceLaw.to_csv('verson1.csv') 

state_map = 'https://cdn.jsdelivr.net/npm/vega-datasets@v1.29.0/data/us-10m.json'
violenceLaw = pd.read_csv('verson1.csv',index_col=0)
# In[5]:


yearList = list(violenceLaw['year'].unique())
click = alt.selection_multi(fields=['state'])

selectionGroupYear = alt.selection_single(
    fields=['year'],
    init={'year': yearList[0]},
    bind=alt.binding_select(options = yearList,name='Select year '),
    on="keyup",
    clear="false"
)

states = alt.topo_feature(state_map, 'states')

barTotal = alt.Chart(violenceLaw).transform_filter(
    alt.datum.GunDeathPer100k > violenceLaw['GunDeathPer100k'].median()
    ).mark_bar().encode(
    x=alt.X('TotalGunlaw',title='Number of Gun Law in Each State'),
    color='TotalGunlaw',
    tooltip =['state', 'TotalGunlaw','ChangeGunLaw'],
    opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
    y=alt.Y('state', sort='-x')).add_selection(selectionGroupYear,click
                           ).transform_filter(selectionGroupYear,).properties(
height = 400)



barChange = alt.Chart(violenceLaw).transform_filter(
    alt.datum.GunDeathPer100k > violenceLaw['GunDeathPer100k'].median() & alt.datum.ChangeGunLaw != 0
    ).mark_bar().encode(
    x = alt.X('ChangeGunLaw',title='Change of Law Compare to Last Year'),
    color='ChangeGunLaw',
    tooltip =['state', 'TotalGunlaw','ChangeGunLaw'],
    opacity=alt.condition(click, alt.value(1), alt.value(0.2)),
    y=alt.Y('state', sort='-x')).add_selection(selectionGroupYear,click
                           ).transform_filter(selectionGroupYear).properties(
height = 400)

map = alt.Chart(violenceLaw).mark_geoshape(stroke='#FFFFFF', strokeWidth=0.3
                           ).encode(alt.Color('GunDeathPer100k:Q',
                                              scale = alt.Scale(     
                                              range = ['white', 'red']
                                              ),
                                              #manual line switch zz
                                              legend = alt.Legend(title= ['Number of Gun related', 'Death per 100k Population'],titleLimit = 5000)),
                                              tooltip =['state', 'GunDeathPer100k','GunInjuryPer100k'],
                                              opacity=alt.condition(click, alt.value(1), alt.value(0.3))
                                              ).add_selection(selectionGroupYear,click
                           ).transform_filter(selectionGroupYear 
                           ).transform_lookup(lookup='id', 
                                              from_ = alt.LookupData(states, 
                                                                     key='id', 
                                                                     fields=["type", "properties", "geometry"])
                           ).project(type='albersUsa').properties(width=1000,
height=500, title = 'Gun Violence Situation in the US')


map2 = alt.Chart(violenceLaw).mark_geoshape(stroke='#FFFFFF', strokeWidth=0.3
                           ).encode(alt.Color('GunInjuryPer100k:Q',
                                              scale = alt.Scale(     
                                              range = ['white', 'red']
                                              ),
                                              #manual line switch zz
                                              legend = alt.Legend(title= ['Number of Gun related', 'Injury per 100k Population'],titleLimit = 5000)),
                                              tooltip =['state', 'GunInjuryPer100k','GunDeathPer100k'],
                                              opacity=alt.condition(click, alt.value(1), alt.value(0.3))
                                              ).add_selection(selectionGroupYear,click
                           ).transform_filter(selectionGroupYear 
                           ).transform_lookup(lookup='id', 
                                              from_ = alt.LookupData(states, 
                                                                     key='id', 
                                                                     fields=["type", "properties", "geometry"])
                           ).project(type='albersUsa').properties(width=1000,
height=500, title = 'Gun Violence Situation in the US')



g1 = (map & (barTotal | barChange).resolve_scale(
    color='independent',
    # noticing titlePadding will change the distance between GunDeath and bar
)).configure_legend(labelFontSize = 15 ,titleFontSize = 14, titlePadding = 20, titleAlign = 'left'  ).configure_axisX(labelFontSize = 15,titleFontSize = 18
                                                                                                                     ).configure_axisY(labelFontSize = 14,titleFontSize = 18
                                                                                                                     ).configure_title(fontSize = 40)

g2 = (map2 & (barTotal | barChange).resolve_scale(
    color='independent',
    # noticing titlePadding will change the distance between GunDeath and bar
)).configure_legend(labelFontSize = 15 ,titleFontSize = 14, titlePadding = 20, titleAlign = 'left'  ).configure_axisX(labelFontSize = 15,titleFontSize = 18
                                                                                                                     ).configure_axisY(labelFontSize = 14,titleFontSize = 18
                                                                                                                     ).configure_title(fontSize = 40)


tab1,tab2 = streamlit.tabs(['Gun Relatd Death','Gun Relatd Injury'])

with tab1:
    streamlit.altair_chart(g1, theme = None)

with tab2:
    streamlit.altair_chart(g2, theme = None)






