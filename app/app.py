"""Editorial dashboard for the verified PLFS aggregate outputs."""
from __future__ import annotations
import os
import sys
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

sys.path.insert(0,str(Path(__file__).resolve().parent))
from data import load_experiment, load_run, summarize
from insights import aggregate, age_standardized_sector, marital_by_age, education_by_sector
from style import inject_style

ROOT=Path(__file__).resolve().parents[1]
ARTIFACTS=Path(os.environ.get('PLFS_ARTIFACTS',str(ROOT/'artifacts')))
INK='#000000'; MUTED='#000000'; TEAL='#000000'; CORAL='#ff4332'; CREAM='#fff5d6'; LINE='#000000'
AGE=['15–24','25–34','35–44','45–54','55–64','65+']

st.set_page_config(page_title='PLFS • Women at work',page_icon='◒',layout='wide',initial_sidebar_state='collapsed')
inject_style()


def html(s):st.markdown(s,unsafe_allow_html=True)
def val(x):return f'{x:.1f}%'
def heading(kicker,title,deck=''):
    html(f'<div class="eyebrow">{kicker}</div>')
    st.header(title)
    if deck:html(f'<p class="deck">{deck}</p>')
def card(value,label):return f'<div class="stat"><div class="value">{value}</div><div class="label">{label}</div></div>'
def intro_card(number,title,body):
    return f'<div class="intro-card"><span class="num">{number}</span><h3>{title}</h3><p>{body}</p></div>'
def flow_step(number,title,body):
    return f'<div class="flow-step"><b>{number}</b><h3>{title}</h3><p>{body}</p></div>'
def requirement_row(number,title,evidence,status):
    return f'<div class="req-row"><div class="req-num">{number}</div><div class="req-main"><b>{title}</b><p>{evidence}</p></div><div class="req-status">{status}</div></div>'
def note(text):html(f'<div class="note">{text}</div>')
def caption(text):html(f'<div class="caption">{text}</div>')
def chart(fig,height=360):
    fig.update_layout(height=height,margin=dict(l=15,r=20,t=24,b=35),
                      paper_bgcolor='white',plot_bgcolor='white',font=dict(family='NeoBrutalismHost',color=INK,size=14),
                      legend=dict(orientation='h',y=1.13,x=0),hoverlabel=dict(bgcolor='white',font_color=INK))
    fig.update_xaxes(showgrid=False,zeroline=False,linecolor=LINE,linewidth=2,
                     tickfont=dict(color=INK,size=13),title_font=dict(color=INK,size=14))
    fig.update_yaxes(showgrid=True,gridcolor='#d9d9d9',zeroline=False,
                     tickfont=dict(color=INK,size=13),title_font=dict(color=INK,size=14))
    st.plotly_chart(fig,width='stretch',config={'displayModeBar':False})

def side_by_side(df,xcol):
    fig=go.Figure()
    for sector,color in [('Rural',TEAL),('Urban',CORAL)]:
        z=df[df.sector==sector].set_index(xcol).reindex(AGE)
        fig.add_scatter(x=AGE,y=z.rate,mode='lines+markers',name=sector,line=dict(color=color,width=3),
                        marker=dict(size=10,line=dict(color=INK,width=2)),customdata=z.n,
                        hovertemplate='%{x}<br>'+sector+': %{y:.1f}% working<br>Women surveyed: %{customdata:,}<extra></extra>')
    fig.update_yaxes(title='Estimated share working (%)',range=[0,76])
    fig.update_xaxes(title=None)
    return fig

def marital_chart(overall,by_age):
    subset=by_age[by_age.age_band=='25–34'].set_index('marital')
    names=['Currently married','Never married']
    fig=go.Figure()
    for label,color in [('All ages 15+',TEAL),('Age 25–34',CORAL)]:
        rates=[float(overall.loc[x,'weighted_share_pct']) if label=='All ages 15+' else float(subset.loc[x,'rate']) for x in names]
        fig.add_bar(name=label,x=names,y=rates,marker_color=color,marker_line_color=INK,marker_line_width=2,
                    text=[f'{x:.1f}%' for x in rates],textposition='outside')
    fig.update_layout(barmode='group',showlegend=True)
    fig.update_yaxes(title='Estimated share working (%)',range=[0,60])
    return fig

