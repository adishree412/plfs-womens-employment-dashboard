"""Read completed aggregate exports and recompute filtered shares from joint cells."""
import json
from pathlib import Path
import pandas as pd


def load_run(root):
    root=Path(root)
    pointer=root/'latest.json'
    if not pointer.exists():
        public=Path(__file__).resolve().parent/'public/results.json'
        if not public.exists():
            return None
        bundle=json.loads(public.read_text())
        manifest=bundle['manifest']
        if manifest.get('master')!='yarn' or not manifest.get('public_bundle'):
            raise ValueError('Unsupported public result bundle')
        tables={name:pd.DataFrame(rows) for name,rows in bundle['tables'].items()}
        return manifest,bundle['metrics'],tables
    run_id=json.loads(pointer.read_text())['run_id']
    if not isinstance(run_id,str) or not run_id or not all(c.isalnum() or c in '-_' for c in run_id):
        raise ValueError('Invalid run pointer')
    path=root/'runs'/run_id
    manifest=json.loads((path/'manifest.json').read_text())
    metrics=json.loads((path/'model_metrics.json').read_text())
    if manifest['master'] != 'yarn' or manifest['schema_version'] != 1:
        raise ValueError('Unsupported run')
    tables={n:pd.read_csv(path/(n+'.csv')) for n in manifest['aggregate_tables']}
    return manifest,metrics,tables


def load_experiment(root, source_run):
    """Find the newest completed model experiment linked to this analysis run."""
    root=Path(root)/'experiments'
    if not root.exists():
        public=Path(__file__).resolve().parent/'public/results.json'
        if public.exists():
            bundle=json.loads(public.read_text())
            if bundle['manifest']['run_id']==source_run:
                return bundle['experiment'],bundle['selection']
        return None
    matching=[]
    for path in root.iterdir():
        if not path.is_dir() or not all(c.isalnum() or c in '-_' for c in path.name):
            continue
        result_path=path/'result.json'
        selection_path=path/'selection.json'
        if not result_path.exists() or not selection_path.exists():
            continue
        try:
            result=json.loads(result_path.read_text())
            selection=json.loads(selection_path.read_text())
            if result.get('master')!='yarn' or not result.get('source_run','').endswith('/'+source_run):
                continue
            if result.get('run_id')!=path.name or 'model' not in result or 'trials' not in selection:
                continue
            matching.append((path.name,result,selection))
        except (OSError,ValueError,TypeError,KeyError):
            continue
    return max(matching,key=lambda x:x[0])[1:] if matching else None


def summarize(cube, selections, group=None, minimum=30):
    selected=cube
    for col,value in selections.items():
        if value != 'All':
            selected=selected[selected[col] == value]
    cols=['n','employed_n','weight_denominator','weighted_employed']
    if selected.empty:
        return pd.DataFrame()
    if group:
        result=selected.groupby(group,as_index=False,observed=True)[cols].sum()
    else:
        result=pd.DataFrame([selected[cols].sum()])
    result['small_cell']=result['n'] < minimum
    result['weighted_share_pct']=100*result.weighted_employed/result.weight_denominator
    result['unweighted_share_pct']=100*result.employed_n/result.n
    result.loc[result.small_cell,['weighted_share_pct','unweighted_share_pct']]=float('nan')
    # Do not expose sufficient statistics for suppressed cells in the download/UI.
    result=result.drop(columns=['employed_n','weighted_employed','weight_denominator'])
    return result
