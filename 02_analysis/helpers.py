# Helper functions

import numpy as np
import pandas as pd

def amiBINS(df,col_in):
    df['pct_ami'] = df[col_in] / df['AMI']
    cond = [df['pct_ami']<=0.3,df['pct_ami']<=0.6,df['pct_ami']<=0.8,df['pct_ami']<=1,df['pct_ami']<=1.5,df['pct_ami']<=2,df['pct_ami']>2]
    choice = [0,1,2,3,4,5,6]
    # choice = ['0-30% AMI','30-60% AMI','60-80% AMI','80-100% AMI','100-150% AMI','150-200% AMI','200%+ AMI']
    df['ami_bin'] = np.select(condlist=cond,choicelist=choice,default=np.nan)
    # df['ami_bin'] = pd.Categorical(df['ami_bin'],choice)

def categorize_sign(df,col_prefixes,scenarios):
    for s in scenarios:
        for col in col_prefixes:
            df[f'sign_{col}{s}'] = np.select(condlist=[df[f'{col}{s}'].isna(),df[f'{col}{s}']<0,df[f'{col}{s}']>=0],choicelist=[np.nan,'Negative','Positive'])

def categorize_quantiles(res_dfs,scenario_names,units,which_results,burden_25th=0.02,burden_75th=0.04):
    cat_outputs = ['Low','Mid','High']
    for res_df in res_dfs:
        if 'burden_results' in which_results:
            # Current TEB
            cond_TEB_cat = [(res_df['burden'] <= burden_25th),((res_df['burden'] > burden_25th)&(res_df['burden'] <= burden_75th)),(res_df['burden'] > burden_75th)]
            res_df['cat_TEB'] = np.select(cond_TEB_cat,cat_outputs,None)
            res_df['cat_TEB'] = pd.Categorical(res_df['cat_TEB'],['Low','Mid','High'])

            # New TEB
            for s in scenario_names:
                TEB_BEV_label_cat = '_'.join(['cat_TEB_newBEV',s])
                TEB_ICEV_label_cat = '_'.join(['cat_TEB_newICEV',s])

                TEB_BEV_col = '_'.join(['TEB_newBEV',s])
                TEB_ICEV_col = '_'.join(['TEB_newICEV',s])
                # categorize based on current TEB thresholds
                cond_TEB_BEV_cat = [(res_df[TEB_BEV_col] <= burden_25th),((res_df[TEB_BEV_col] > burden_25th)&(res_df[TEB_BEV_col] <= burden_75th)),(res_df[TEB_BEV_col] > burden_75th)]
                cond_TEB_ICEV_cat = [(res_df[TEB_ICEV_col] <= burden_25th),((res_df[TEB_ICEV_col] > burden_25th)&(res_df[TEB_ICEV_col] <= burden_75th)),(res_df[TEB_ICEV_col] > burden_75th)]
                res_df[TEB_BEV_label_cat] = np.select(cond_TEB_BEV_cat,cat_outputs,np.nan)
                res_df[TEB_ICEV_label_cat] = np.select(cond_TEB_ICEV_cat,cat_outputs,np.nan)
                res_df[TEB_BEV_label_cat] = pd.Categorical(res_df[TEB_BEV_label_cat],['Low','Mid','High'])
                res_df[TEB_ICEV_label_cat] = pd.Categorical(res_df[TEB_ICEV_label_cat],['Low','Mid','High'])

        if 'ghg_cost_results' in which_results:
        # biv1 = lces + lfcs
        # biv2 = lces + burden savings
            for s in scenario_names:
                for u in units:
                    lces_label_r = '_'.join(['rk_lces',u,s])
                    lfcs_label_r = '_'.join(['rk_lfcs',u,s])
                    lces_label_cat = '_'.join(['cat_lces',u,s])
                    lfcs_label_cat = '_'.join(['cat_lfcs',u,s])
                    lces_col = res_df.columns[('lces' == res_df.columns.str[0:4]) & (res_df.columns.str.contains(s)) & (res_df.columns.str.contains(u))]
                    lfcs_col = res_df.columns[('lfcs' == res_df.columns.str[0:4]) & (res_df.columns.str.contains(s)) & (res_df.columns.str.contains(u))]
                    res_df[lces_label_r] = res_df[lces_col].rank(pct=True) * 100
                    res_df[lfcs_label_r] = res_df[lfcs_col].rank(pct=True) * 100
                    cond_lces = [(res_df[lces_label_r] <= 25),((res_df[lces_label_r] > 25)&(res_df[lces_label_r] <= 75)),(res_df[lces_label_r] > 75)]
                    cond_lfcs = [(res_df[lfcs_label_r] <= 25),((res_df[lfcs_label_r] > 25)&(res_df[lfcs_label_r] <= 75)),(res_df[lfcs_label_r] > 75)]
                    res_df[lces_label_cat] = np.select(cond_lces,cat_outputs,np.nan)
                    res_df[lfcs_label_cat] = np.select(cond_lfcs,cat_outputs,np.nan)
                    res_df[lces_label_cat] = pd.Categorical(res_df[lces_label_cat],['Low','Mid','High'])
                    res_df[lfcs_label_cat] = pd.Categorical(res_df[lfcs_label_cat],['Low','Mid','High'])
                    res_df['_'.join(['biv1_rk',u,s])] = res_df[lces_label_r] + res_df[lfcs_label_r]
                    res_df['_'.join(['biv1_cat',u,s])] = np.where((res_df[lces_label_cat].isna()),np.nan,res_df[lces_label_cat].astype(str) + '_' + res_df[lfcs_label_cat].astype(str))
                    if u == 'pHHy':
                        # Burden savings
                        burden_svgs_label_r = '_'.join(['rk_burden_svgs',s])
                        burden_svgs_label_cat = '_'.join(['cat_burden_svgs',s])
                        burden_svgs_col = '_'.join(['burden_svgs',s])
                        # categorize based on percentiles
                        res_df[burden_svgs_label_r] = res_df[burden_svgs_col].rank(pct=True) * 100
                        cond_BEV = [(res_df[burden_svgs_label_r] <= 25),((res_df[burden_svgs_label_r] > 25)&(res_df[burden_svgs_label_r] <= 75)),(res_df[burden_svgs_label_r] > 75)]
                        res_df[burden_svgs_label_cat] = np.select(cond_BEV,cat_outputs,np.nan)
                        # GHG and Burden savings rankings and quartile categories
                        res_df['_'.join(['biv2_rk',u,s])] = res_df[lces_label_r] + res_df[burden_svgs_label_r]
                        res_df['_'.join(['biv2_cat',u,s])] = np.where((res_df[lces_label_cat].isna()),np.nan,res_df[lces_label_cat].astype(str) + '_' + res_df[burden_svgs_label_cat].astype(str))