def education_chart(edu):
    selected=['Not literate','Postgraduate and above']
    fig=go.Figure()
    for sector,color in [('Rural',TEAL),('Urban',CORAL)]:
        z=edu[edu.sector==sector].set_index('education').loc[selected]
        fig.add_bar(name=sector,x=selected,y=z.rate,marker_color=color,marker_line_color=INK,marker_line_width=2,
                    text=[f'{x:.1f}%' for x in z.rate],textposition='outside',
                    customdata=z.n,hovertemplate='%{x}<br>'+sector+': %{y:.1f}% working<br>Women surveyed: %{customdata:,}<extra></extra>')
    fig.update_layout(barmode='group',showlegend=True)
    fig.update_yaxes(title='Estimated share working (%)',range=[0,68])
    return fig

def explore_chart(frame,column):
    d=frame.dropna(subset=['weighted_share_pct']).copy()
    if d.empty:
        st.info('These groups have fewer than 30 survey responses, so their rates are hidden.')
        return
    d=d.sort_values('weighted_share_pct',ascending=True)
    fig=go.Figure(go.Bar(x=d.weighted_share_pct,y=d[column],orientation='h',marker_color=TEAL,
                         marker_line_color=INK,marker_line_width=2,
                         text=[f'{v:.1f}%' for v in d.weighted_share_pct],textposition='outside',
                         customdata=d.n,hovertemplate='%{y}<br>Estimated share working: %{x:.1f}%<br>Women surveyed: %{customdata:,}<extra></extra>'))
    fig.update_xaxes(title='Estimated share working (%)',range=[0,110])
    fig.update_yaxes(title=None,showgrid=False)
    chart(fig,max(340,39*len(d)+100))

def score_chart(original,improved):
    keys=['accuracy','recall','f1','macro_f1']
    labels=['Correct overall','Working women found','F1 balance score','Both groups (F1)']
    fig=go.Figure()
    for name,m,color in [('First model',original,CORAL),('Improved model',improved,TEAL)]:
        values=[100*m[k] for k in keys]
        fig.add_bar(name=name,x=labels,y=values,marker_color=color,marker_line_color=INK,marker_line_width=2,
                    text=[f'{v:.1f}%' for v in values],textposition='outside')
    fig.update_layout(barmode='group')
    fig.update_yaxes(title='Score on test data (%)',range=[0,90])
    chart(fig,420)

def confusion(matrix,title):
    fig=px.imshow(matrix,x=['Predicted no','Predicted yes'],y=['Actual no','Actual yes'],text_auto=',d',
                  color_continuous_scale=[[0,'#ffffff'],[1,'#d4bdff']],aspect='auto')
    fig.update_layout(title=title,coloraxis_showscale=False)
    fig.update_xaxes(side='bottom')
    chart(fig,290)

html('<div class="brand"><div class="brand-name"><span class="brand-dot"></span>Women and work in India</div><div class="brand-meta">PLFS survey · 2023–24</div></div>')
page=st.radio('Section',['Project intro','The story','Explore the data','Model results','How we did it'],horizontal=True,label_visibility='collapsed')

try:run=load_run(ARTIFACTS)
except (OSError,ValueError,KeyError,TypeError) as exc:
    st.error(f'Saved results could not be loaded: {exc}');st.stop()
if run is None:
    st.info('No saved analysis results were found. Run `bash scripts/run-project.sh` first.');st.stop()
manifest,metrics,tables=run
experiment=load_experiment(ARTIFACTS,manifest['run_id'])
cube=tables.get('cube');minimum=int(manifest['min_cell_n'])
overview=tables['overview'].iloc[0]
sector=tables['by_sector'].set_index('sector')
raw_gap=float(sector.loc['Rural','weighted_share_pct']-sector.loc['Urban','weighted_share_pct'])
if cube is None:
    sector_age=tables['by_sector_age']
    standardized=manifest['age_standardized']
    marital_age=tables['by_marital_age']
    education_sector=tables['by_education_sector']
else:
    sector_age,standardized=age_standardized_sector(cube)
    marital_age=marital_by_age(cube)
    education_sector=education_by_sector(cube)
marital_overall=tables['by_marital'].set_index('marital')

if page=='Project intro':
    html('''<div class="intro-poster"><div class="kicker">Big Data Analytics mini-project · PLFS 2023–24</div>
    <h1>How does women’s work differ across India?</h1>
    <p>We studied women aged 15 or older in India’s labour force survey. Spark read the survey file from Hadoop storage, calculated employment estimates, and tested a prediction model. This dashboard explains the saved results.</p></div>''')
    heading('Why these tools?','What makes this a Big Data project?',
            'The course asks for an end-to-end cluster workflow: store the data, run analysis across workers, and explain the results. The CSV is about 119 MB—small enough for one laptop—but it contains 418,159 records and meets the course’s 10,000-record alternative.')
    html('<div class="intro-grid">'+
         intro_card('HDFS','Store the survey file','Hadoop Distributed File System stores the file in blocks. One NameNode keeps track of them; two DataNodes hold copies. The raw file passed the HDFS health check with two copies of its block.')+
         intro_card('YARN','Assign the work','YARN is the cluster scheduler. One ResourceManager assigns jobs, and two NodeManagers run the assigned tasks. The saved cluster check found both workers active.')+
         intro_card('SPARK','Calculate and model','Spark read the file from HDFS and ran on YARN. Spark SQL/DataFrames made the weighted tables; Spark MLlib trained and evaluated the prediction models.')+'</div>')
    note('All three Docker containers run on one Linux Mint laptop with 15 GiB of RAM. They demonstrate separate Hadoop services and job scheduling, but they do not provide protection against failure of the laptop or its disk.')
    heading('The steps','From survey file to dashboard',
            'The dashboard is the last step. It reads saved summaries; it does not run Hadoop or Spark when you open a page.')
    html('<div class="flow-grid">'+
         flow_step('01','Load','Stored the PLFS person CSV in HDFS and checked the health of its stored block.')+
         flow_step('02','Check','Selected women aged 15 or older and checked person keys, work-status codes, and survey weights.')+
         flow_step('03','Analyse','Ran Spark on YARN to make weighted group estimates and test MLlib models.')+
         flow_step('04','Explain','Exported aggregate tables, model scores, plots, the report, and this dashboard.')+'</div>')
    heading('Course checklist','How the six lab requirements are covered',
            'The project meets the six technical requirements in the supplied Big Data Analytics mini-project guidelines. These results come from the completed cluster runs.')
    html('<div class="req-list">'+
         requirement_row('1','Multi-node HDFS and YARN','One master runs NameNode and ResourceManager. Two workers each run DataNode and NodeManager. The recorded check showed two live DataNodes and two RUNNING NodeManagers.','Verified in saved check')+
         requirement_row('2','Data stored in HDFS and read by Spark','The 119,224,634-byte perv1.csv file was healthy in HDFS with replication factor 2. The successful Spark run names its HDFS input path.','Verified')+
         requirement_row('3','Spark jobs run on YARN','The main analysis succeeded as '+manifest['application_id']+' with master=yarn. The model improvement job also ran successfully on YARN.','Completed YARN runs')+
         requirement_row('4','At least two Spark components','The project uses Spark SQL/DataFrames for group tables and Spark MLlib for classification models.','Verified')+
         requirement_row('5','Enough data','The guideline says 500 MB <em>or</em> 10,000+ records. This CSV is about 119 MB, but has 418,159 records, so it qualifies through the record-count option.','Record-count rule met')+
         requirement_row('6','Original analysis and insights','The question is women’s usual-status work. The findings include an age-adjusted rural–urban comparison, a marital-status pattern within ages 25–34, and education-group differences.','Findings recorded')+'</div>')
    caption('Checklist source: the course-supplied “Mini Project Guidelines: Big Data Analytics” PDF. Survey source: MoSPI PLFS July 2023–June 2024.')