def fixGEOID(df,col_in,col_out,length):
    cond = [df[col_in].astype(str).str.len() == length]
    out = ['T' + df[col_in].astype(str)]
    df[col_out] = np.select(cond,out,('T0' + df[col_in].astype(str)))
    df[col_out] = df[col_out].astype('category')

def get_cols_pHHy_results(df):
    cols_pHHy = [x for x in df.columns.tolist() if ('vmt_wtd' in x) or ('hh_income_wtd' in x) or ('pHHy' in x) or ('burden_svgs' in x) or ('burden' in x) or ('TEB' in x)]
    return cols_pHHy

def state_county_FIPS(fips_state_file_path,fips_state_county_file_path):
    # US Census state and county fips data (downloaded from https://www.census.gov/library/reference/code-lists/ansi.html)
    # County FIPS and name changes documented here: https://www.cdc.gov/nchs/data/nvss/bridged_race/County-Geography-Changes-1990-present.pdf

    # state and state equivalents
    fips_state_dtype = {'STATE':object,'STUSAB':object,'STATE_NAME':object,'STATENS':object}
    fips_state = pd.read_csv(fips_state_file_path,delimiter='|',dtype=fips_state_dtype)
    fips_state.rename(columns={'STATE':'state_fips','STUSAB':'state','STATE_NAME':'state_name','STATENS':'statens'},inplace=True)
    fips_state['state_text'] = 'T' + fips_state.state_fips

    # county and county equivalents
    fips_state_county_dtype = {0:object,1:object,2:object,3:object,4:object}
    fips_state_county = pd.read_csv(fips_state_county_file_path,header=None,dtype=fips_state_county_dtype )
    fips_state_county_header = {0:'state',1:'state_fips',2:'county_fips',3:'county_name',4:'class_fips'}
    fips_state_county.rename(columns=fips_state_county_header,inplace=True)
    fips_state_county.loc[(fips_state_county['state_fips']=='02') & (fips_state_county['county_fips']=='270'),'county_fips'] = '158' # Effective July 1, 2015, Wade Hampton Census Area (FIPS code=02270) was renamed Kusilvak Census Area and assigned a new FIPS code
    fips_state_county.loc[(fips_state_county['state_fips']=='02') & (fips_state_county['county_fips']=='158'),'county_name'] = 'Kusilvak Census Area' # Effective July 1, 2015, Wade Hampton Census Area (FIPS code=02270) was renamed Kusilvak Census Area and assigned a new FIPS code
    fips_state_county.loc[(fips_state_county['state_fips']=='46') & (fips_state_county['county_fips']=='113'),'county_fips'] = '102' # Shannon County, SD renamed and renumbered in 2015
    fips_state_county.loc[(fips_state_county['state_fips']=='46') & (fips_state_county['county_fips']=='102'),'county_name'] = 'Oglala Lakota County' # Shannon County, SD renamed and renumbered in 2015
    fips_state_county = fips_state_county[(fips_state_county['state_fips']!='51') | (fips_state_county['county_fips']!='515')] # Bedford City (51515) merged with Bedford County in 2013, remove from dataset

    # add helper lookup columns
    fips_state_county['state_text'] = ('T' + fips_state_county.state_fips).astype('category')
    fips_state_county['county_text'] = ('T' + fips_state_county.state_fips + fips_state_county.county_fips).astype('category')
    fips_state_county['county'] = fips_state_county['county_name'].str.replace(' County','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' Parish','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' Census Area','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' City and Borough','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' Borough','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' Municipality','')
    fips_state_county['county'] = fips_state_county['county'].str.replace('St. ','St ',regex=True)
    fips_state_county['county'] = fips_state_county['county'].str.replace('Ste. ','Ste ',regex=True)
    fips_state_county['county'] = fips_state_county['county'].str.replace('Ste. ','Ste ',regex=True)
    fips_state_county['county'] = fips_state_county['county'].str.replace("'","")
    fips_state_county['county'] = fips_state_county['county'].str.replace('-','')
    fips_state_county['county'] = fips_state_county['county'].str.replace(' ','')
    fips_state_county['county_lwr'] = fips_state_county['county'].str.lower()

    # filter out territories
    fips_state_county = pd.DataFrame(fips_state_county.query('state != "AS" & state != "GU" & state != "MP" & state != "PR" & state != "UM" & state != "VI"'))
    # merge state name
    fips_state_county = fips_state_county.merge(fips_state[['state_name','state_text']],how='left',on='state_text',validate='many_to_one')
    
    return fips_state_county