elif page=='The story':
    html(f'''<div class="hero"><div class="hero-top"><div class="hero-label">Women aged 15 or older · India · 2023–24</div><div class="hero-arrow" aria-hidden="true">↗</div></div>
    <div class="poster-strips"><span class="strip strip-white">SHARE OF WOMEN</span><span class="strip strip-black">WHO WORK</span></div>
    <h1>{val(float(overview['weighted_share_pct']))}</h1>
    <div class="hero-foot">Based on {int(overview['n']):,} women surveyed · Adjusted to represent India</div></div>
    <div class="hero-band"><p>About 4 in 10 women aged 15 or older were counted as working. The survey counts both main work and additional work, including unpaid work in a family business or farm. The percentage is adjusted to better represent India.</p><b>↓ What we found</b></div>''')
    html('<div class="statrow">'+card(val(float(sector.loc['Rural','weighted_share_pct'])),'Estimated share of rural women working')+
         card(val(float(sector.loc['Urban','weighted_share_pct'])),'Estimated share of urban women working')+
         card(f'{raw_gap:.1f}','Percentage-point difference: rural minus urban')+'</div>')
    note('<strong>How to read these numbers:</strong> A “survey response” is one woman in the sample. A “survey weight” adjusts for how people were selected, so the percentages estimate the wider population. “Percentage points” are the difference between two percentages—for example, about 46.5% minus 26.0% is 20.5 points.')
    heading('01 / age','The rural–urban difference stays large when ages are matched',
            'Rural and urban women have different ages. To check whether that explains the gap, we calculated both rates using the same mix of age groups.')
    left,right=st.columns([1.8,1],gap='large')
    with left:chart(side_by_side(sector_age,'age_band'),370)
    with right:
        html('<div class="feature"><strong>'+f'{raw_gap:.1f}'+'</strong><p>Percentage-point difference before matching ages</p></div>')
        html('<div class="feature"><strong>'+f"{standardized['Rural']-standardized['Urban']:.1f}"+'</strong><p>Percentage-point difference with the same age mix</p></div>')
        caption('The gap changes very little. Different age mixes do not explain most of it. This calculation does not tell us what causes the gap.')
    html('<div class="sectionline"></div>')
    heading('02 / marriage and age','The marriage pattern changes for women aged 25–34',
            'Across all adult ages, married women have the higher working share. Within ages 25–34, never-married women have the higher share.')
    left,right=st.columns([1.8,1],gap='large')
    with left:chart(marital_chart(marital_overall,marital_age),350)
    with right:
        marr=marital_age[(marital_age.age_band=='25–34')].set_index('marital')
        diff=float(marr.loc['Never married','rate']-marr.loc['Currently married','rate'])
        html('<div class="feature"><strong>'+f'{diff:.1f}'+'</strong><p>Percentage points higher for never-married women aged 25–34</p></div>')
        caption(f"This age group includes {int(marr.loc['Never married','n']):,} never-married and {int(marr.loc['Currently married','n']):,} married women in the survey. Their work rates differ; the data do not show that marriage caused the difference.")
    html('<div class="sectionline"></div>')
    heading('03 / education','The rural–urban difference varies by education',
            'The gap is large among women the survey records as “not literate”. It is much smaller among women with postgraduate education.')
    left,right=st.columns([1.8,1],gap='large')
    with left:chart(education_chart(education_sector),350)
    with right:
        ed=education_sector.set_index(['education','sector'])
        gap_low=float(ed.loc[('Not literate','Rural'),'rate']-ed.loc[('Not literate','Urban'),'rate'])
        gap_high=float(ed.loc[('Postgraduate and above','Rural'),'rate']-ed.loc[('Postgraduate and above','Urban'),'rate'])
        html('<div class="feature"><strong>'+f'{gap_low:.1f}'+'</strong><p>Percentage-point rural–urban gap: “not literate” group</p></div>')
        html('<div class="feature"><strong>'+f'{gap_high:.1f}'+'</strong><p>Percentage-point rural–urban gap: postgraduate group</p></div>')
        caption('The rural postgraduate group has 980 survey responses. These two education comparisons do not account for differences in age, state or other factors.')
    note('These comparisons show patterns, not causes. We did not calculate a margin of error, so the small difference among postgraduates does not prove that rural and urban rates are equal.')

elif page=='Explore the data':
    heading('Compare groups','Explore work rates for different women',
            'Choose what to compare. Each percentage uses survey weights to estimate the share for India.')
    note('The estimated percentage is adjusted for how people were selected for the survey. “Women surveyed” is the number of answers in this dataset, not the number of women in India.')
    options={'State or union territory':'state','Rural or urban':'sector','Age group':'age_band','Education':'education','Marital status':'marital'}
    compare_name=st.selectbox('Compare by',list(options),index=2)
    compare=options[compare_name]
    if cube is None:
        st.caption('This shareable version shows broad groups only. The detailed combined filters remain in the local project, where the internal joint table is kept.')
        groups=tables['by_'+('age' if compare=='age_band' else compare)].copy()
        n=int(tables['overview'].iloc[0]['n'])
        rate=float(tables['overview'].iloc[0]['weighted_share_pct'])
    else:
        with st.expander('Choose filters',expanded=True):
            columns=st.columns(3)
            selected={}
            for i,(label,col) in enumerate(options.items()):
                values=sorted(cube[col].dropna().unique().tolist())
                if col=='age_band':values=[x for x in AGE if x in values]
                with columns[i%3]:selected[col]=st.selectbox(label,['All']+values,key='filter_'+col)
        summary=summarize(cube,selected,minimum=minimum)
        if summary.empty:
            st.warning('No women in the survey match this combination. Try fewer filters.');st.stop()
        n=int(summary.iloc[0]['n']);rate=summary.iloc[0]['weighted_share_pct']
        groups=summarize(cube,selected,compare,minimum)
    html('<div class="statrow">'+card(f'{n:,}' if n>=minimum else f'&lt;{minimum}','Women in the selected survey group')+
         card(val(float(rate)) if pd.notna(rate) else 'Hidden','Estimated share working in this group')+
         card(f'{minimum}','Fewest responses needed to show a rate')+'</div>')
    if not groups.empty:
        explore_chart(groups,compare)
        show=groups.rename(columns={compare:compare_name,'n':'Women surveyed','small_cell':'Too few responses',
                                    'weighted_share_pct':'Estimated working share %','unweighted_share_pct':'Share within survey sample %'})
        if 'Too few responses' in show:
            show.loc[show['Too few responses'],'Women surveyed']=float('nan')
        st.dataframe(show,hide_index=True,width='stretch',column_config={
            'Estimated working share %':st.column_config.NumberColumn(format='%.1f%%'),
            'Share within survey sample %':st.column_config.NumberColumn(format='%.1f%%')})
        caption('The estimated share uses survey weights. The sample share is simply the percentage among the women interviewed in this group.')
        st.download_button('Download this table (CSV)',show.to_csv(index=False).encode(),
                           file_name='plfs-filtered-aggregates.csv',mime='text/csv')
    note(f'If fewer than {minimum} women match a group, we hide its count and percentage. Small groups can give misleading percentages. This simple rule does not replace a formal margin-of-error calculation or privacy review.')

elif page=='Model results':
    heading('Computer models','The improved model still misses many working women',
            'We tested whether a computer model could identify who the survey classified as working, using age, education, marital status and location. Some survey responses were set aside to test it. These scores are not employment rates for India.')
    base=metrics['baseline'];original=metrics['model'];improved=experiment[0]['model'] if experiment else None
    html('<div class="statrow">'+card(val(100*base['accuracy']),'Correct when always guessing “not working”')+
         card(val(100*original['accuracy']),'Correct with the first model')+
         card(val(100*improved['accuracy']) if improved else '—','Correct with the improved model')+'</div>')
    note('<strong>What do these scores mean?</strong> “Correct overall” is the share of all test predictions that were right. “Working women found” is the share of women who really had work that the model correctly identified. The F1 score balances finding working women with avoiding wrong “working” predictions. A high overall score can still hide many missed working women.')
    if improved:
        score_chart(original,improved)
        urban=improved['by_sector']['Urban']
        note(f"Among urban women who were actually working in the test data, the improved model found only {100*urban['recall']:.1f}%. It missed the rest. The higher overall score does not remove this weakness.")
        a,b=st.columns(2)
        st.write('The charts below count correct and incorrect predictions. “Yes” means the woman was classified as working; “no” means she was not.')
        with a:confusion(original['confusion_matrix'],'First model')
        with b:confusion(improved['confusion_matrix'],'Improved model')
        comparison=pd.DataFrame([{'Model':name,'Correct overall %':100*m['accuracy'],'Working women found %':100*m['recall'],
                                  'F1 balance score':m['f1'],'Both-group F1':m['macro_f1'],'ROC AUC':m.get('auc_roc'),'PR AUC':m.get('auc_pr')}
                                 for name,m in [('Always guess “not working”',base),('First model',original),('Improved model',improved)]])
        st.dataframe(comparison,hide_index=True,width='stretch')
        caption('F1 balances finding working women with avoiding false alarms. “Both-group F1” gives equal attention to working and not-working cases. ROC AUC and PR AUC show how well the model ranks cases across different cutoffs.')
        with st.expander('See the technical model comparison'):
            trials=pd.DataFrame([{'Candidate':x['candidate']['name'],'Validation accuracy %':100*x['validation']['accuracy'],
                                  'Validation employed recall %':100*x['validation']['recall'],
                                  'Validation macro F1':x['validation']['macro_f1']}
                                  for x in experiment[1]['trials']])
            st.dataframe(trials,hide_index=True,width='stretch')
            st.caption('Five models were compared using a separate validation group. The original test results had already been viewed before this later comparison, so it is not a completely new external test.')
    else:
        st.info('The later model results were not found. Only the first model is available.')
    caption(f"The test group contains {metrics['test_n']:,} people. People from the same household were kept together when splitting the data. The improved model was compared on a test group whose earlier results had already been seen, so this is a follow-up comparison rather than a fresh independent test.")

else:
    heading('How the study works','Where the numbers came from',
            'This page explains the survey, the meaning of “working,” and how the computer processed the answers. The dashboard shows saved results; it does not run the analysis again.')
    html('<div class="statrow">'+card(f"{manifest['audit']['raw_rows']:,}",'People in the source survey file')+
         card(f"{manifest['audit']['curated_rows']:,}",'Women aged 15 or older analysed')+
         card('2','Worker containers in the recorded Hadoop cluster')+'</div>')
    st.subheader('Words used in this dashboard')
    st.markdown('''- **PLFS:** India’s Periodic Labour Force Survey, run by the government to study work and employment. This project uses its July 2023–June 2024 first-visit data.
- **Working / employed:** a woman was counted as working if the survey recorded work as her usual main activity **or** as an additional activity. This includes paid work and some unpaid work in a family business or farm. “Not working” also includes people outside the labour force; it is **not** the unemployment rate.
- **Survey sample:** the people who answered the survey. The 160,042 women here are survey responses, not the number of women in India.
- **Survey weight:** a number assigned to each response to account for how the survey selected people. The dashboard uses these weights to estimate percentages for India.
- **Rural and urban:** the survey’s location groups—villages and towns/cities. “Not literate” is one of its recorded education groups.
- **Percentage point:** the difference between two percentages. For example, 46% minus 26% is a gap of 20 percentage points.''')
    st.subheader('How the analysis was done')
    st.markdown('''1. The survey file was stored in **HDFS**, the cluster’s shared file storage.
2. **Spark** read that file and cleaned the information needed for this question.
3. **YARN** gave Spark work to two worker containers on the same laptop.
4. Spark calculated the group percentages and tested the prediction models. This dashboard reads the saved summaries, not individual survey answers.''')
    st.subheader('How to understand the deeper comparisons')
    st.markdown('''- **Same age mix:** we asked what the rural and urban percentages would look like if both groups had the same distribution of ages. The gap stayed about the same. This is a comparison method, not proof of a cause.
- **Marriage and education charts:** these compare groups within the survey. Other differences between people may affect the result.
- **Model test:** we held back some households to check predictions. These model scores are **not** survey-weighted employment percentages.''')
    with st.expander('Exact survey and software rules for the project demo'):
        st.markdown('''- Worker status codes: `11, 12, 21, 31, 41, 51` in principal or subsidiary status. The technical name is **UPSS**: usual principal plus subsidiary status.
- Annual survey weight: `MULT / (100 if NSS == NSC else 200) / NO_QTR`.
- Weighted working share: `100 × sum(weight × working) / sum(weight)`.
- Spark SQL/DataFrames produced the group tables; Spark MLlib trained the models. Both ran on YARN. The age comparison uses the same pooled weighted age distribution for rural and urban women.''')
        st.code('PLFS person file → HDFS → Spark on YARN → checked women aged 15+ → group summaries and models → this dashboard',language='text')
    st.subheader('Saved evidence from the run')
    st.write('The saved record below identifies the successful Spark-on-YARN job and the HDFS file it read. It describes a completed run; it does not show whether the cluster is running right now.')
    st.json({k:manifest[k] for k in ['run_id','application_id','spark_version','master','input','hdfs_output','duration_seconds']},expanded=False)
    if experiment:st.caption(f"Later model comparison: YARN application {experiment[0]['application_id']} · {experiment[0]['selected']['name']}")
    with st.expander('Data checks from the completed run'):
        st.json(manifest['audit'])
    with st.expander('Terminal commands for the project demonstration'):
        st.code('bash scripts/verify.sh\nsudo docker compose exec -T --user hadoop master hdfs fsck /plfs/raw/perv1.csv -files -blocks -locations\nsudo docker compose exec -T --user hadoop master yarn application -status '+manifest['application_id']+'\npython3 scripts/show-results.py',language='bash')
    note('The dashboard does not check whether the cluster is running now. It also does not calculate margins of error, so small differences should be interpreted carefully.')

html('<div class="sectionline"></div>')
caption(f"Source: India’s PLFS survey, July 2023–June 2024. The story and comparison pages show survey-adjusted estimates; the model page shows prediction scores. Analysis run: {manifest['run_id']}.")
