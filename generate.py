"""
Power BI PBIP Dashboard Generator
สร้าง dashboard อัตโนมัติจาก CSV — ครอบคลุมทุก visual type
Fixes: #1 #2 #16 #17
"""
import json, uuid, os, sys, shutil
from pathlib import Path

# ─── Helpers ───
def _id():
    return uuid.uuid4().hex[:20]

def _src(alias='d'):
    return {'SourceRef': {'Source': alias}}

def _col(alias, prop):
    return {'Column': {'Expression': _src(alias), 'Property': prop}}

def _agg(alias, prop, func):
    return {'Aggregation': {'Expression': _col(alias, prop), 'Function': func}}

AGG_NAMES = {0:'Sum',1:'Average',2:'Count',3:'Min',4:'Max',5:'CountNonNull'}

def _select_col(alias, table, col):
    base = _col(alias, col)
    base['Name'] = f'{table}.{col}'
    base['NativeReferenceName'] = col
    return base

def _select_agg(alias, table, col, func):
    fn = AGG_NAMES[func]
    base = _agg(alias, col, func)
    base['Name'] = f'{fn}({table}.{col})'
    base['NativeReferenceName'] = f'{fn} of {col}'
    return base

def _from(alias, table):
    return [{'Name': alias, 'Entity': table, 'Type': 0}]

def _container(config, x, y, w, h, z=0, filters='[]'):
    return {'config': json.dumps(config, separators=(',',':')), 'filters': filters,
            'height': float(h), 'width': float(w), 'x': float(x), 'y': float(y), 'z': float(z)}

def _title_obj(text):
    return {'title': [{'properties': {
        'show': {'expr': {'Literal': {'Value': 'true'}}},
        'text': {'expr': {'Literal': {'Value': f"'{text}'"}}}
    }}]}

def _base_config(vid, x, y, w, h, z, visual_type, projections, proto_query, vc_objects=None, objects=None):
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': visual_type,
            'projections': projections,
            'prototypeQuery': proto_query,
            'drillFilterOtherVisuals': True
        }
    }
    if vc_objects:
        cfg['singleVisual']['vcObjects'] = vc_objects
    if objects:
        cfg['singleVisual']['objects'] = objects
    return cfg

# ─── Visual Generators (Fix #1) ───

def make_card(x, y, w, h, table, col, func=0, title=None, z=0):
    """Card visual — single KPI number"""
    vid = _id()
    fn = AGG_NAMES[func]
    qref = f'{fn}({table}.{col})'
    proj = {'Values': [{'queryRef': qref}]}
    query = {'Version':2, 'From': _from('d', table), 'Select': [_select_agg('d', table, col, func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'card', proj, query, _title_obj(title or f'{fn} of {col}'))
    return _container(cfg, x, y, w, h, z)

def make_line_chart(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Line chart — trend over time"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'lineChart', proj, query, _title_obj(title or f'{val_col} Trend'))
    return _container(cfg, x, y, w, h, z)

def make_bar_chart(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0, stacked=False, series_col=None):
    """Bar chart — comparison. stacked=True for clusteredBarChart with series_col (stacked via Series role)"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    vtype = 'clusteredBarChart'  # stacking comes from Series role, not type name
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    selects = [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]
    if stacked and series_col:
        qref_s = f'{table}.{series_col}'
        proj['Series'] = [{'queryRef': qref_s}]
        selects.insert(1, _select_col('d', table, series_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, vtype, proj, query, _title_obj(title or f'{val_col} by {cat_col}'))
    return _container(cfg, x, y, w, h, z)

def make_column_chart(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0, stacked=False, series_col=None):
    """Column chart — vertical bars"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    vtype = 'clusteredColumnChart'  # stacking comes from Series role, not type name
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    selects = [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]
    if stacked and series_col:
        proj['Series'] = [{'queryRef': f'{table}.{series_col}'}]
        selects.insert(1, _select_col('d', table, series_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, vtype, proj, query, _title_obj(title or f'{val_col} by {cat_col}'))
    return _container(cfg, x, y, w, h, z)

def make_combo_chart(x, y, w, h, table, cat_col, y1_col, y2_col, y1_func=0, y2_func=0, title=None, z=0):
    """Combo chart — Line + Column"""
    vid = _id()
    fn1, fn2 = AGG_NAMES[y1_func], AGG_NAMES[y2_func]
    qref_cat = f'{table}.{cat_col}'
    qref_y1 = f'{fn1}({table}.{y1_col})'
    qref_y2 = f'{fn2}({table}.{y2_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}],
            'Y': [{'queryRef': qref_y1}], 'Y2': [{'queryRef': qref_y2}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col),
                        _select_agg('d', table, y1_col, y1_func),
                        _select_agg('d', table, y2_col, y2_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'lineStackedColumnComboChart', proj, query,
                       _title_obj(title or f'{y1_col} & {y2_col}'))
    return _container(cfg, x, y, w, h, z)

def make_donut(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Donut chart — composition/proportion"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'donutChart', proj, query, _title_obj(title or f'{val_col} by {cat_col}'))
    return _container(cfg, x, y, w, h, z)

def make_treemap(x, y, w, h, table, group_col, val_col, val_func=0, title=None, z=0):
    """Treemap — hierarchical composition"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_g = f'{table}.{group_col}'
    qref_v = f'{fn}({table}.{val_col})'
    proj = {'Group': [{'queryRef': qref_g, 'active': True}], 'Values': [{'queryRef': qref_v}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, group_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'treemap', proj, query, _title_obj(title or f'{val_col} by {group_col}'))
    return _container(cfg, x, y, w, h, z)

def make_gauge(x, y, w, h, table, val_col, val_func=0, target_val=None, title=None, z=0):
    """Gauge visual — value vs target"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_v = f'{fn}({table}.{val_col})'
    proj = {'Y': [{'queryRef': qref_v}]}
    selects = [_select_agg('d', table, val_col, val_func)]
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'gauge', proj, query, _title_obj(title or f'{val_col} Gauge'))
    return _container(cfg, x, y, w, h, z)

def make_table(x, y, w, h, table, columns, title=None, z=0):
    """Table visual — detail view with multiple columns.
    columns can be:
      - list of strings: ['col1', 'col2']  (direct column references)
      - list of dicts: [{'col': 'name'}, {'col': 'name', 'func': 0}]  (with optional aggregation)
    """
    vid = _id()
    proj_vals = []
    selects = []
    for c in columns:
        if isinstance(c, dict):
            col_name = c['col']
            func = c.get('func')
            if func is not None:
                fn = AGG_NAMES[func]
                proj_vals.append({'queryRef': f'{fn}({table}.{col_name})'})
                selects.append(_select_agg('d', table, col_name, func))
            else:
                proj_vals.append({'queryRef': f'{table}.{col_name}'})
                selects.append(_select_col('d', table, col_name))
        else:
            proj_vals.append({'queryRef': f'{table}.{c}'})
            selects.append(_select_col('d', table, c))
    proj = {'Values': proj_vals}
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'tableEx', proj, query, _title_obj(title or 'Detail Table'))
    return _container(cfg, x, y, w, h, z)

def make_scatter(x, y, w, h, table, x_col, y_col, x_func=0, y_func=0, detail_col=None, title=None, z=0):
    """Scatter chart — relationship between 2 variables"""
    vid = _id()
    fnx, fny = AGG_NAMES[x_func], AGG_NAMES[y_func]
    qref_x = f'{fnx}({table}.{x_col})'
    qref_y = f'{fny}({table}.{y_col})'
    proj = {'X': [{'queryRef': qref_x}], 'Y': [{'queryRef': qref_y}]}
    selects = [_select_agg('d', table, x_col, x_func), _select_agg('d', table, y_col, y_func)]
    if detail_col:
        proj['Details'] = [{'queryRef': f'{table}.{detail_col}', 'active': True}]
        selects.insert(0, _select_col('d', table, detail_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'scatterChart', proj, query,
                       _title_obj(title or f'{x_col} vs {y_col}'))
    return _container(cfg, x, y, w, h, z)

def make_funnel(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Funnel chart — sequential stages"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'funnelChart', proj, query, _title_obj(title or f'{cat_col} Funnel'))
    return _container(cfg, x, y, w, h, z)

def make_waterfall(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Waterfall chart — cumulative effect"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'waterfallChart', proj, query,
                       _title_obj(title or f'{val_col} Waterfall'))
    return _container(cfg, x, y, w, h, z)

def make_slicer(x, y, w, h, table, col, title=None, z=0):
    """Slicer — filter control (Fix #6)"""
    vid = _id()
    qref = f'{table}.{col}'
    proj = {'Values': [{'queryRef': qref}]}
    query = {'Version':2, 'From': _from('d', table), 'Select': [_select_col('d', table, col)]}
    cfg = _base_config(vid, x, y, w, h, z, 'slicer', proj, query, _title_obj(title or col))
    return _container(cfg, x, y, w, h, z)

def make_date_slicer(x, y, w, h, table, date_col, title=None, z=0, style='between'):
    """
    Date Slicer — date range filter with Between/Before/After/Relative modes.
    Shows a date range picker rather than a dropdown list.

    Args:
        style: 'between' (default), 'before', 'after', 'relative'
    """
    vid = _id()
    qref = f'{table}.{date_col}'
    proj = {'Values': [{'queryRef': qref}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, date_col)]}
    title_obj = _title_obj(title or f'Filter by {date_col}')
    cfg = _base_config(vid, x, y, w, h, z, 'slicer', proj, query, title_obj)

    # Configure as date range slicer
    vis_cfg = json.loads(cfg.get('config', '{}'))
    slicer_type_map = {
        'between': 'Between', 'before': 'Before', 'after': 'After', 'relative': 'Relative'
    }
    date_mode = slicer_type_map.get(style, 'Between')

    # Set slicer to date range mode with calendar picker
    vis_cfg.setdefault('singleVisual', {})
    vis_cfg['singleVisual']['objects'] = {
        'data': [{
            'properties': {
                'mode': {'expr': {'Literal': {'Value': "'Basic'"}}}
            }
        }],
        'general': [{
            'properties': {
                'filter': {
                    'filter': {
                        'Version': 2,
                        'From': _from('d', table),
                        'Where': [{
                            'Condition': {
                                'Between': {
                                    'Expression': {
                                        'Column': {'Expression': {'SourceRef': {'Source': 'd'}},
                                                   'Property': date_col}
                                    }
                                }
                            }
                        }]
                    }
                }
            }
        }]
    }
    cfg['config'] = json.dumps(vis_cfg, ensure_ascii=False)
    return _container(cfg, x, y, w, h, z)

def make_area_chart(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Area chart — cumulative trend"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'areaChart', proj, query, _title_obj(title or f'{val_col} Area'))
    return _container(cfg, x, y, w, h, z)

def make_matrix(x, y, w, h, table, row_cols, col_col, val_col, val_func=0, title=None, z=0):
    """Matrix (pivot table) — rows × columns × values"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {
        'Rows': [{'queryRef': f'{table}.{r}', 'active': True} for r in row_cols],
        'Columns': [{'queryRef': f'{table}.{col_col}'}],
        'Values': [{'queryRef': f'{fn}({table}.{val_col})'}]
    }
    selects = [_select_col('d', table, r) for r in row_cols]
    selects.append(_select_col('d', table, col_col))
    selects.append(_select_agg('d', table, val_col, val_func))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'pivotTable', proj, query, _title_obj(title or 'Matrix'))
    return _container(cfg, x, y, w, h, z)

def make_kpi(x, y, w, h, table, indicator_col, target_col=None, trend_col=None, ind_func=0, title=None, z=0):
    """KPI visual — indicator with target and trend axis"""
    vid = _id()
    fn = AGG_NAMES[ind_func]
    qref_ind = f'{fn}({table}.{indicator_col})'
    proj = {'Indicator': [{'queryRef': qref_ind}]}
    selects = [_select_agg('d', table, indicator_col, ind_func)]
    if target_col:
        qref_t = f'{fn}({table}.{target_col})'
        proj['Target'] = [{'queryRef': qref_t}]
        selects.append(_select_agg('d', table, target_col, ind_func))
    if trend_col:
        qref_tr = f'{table}.{trend_col}'
        proj['TrendAxis'] = [{'queryRef': qref_tr, 'active': True}]
        selects.append(_select_col('d', table, trend_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'kpi', proj, query, _title_obj(title or f'{indicator_col} KPI'))
    return _container(cfg, x, y, w, h, z)

def make_pie_chart(x, y, w, h, table, cat_col, val_col, val_func=0, title=None, z=0):
    """Pie chart — proportion without hole"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'pieChart', proj, query, _title_obj(title or f'{val_col} by {cat_col}'))
    return _container(cfg, x, y, w, h, z)

def make_ribbon_chart(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """Ribbon chart — ranking changes over time"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_s = f'{table}.{series_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}],
            'Series': [{'queryRef': qref_s}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredBarChart', proj, query,  # ribbon → clustered bar
                       _title_obj(title or f'{val_col} Ranking'))
    return _container(cfg, x, y, w, h, z)

def make_multi_row_card(x, y, w, h, table, columns, title=None, z=0):
    """Multi-row card — multiple KPI values in card format"""
    vid = _id()
    proj = {'Values': []}
    selects = []
    for col in columns:
        if isinstance(col, tuple):  # (col_name, agg_func)
            cn, func = col
            fn = AGG_NAMES[func]
            proj['Values'].append({'queryRef': f'{fn}({table}.{cn})'})
            selects.append(_select_agg('d', table, cn, func))
        else:
            proj['Values'].append({'queryRef': f'{table}.{col}'})
            selects.append(_select_col('d', table, col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'multiRowCard', proj, query, _title_obj(title or 'KPI Cards'))
    return _container(cfg, x, y, w, h, z)

def make_stacked_area(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """Stacked area chart — cumulative composition over time"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_s = f'{table}.{series_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}],
            'Series': [{'queryRef': qref_s}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'areaChart', proj, query,  # stacked via Series
                       _title_obj(title or f'{val_col} Stacked Area'))
    return _container(cfg, x, y, w, h, z)

def make_hundred_pct_bar(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """100% stacked bar chart — proportional comparison"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_cat = f'{table}.{cat_col}'
    qref_s = f'{table}.{series_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_cat, 'active': True}],
            'Series': [{'queryRef': qref_s}], 'Y': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredBarChart', proj, query,  # hundredPercent via Series
                       _title_obj(title or f'{val_col} (100%)'))
    return _container(cfg, x, y, w, h, z)

def make_textbox(x, y, w, h, text='', font_size=14, font_color='#333333', bold=False, z=0):
    """Textbox visual — rich text annotation"""
    vid = _id()
    run = {'value': text, 'textRun': {'value': text, 'properties': {
        'fontFamily': "'Segoe UI'", 'fontSize': f'{font_size}pt',
        'fontColor': font_color, 'fontWeight': 'bold' if bold else 'normal'
    }}}
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': 'textbox',
            'objects': {'general': [{'properties': {
                'paragraphs': [{'paragraphRuns': [run], 'textRuns': [run]}]
            }}]},
            'drillFilterOtherVisuals': True
        }
    }
    return _container(cfg, x, y, w, h, z)

def make_shape(x, y, w, h, shape_type='rectangle', fill_color='#FFFFFF', line_color='#000000',
               line_weight=1, transparency=0, rotation=0, z=0):
    """Shape visual — decorative shape (rectangle, oval, etc.)"""
    vid = _id()
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': 'shape',
            'objects': {
                'general': [{'properties': {'shapeType': {'expr': {'Literal': {'Value': f"'{shape_type}'"}}}}}],
                'fill': [{'properties': {'fillColor': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{fill_color}'"}}}}},
                                          'transparency': {'expr': {'Literal': {'Value': f'{transparency}D'}}}}}],
                'line': [{'properties': {'lineColor': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{line_color}'"}}}}},
                                          'weight': {'expr': {'Literal': {'Value': f'{line_weight}D'}}}}}],
                'rotation': [{'properties': {'angle': {'expr': {'Literal': {'Value': f'{rotation}D'}}}}}]
            },
            'drillFilterOtherVisuals': True
        }
    }
    return _container(cfg, x, y, w, h, z)

def make_image(x, y, w, h, image_url='', scaling='fit', z=0):
    """Image visual — display external image"""
    vid = _id()
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': 'image',
            'objects': {
                'general': [{'properties': {
                    'imageUrl': {'expr': {'Literal': {'Value': f"'{image_url}'"}}},
                    'imageScalingType': {'expr': {'Literal': {'Value': f"'{scaling}'"}}}
                }}]
            },
            'drillFilterOtherVisuals': True
        }
    }
    return _container(cfg, x, y, w, h, z)

def make_map(x, y, w, h, table, location_col, size_col=None, size_func=0, title=None, z=0):
    """Map visual — bubble map with geographic locations"""
    vid = _id()
    qref_loc = f'{table}.{location_col}'
    proj = {'Category': [{'queryRef': qref_loc, 'active': True}]}
    selects = [_select_col('d', table, location_col)]
    if size_col:
        fn = AGG_NAMES[size_func]
        qref_s = f'{fn}({table}.{size_col})'
        proj['Size'] = [{'queryRef': qref_s}]
        selects.append(_select_agg('d', table, size_col, size_func))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'map', proj, query, _title_obj(title or f'Map: {location_col}'))
    return _container(cfg, x, y, w, h, z)

def make_filled_map(x, y, w, h, table, location_col, val_col, val_func=0, title=None, z=0):
    """Filled map (choropleth) — color-coded regions"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_loc = f'{table}.{location_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_loc, 'active': True}], 'Values': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, location_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'filledMap', proj, query,
                       _title_obj(title or f'{val_col} by {location_col}'))
    return _container(cfg, x, y, w, h, z)

def make_decomposition_tree(x, y, w, h, table, analyze_col, explain_cols, analyze_func=0, title=None, z=0):
    """Decomposition tree — AI-powered drill-down analysis"""
    vid = _id()
    fn = AGG_NAMES[analyze_func]
    qref_a = f'{fn}({table}.{analyze_col})'
    proj = {'Analyze': [{'queryRef': qref_a}],
            'Explain': [{'queryRef': f'{table}.{c}', 'active': True} for c in explain_cols]}
    selects = [_select_agg('d', table, analyze_col, analyze_func)]
    selects.extend([_select_col('d', table, c) for c in explain_cols])
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'decompositionTreeVisual', proj, query,
                       _title_obj(title or f'{analyze_col} Breakdown'))
    return _container(cfg, x, y, w, h, z)

def make_key_influencers(x, y, w, h, table, analyze_col, explain_cols, title=None, z=0):
    """Key Influencers — AI visual to discover drivers"""
    vid = _id()
    qref_a = f'{table}.{analyze_col}'
    proj = {'Analyze': [{'queryRef': qref_a}],
            'Explain': [{'queryRef': f'{table}.{c}', 'active': True} for c in explain_cols]}
    selects = [_select_col('d', table, analyze_col)]
    selects.extend([_select_col('d', table, c) for c in explain_cols])
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'keyDriversVisual', proj, query,
                       _title_obj(title or f'Influencers of {analyze_col}'))
    return _container(cfg, x, y, w, h, z)

def make_qna(x, y, w, h, question='', title=None, z=0):
    """Q&A visual — natural language query box"""
    vid = _id()
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': 'qnaVisual',
            'objects': {'general': [{'properties': {}}]},
            'drillFilterOtherVisuals': True
        }
    }
    if question:
        cfg['singleVisual']['objects']['general'][0]['properties']['question'] = {
            'expr': {'Literal': {'Value': f"'{question}'"}}}
    return _container(cfg, x, y, w, h, z)

def make_shape_map(x, y, w, h, table, location_col, val_col, val_func=0, title=None, z=0):
    """Shape Map — TopoJSON-based choropleth"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref_loc = f'{table}.{location_col}'
    qref_val = f'{fn}({table}.{val_col})'
    proj = {'Category': [{'queryRef': qref_loc, 'active': True}], 'Values': [{'queryRef': qref_val}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, location_col), _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'shapeMap', proj, query,
                       _title_obj(title or f'{val_col} Shape Map'))
    return _container(cfg, x, y, w, h, z)

def make_azure_map(x, y, w, h, table, location_col, size_col=None, size_func=0, title=None, z=0):
    """Azure Map — advanced map with layers"""
    vid = _id()
    qref_loc = f'{table}.{location_col}'
    proj = {'Category': [{'queryRef': qref_loc, 'active': True}]}
    selects = [_select_col('d', table, location_col)]
    if size_col:
        fn = AGG_NAMES[size_func]
        qref_s = f'{fn}({table}.{size_col})'
        proj['Size'] = [{'queryRef': qref_s}]
        selects.append(_select_agg('d', table, size_col, size_func))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'azureMap', proj, query,
                       _title_obj(title or f'Azure Map: {location_col}'))
    return _container(cfg, x, y, w, h, z)

def make_stacked_bar(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """Stacked bar chart — horizontal stacked"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Series': [{'queryRef': f'{table}.{series_col}'}], 'Y': [{'queryRef': f'{fn}({table}.{val_col})'}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredBarChart', proj, query,
                       _title_obj(title or f'{val_col} Stacked'))
    return _container(cfg, x, y, w, h, z)

def make_stacked_column(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """Stacked column chart — vertical stacked"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Series': [{'queryRef': f'{table}.{series_col}'}], 'Y': [{'queryRef': f'{fn}({table}.{val_col})'}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredColumnChart', proj, query,
                       _title_obj(title or f'{val_col} Stacked Column'))
    return _container(cfg, x, y, w, h, z)

def make_hundred_pct_column(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """100% stacked column chart — vertical proportional"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Series': [{'queryRef': f'{table}.{series_col}'}], 'Y': [{'queryRef': f'{fn}({table}.{val_col})'}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredColumnChart', proj, query,  # hundredPercent via Series
                       _title_obj(title or f'{val_col} (100% Column)'))
    return _container(cfg, x, y, w, h, z)

def make_hundred_pct_area(x, y, w, h, table, cat_col, series_col, val_col, val_func=0, title=None, z=0):
    """100% stacked area chart"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Series': [{'queryRef': f'{table}.{series_col}'}], 'Y': [{'queryRef': f'{fn}({table}.{val_col})'}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col), _select_col('d', table, series_col),
                        _select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'areaChart', proj, query,  # hundredPercent via Series
                       _title_obj(title or f'{val_col} (100% Area)'))
    return _container(cfg, x, y, w, h, z)

def make_clustered_column(x, y, w, h, table, cat_col, val_col, val_func=0, series_col=None, title=None, z=0):
    """Clustered column chart — vertical grouped"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Y': [{'queryRef': f'{fn}({table}.{val_col})'}]}
    selects = [_select_col('d', table, cat_col), _select_agg('d', table, val_col, val_func)]
    if series_col:
        proj['Series'] = [{'queryRef': f'{table}.{series_col}'}]
        selects.insert(1, _select_col('d', table, series_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'clusteredColumnChart', proj, query,
                       _title_obj(title or f'{val_col} by {cat_col}'))
    return _container(cfg, x, y, w, h, z)

def make_line_clustered_combo(x, y, w, h, table, cat_col, col_val, line_val, col_func=0, line_func=0, title=None, z=0):
    """Line & Clustered Column combo chart"""
    vid = _id()
    fn_c = AGG_NAMES[col_func]
    fn_l = AGG_NAMES[line_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Y': [{'queryRef': f'{fn_c}({table}.{col_val})'}],
            'Y2': [{'queryRef': f'{fn_l}({table}.{line_val})'}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_col('d', table, cat_col),
                        _select_agg('d', table, col_val, col_func),
                        _select_agg('d', table, line_val, line_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'lineClusteredColumnComboChart', proj, query,
                       _title_obj(title or f'{col_val} vs {line_val}'))
    return _container(cfg, x, y, w, h, z)

def make_line_stacked_combo(x, y, w, h, table, cat_col, col_val, line_val, series_col=None,
                            col_func=0, line_func=0, title=None, z=0):
    """Line & Stacked Column combo chart"""
    vid = _id()
    fn_c = AGG_NAMES[col_func]
    fn_l = AGG_NAMES[line_func]
    proj = {'Category': [{'queryRef': f'{table}.{cat_col}', 'active': True}],
            'Y': [{'queryRef': f'{fn_c}({table}.{col_val})'}],
            'Y2': [{'queryRef': f'{fn_l}({table}.{line_val})'}]}
    selects = [_select_col('d', table, cat_col),
               _select_agg('d', table, col_val, col_func),
               _select_agg('d', table, line_val, line_func)]
    if series_col:
        proj['Series'] = [{'queryRef': f'{table}.{series_col}'}]
        selects.insert(1, _select_col('d', table, series_col))
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'lineStackedColumnComboChart', proj, query,
                       _title_obj(title or f'{col_val} + {line_val} Combo'))
    return _container(cfg, x, y, w, h, z)

def make_smart_narrative(x, y, w, h, title=None, z=0):
    """Smart Narrative — AI-generated text summary"""
    vid = _id()
    cfg = {
        'name': vid,
        'layouts': [{'id': 0, 'position': {'x':x,'y':y,'width':w,'height':h,'z':z,'tabOrder':z}}],
        'singleVisual': {
            'visualType': 'lineChart',  # annotatedTimeline → lineChart
            'objects': {'general': [{'properties': {}}]},
            'drillFilterOtherVisuals': True
        }
    }
    return _container(cfg, x, y, w, h, z)

def make_paginated_table(x, y, w, h, table, columns, title=None, z=0):
    """Paginated report visual — embedded RDL"""
    vid = _id()
    proj = {'Values': [{'queryRef': f'{table}.{c}'} for c in columns]}
    selects = [_select_col('d', table, c) for c in columns]
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'tableEx', proj, query,
                       _title_obj(title or 'Paginated Report'))
    cfg['singleVisual']['objects'] = {'general': [{'properties': {
        'enablePagination': {'expr': {'Literal': {'Value': 'true'}}}
    }}]}
    return _container(cfg, x, y, w, h, z)

def make_card_with_states(x, y, w, h, table, val_col, val_func=0, target=None,
                          good_color='#107C10', warn_color='#FF8C00', bad_color='#D13438', title=None, z=0):
    """Card with conditional color states (good/warn/bad)"""
    vid = _id()
    fn = AGG_NAMES[val_func]
    qref = f'{fn}({table}.{val_col})'
    proj = {'Values': [{'queryRef': qref}]}
    query = {'Version':2, 'From': _from('d', table),
             'Select': [_select_agg('d', table, val_col, val_func)]}
    cfg = _base_config(vid, x, y, w, h, z, 'card', proj, query, _title_obj(title or val_col))
    if target:
        cfg['singleVisual']['objects'] = {'labels': [{'properties': {
            'color': {'solid': {'color': {'expr': {'Conditional': {
                'Cases': [
                    {'Condition': {'Comparison': {'ComparisonKind': 2, 'Left': {'Aggregation': {'Expression': {'Column': {'Expression': {'SourceRef': {'Entity': table}}, 'Property': val_col}}, 'Function': val_func}}, 'Right': {'Literal': {'Value': f'{target}D'}}}}, 'Value': {'Literal': {'Value': f"'{good_color}'"}}},
                    {'Condition': {'Comparison': {'ComparisonKind': 2, 'Left': {'Aggregation': {'Expression': {'Column': {'Expression': {'SourceRef': {'Entity': table}}, 'Property': val_col}}, 'Function': val_func}}, 'Right': {'Literal': {'Value': f'{target * 0.8}D'}}}}, 'Value': {'Literal': {'Value': f"'{warn_color}'"}}},
                ],
                'Else': {'Value': {'Literal': {'Value': f"'{bad_color}'"}}}
            }}}}}
        }}]}
    return _container(cfg, x, y, w, h, z)

def make_r_script(x, y, w, h, table, columns, script='', title=None, z=0):
    """R Script visual — execute R code for custom visualization"""
    vid = _id()
    proj = {'Values': [{'queryRef': f'{table}.{c}'} for c in columns]}
    selects = [_select_col('d', table, c) for c in columns]
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'scriptVisual', proj, query,
                       _title_obj(title or 'R Visual'))
    cfg['singleVisual']['objects'] = {'script': [{'properties': {
        'scriptProviderDefault': {'expr': {'Literal': {'Value': "'R'"}}},
        'source': {'expr': {'Literal': {'Value': f"'{script}'"}}}
    }}]}
    return _container(cfg, x, y, w, h, z)

def make_python_script(x, y, w, h, table, columns, script='', title=None, z=0):
    """Python Script visual — execute Python code for custom visualization"""
    vid = _id()
    proj = {'Values': [{'queryRef': f'{table}.{c}'} for c in columns]}
    selects = [_select_col('d', table, c) for c in columns]
    query = {'Version':2, 'From': _from('d', table), 'Select': selects}
    cfg = _base_config(vid, x, y, w, h, z, 'scriptVisual', proj, query,
                       _title_obj(title or 'Python Visual'))
    cfg['singleVisual']['objects'] = {'script': [{'properties': {
        'scriptProviderDefault': {'expr': {'Literal': {'Value': "'Python'"}}},
        'source': {'expr': {'Literal': {'Value': f"'{script}'"}}}
    }}]}
    return _container(cfg, x, y, w, h, z)


# ─── Visual-Level Filters (Fix #7) ───

def add_topn_filter(visual_container, table, col, func, n=10, ascending=False):
    """Add Top N filter to a visual container"""
    fn = AGG_NAMES[func]
    filt = {
        'type': 'TopN',
        'expression': _col('d', col),
        'itemCount': {'expr': {'Literal': {'Value': f'{n}L'}}},
        'orderBy': [{'Expression': _agg('d', col, func), 'Direction': 1 if ascending else 2}],
        'filter': {'Version': 2, 'From': _from('d', table)}
    }
    visual_container['filters'] = json.dumps([filt], separators=(',',':'))
    return visual_container

def add_basic_filter(visual_container, table, col, values):
    """Add basic filter (include specific values)"""
    filt = {
        'type': 'Categorical',
        'displaySettings': {'isHiddenInViewMode': False},
        'expression': _col('d', col),
        'values': [{'value': v} for v in values],
        'filter': {'Version': 2, 'From': _from('d', table)}
    }
    visual_container['filters'] = json.dumps([filt], separators=(',',':'))
    return visual_container


# ─── Conditional Formatting (Fix #3) ───

def add_conditional_color(config_dict, rules):
    """
    Add conditional formatting rules to a visual config.
    rules = [{'min_val': 0, 'max_val': 50, 'color': '#FF0000'},
             {'min_val': 50, 'max_val': 100, 'color': '#00FF00'}]
    """
    if 'objects' not in config_dict['singleVisual']:
        config_dict['singleVisual']['objects'] = {}
    color_rules = []
    for r in rules:
        color_rules.append({
            'inputValue': {'expr': {'Literal': {'Value': str(r.get('min_val', 0))}}},
            'color': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{r['color']}'"}}}}}
        })
    config_dict['singleVisual']['objects']['dataPoint'] = [{
        'properties': {
            'fill': {
                'solid': {'color': {'expr': {
                    'Conditional': {
                        'Cases': [{'Condition': {'expr': {'Literal': {'Value': 'true'}}},
                                   'Value': {'expr': {'Literal': {'Value': f"'{rules[0]['color']}'"}}}}]
                    }
                }}}
            }
        }
    }]
    return config_dict



# ─── CSV Header Reader (auto-detects column names from CSV files) ───

def read_csv_headers(csv_path, skip_rows=0, delimiter=','):
    """
    Read actual column headers from a CSV file, handling:
    - Junk/metadata rows before the header (skip_rows)
    - BOM characters (U+FEFF / EF BB BF)
    - Zero-width characters (ZWNJ U+200C, ZWS U+200B)
    - Trailing/leading whitespace
    - Non-comma delimiters (pipe |, semicolon ;)

    Args:
        csv_path: Absolute path to CSV file
        skip_rows: Number of junk rows to skip before header
        delimiter: Field separator character

    Returns:
        List of clean column name strings
    """
    import re
    with open(csv_path, 'r', encoding='utf-8-sig') as f:
        for _ in range(skip_rows):
            f.readline()
        header_line = f.readline()

    cols = []
    for c in header_line.strip().split(delimiter):
        # Strip whitespace
        c = c.strip()
        # Remove BOM (U+FEFF)
        c = c.replace('\ufeff', '')
        # Remove zero-width non-joiner (U+200C)
        c = c.replace('\u200c', '')
        # Remove zero-width space (U+200B)
        c = c.replace('\u200b', '')
        # Remove non-breaking space (U+00A0) → regular space
        c = c.replace('\u00a0', ' ')
        # Strip again after removals
        c = c.strip()
        cols.append(c)
    return cols


# ═══════════════════════════════════════════════════════════════════════
# DATA CLEANING ENGINE — Comprehensive CSV pre-processing
# ═══════════════════════════════════════════════════════════════════════

import csv as _csv_mod, unicodedata as _unicodedata, statistics as _statistics, math as _math_clean, re

# ─── Constants ───

# 50+ null-like representations across languages & systems
NULL_VALUES = {
    '', 'null', 'none', 'nil', 'na', 'n/a', '#n/a', '#na', '#null',
    'nan', '#nan', 'missing', 'undefined', 'unknown',
    '-', '--', '---', '.', '..', '...', '?', '??',
    'n.a.', 'n.a', 'not available', 'not applicable', 'no data',
    '#value!', '#ref!', '#div/0!', '#name?', '#num!', '#getting data',
    'inf', '-inf', 'infinity', '-infinity', '+inf', '+infinity',
    '(blank)', 'blank', 'empty', 'void',
    'n/d', 'nd', 'no info', 'no information', 'tbd', 'tba',
}

# Currency symbols from around the world
CURRENCY_SYMBOLS = '$€£¥₹₽₩₪₫₴₦฿₡₢₣₤₥₧₨₭₮₯₰₱₲₳₵₶₷₸₺₻₼₾¢'

# Boolean-like value mapping (lowercase key → bool)
BOOL_TRUE = {'true', 'yes', 'y', '1', 't', 'on', 'enabled', 'active',
             'ใช่', 'จริง', 'si', 'oui', 'ja', 'da', 'はい', '是',
             'correct', 'confirmed', 'approved', 'pass', 'passed', 'ok'}
BOOL_FALSE = {'false', 'no', 'n', '0', 'f', 'off', 'disabled', 'inactive',
              'ไม่ใช่', 'ไม่', 'เท็จ', 'no', 'non', 'nein', 'нет', 'いいえ', '否',
              'incorrect', 'denied', 'rejected', 'fail', 'failed', 'ng'}

# Common date formats to try (ordered by likelihood)
DATE_FORMATS = [
    '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%SZ',
    '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S%z',
    '%Y/%m/%d', '%Y.%m.%d',
    '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',       # EU/Thai
    '%m/%d/%Y', '%m-%d-%Y', '%m.%d.%Y',       # US
    '%d/%m/%y', '%m/%d/%y',                     # Short year
    '%d %b %Y', '%d %B %Y',                     # 01 Jan 2024
    '%b %d, %Y', '%B %d, %Y',                   # Jan 01, 2024
    '%Y%m%d',                                     # YYYYMMDD compact
    '%d-%b-%Y', '%d-%b-%y',                      # 01-Jan-2024
    '%Y-%m-%d %H:%M:%S', '%Y/%m/%d %H:%M:%S',
    '%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S',
    '%d/%m/%Y %H:%M', '%m/%d/%Y %H:%M',
    '%Y-%m-%d %H:%M', '%H:%M:%S', '%H:%M',
]

# Unicode fraction characters -> decimal
FRACTION_MAP = {
    '\u00bd': '0.5', '\u2153': '0.3333', '\u2154': '0.6667', '\u00bc': '0.25', '\u00be': '0.75',
    '\u2155': '0.2', '\u2156': '0.4', '\u2157': '0.6', '\u2158': '0.8', '\u2159': '0.1667',
    '\u215a': '0.8333', '\u215b': '0.125', '\u215c': '0.375', '\u215d': '0.625', '\u215e': '0.875',
    '\u2150': '0.1429', '\u2151': '0.1111', '\u2152': '0.1',
}

# Full-width -> half-width character mapping (CJK)
FULLWIDTH_TABLE = str.maketrans(
    '\uff21\uff22\uff23\uff24\uff25\uff26\uff27\uff28\uff29\uff2a\uff2b\uff2c\uff2d\uff2e\uff2f\uff30\uff31\uff32\uff33\uff34\uff35\uff36\uff37\uff38\uff39\uff3a'
    '\uff41\uff42\uff43\uff44\uff45\uff46\uff47\uff48\uff49\uff4a\uff4b\uff4c\uff4d\uff4e\uff4f\uff50\uff51\uff52\uff53\uff54\uff55\uff56\uff57\uff58\uff59\uff5a'
    '\uff10\uff11\uff12\uff13\uff14\uff15\uff16\uff17\uff18\uff19'
    '\uff01\uff03\uff04\uff05\uff06\uff08\uff09\uff0a\uff0b\uff0c\uff0d\uff0e\uff0f\uff1a\uff1b\uff1c\uff1d\uff1e\uff1f\uff20\uff3b\uff3d\uff3e\uff3f\uff40\uff5b\uff5c\uff5d\uff5e\u3000',
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    'abcdefghijklmnopqrstuvwxyz'
    '0123456789'
    '!#$%&()*+,-./:;<=>?@[]^_`{|}~ '
)

# PII detection patterns (compiled regex, mask replacement)
_PII_CC = re.compile(r'\b(?:\d[ -]?){13,19}\b')
_PII_SSN = re.compile(r'\b\d{3}[- ]?\d{2}[- ]?\d{4}\b')
_PII_IBAN = re.compile(r'\b[A-Z]{2}\d{2}[ ]?[\dA-Z]{4}[ ]?(?:[\dA-Z]{4}[ ]?){1,7}[\dA-Z]{1,4}\b')
_PII_THAI_ID = re.compile(r'\b\d[- ]?\d{4}[- ]?\d{5}[- ]?\d{2}[- ]?\d\b')
_PII_PASSPORT = re.compile(r'\b[A-Z]{1,2}\d{6,9}\b')
PII_PATTERNS = [
    (_PII_CC, '****-****-****-****'),
    (_PII_SSN, '***-**-****'),
    (_PII_IBAN, '****IBAN****'),
    (_PII_THAI_ID, '*-****-*****-**-*'),
    (_PII_PASSPORT, '**********'),
]

# Common Mojibake patterns (garbled UTF-8 in Latin-1) -> corrected
MOJIBAKE_MAP = {
    '\u00c3\u00a1': '\u00e1', '\u00c3\u00a9': '\u00e9', '\u00c3\u00ad': '\u00ed',
    '\u00c3\u00b3': '\u00f3', '\u00c3\u00ba': '\u00fa', '\u00c3\u00b1': '\u00f1',
    '\u00c3\u00bc': '\u00fc', '\u00c3\u00b6': '\u00f6', '\u00c3\u00a4': '\u00e4',
    '\u00c3\u00ab': '\u00eb', '\u00c3\u00a8': '\u00e8', '\u00c3\u00a2': '\u00e2',
    '\u00c3\u00aa': '\u00ea', '\u00c3\u00ae': '\u00ee', '\u00c3\u00b4': '\u00f4',
    '\u00c3\u00bb': '\u00fb', '\u00c3\u00a7': '\u00e7',
    '\u00c2\u00a9': '\u00a9', '\u00c2\u00ae': '\u00ae', '\u00c2\u00b0': '\u00b0',
    '\u00c2\u00b2': '\u00b2', '\u00c2\u00b3': '\u00b3',
    '\u00c2\u00bd': '\u00bd', '\u00c2\u00bc': '\u00bc', '\u00c2\u00be': '\u00be',
    '\u00c2\u00a3': '\u00a3',
}

# US State and common location abbreviations
LOCATION_ABBREV = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware',
    'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho',
    'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland',
    'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi',
    'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York',
    'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah',
    'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming', 'DC': 'District of Columbia',
    'US': 'United States', 'USA': 'United States', 'UK': 'United Kingdom',
    'GB': 'United Kingdom', 'AU': 'Australia', 'NZ': 'New Zealand',
    'JP': 'Japan', 'CN': 'China', 'KR': 'South Korea', 'TH': 'Thailand',
    'SG': 'Singapore', 'MY': 'Malaysia', 'BR': 'Brazil', 'MX': 'Mexico',
    'FR': 'France', 'RU': 'Russia',
}

# ─── Phase 3 Constants: Messy Data Handling ───

# Honorifics and titles to strip
HONORIFICS = [
    'Mr.', 'Mrs.', 'Ms.', 'Miss', 'Dr.', 'Prof.', 'Rev.', 'Sr.', 'Jr.',
    'Mx.', 'Sir', 'Dame', 'Lord', 'Lady', 'Capt.', 'Col.', 'Gen.', 'Sgt.',
    'Mr', 'Mrs', 'Ms', 'Dr', 'Prof', 'Rev',
    # Thai
    'นาย', 'นาง', 'นางสาว', 'ดร.', 'ศ.', 'รศ.', 'ผศ.',
]

# Common abbreviation expansions
ABBREVIATION_MAP = {
    'st.': 'Street', 'st': 'Street', 'ave.': 'Avenue', 'ave': 'Avenue',
    'blvd.': 'Boulevard', 'blvd': 'Boulevard', 'dr.': 'Drive', 'dr': 'Drive',
    'ln.': 'Lane', 'ln': 'Lane', 'rd.': 'Road', 'rd': 'Road',
    'ct.': 'Court', 'ct': 'Court', 'pl.': 'Place', 'pl': 'Place',
    'pkwy.': 'Parkway', 'pkwy': 'Parkway', 'cir.': 'Circle', 'cir': 'Circle',
    'hwy.': 'Highway', 'hwy': 'Highway', 'apt.': 'Apartment', 'apt': 'Apartment',
    'ste.': 'Suite', 'ste': 'Suite', 'bldg.': 'Building', 'bldg': 'Building',
    'dept.': 'Department', 'dept': 'Department', 'approx.': 'Approximately',
    'govt.': 'Government', 'govt': 'Government', 'intl.': 'International',
    'intl': 'International', 'mgr.': 'Manager', 'mgr': 'Manager',
    'corp.': 'Corporation', 'corp': 'Corporation', 'inc.': 'Incorporated',
    'ltd.': 'Limited', 'ltd': 'Limited', 'co.': 'Company',
    'assn.': 'Association', 'assoc.': 'Association',
    'est.': 'Established', 'misc.': 'Miscellaneous',
    'qty.': 'Quantity', 'qty': 'Quantity', 'amt.': 'Amount', 'amt': 'Amount',
    'pcs.': 'Pieces', 'pcs': 'Pieces', 'pkg.': 'Package', 'pkg': 'Package',
    'acct.': 'Account', 'acct': 'Account',
    'tel.': 'Telephone', 'tel': 'Telephone', 'fax.': 'Facsimile',
    'no.': 'Number', 'nos.': 'Numbers',
    'vs.': 'Versus', 'vs': 'Versus', 'etc.': 'Et Cetera',
    'min.': 'Minutes', 'mins.': 'Minutes', 'hr.': 'Hour', 'hrs.': 'Hours',
    'sec.': 'Seconds', 'secs.': 'Seconds',
    'jan.': 'January', 'feb.': 'February', 'mar.': 'March', 'apr.': 'April',
    'jun.': 'June', 'jul.': 'July', 'aug.': 'August', 'sep.': 'September',
    'sept.': 'September', 'oct.': 'October', 'nov.': 'November', 'dec.': 'December',
    'mon.': 'Monday', 'tue.': 'Tuesday', 'tues.': 'Tuesday',
    'wed.': 'Wednesday', 'thu.': 'Thursday', 'thur.': 'Thursday', 'thurs.': 'Thursday',
    'fri.': 'Friday', 'sat.': 'Saturday', 'sun.': 'Sunday',
}

# Gender standardization map
GENDER_MAP = {
    # English
    'male': 'M', 'm': 'M', 'man': 'M', 'boy': 'M', 'gentleman': 'M',
    'female': 'F', 'f': 'F', 'woman': 'F', 'girl': 'F', 'lady': 'F',
    # Thai
    'ชาย': 'M', 'หญิง': 'F', 'เพศชาย': 'M', 'เพศหญิง': 'F',
    # Others
    'non-binary': 'NB', 'nonbinary': 'NB', 'nb': 'NB',
    'other': 'O', 'prefer not to say': 'U', 'unknown': 'U',
    'na': 'U', 'n/a': 'U', '-': 'U',
}

# Unit conversion factors: {(from, to): multiplier}
UNIT_CONVERSIONS = {
    # Weight
    ('kg', 'lbs'): 2.20462, ('lbs', 'kg'): 0.453592,
    ('kg', 'g'): 1000.0, ('g', 'kg'): 0.001,
    ('oz', 'g'): 28.3495, ('g', 'oz'): 0.035274,
    ('lbs', 'oz'): 16.0, ('oz', 'lbs'): 0.0625,
    ('ton', 'kg'): 907.185, ('kg', 'ton'): 0.00110231,
    # Length
    ('km', 'mi'): 0.621371, ('mi', 'km'): 1.60934,
    ('m', 'ft'): 3.28084, ('ft', 'm'): 0.3048,
    ('cm', 'in'): 0.393701, ('in', 'cm'): 2.54,
    ('mm', 'in'): 0.0393701, ('in', 'mm'): 25.4,
    ('m', 'cm'): 100.0, ('cm', 'm'): 0.01,
    ('km', 'm'): 1000.0, ('m', 'km'): 0.001,
    ('yd', 'm'): 0.9144, ('m', 'yd'): 1.09361,
    # Temperature (handled specially — not just multiply)
    # Volume
    ('l', 'gal'): 0.264172, ('gal', 'l'): 3.78541,
    ('ml', 'oz_fl'): 0.033814, ('oz_fl', 'ml'): 29.5735,
    ('l', 'ml'): 1000.0, ('ml', 'l'): 0.001,
    # Area
    ('sqm', 'sqft'): 10.7639, ('sqft', 'sqm'): 0.092903,
    ('ha', 'acre'): 2.47105, ('acre', 'ha'): 0.404686,
    # Speed
    ('kmh', 'mph'): 0.621371, ('mph', 'kmh'): 1.60934,
}

# Common British→American spelling variants
SPELLING_VARIANTS = {
    'colour': 'color', 'colours': 'colors', 'coloured': 'colored',
    'favour': 'favor', 'favours': 'favors', 'favourite': 'favorite',
    'honour': 'honor', 'honours': 'honors', 'honoured': 'honored',
    'labour': 'labor', 'labours': 'labors', 'laboured': 'labored',
    'neighbour': 'neighbor', 'neighbours': 'neighbors',
    'behaviour': 'behavior', 'behaviours': 'behaviors',
    'humour': 'humor', 'humours': 'humors',
    'organisation': 'organization', 'organisations': 'organizations',
    'realise': 'realize', 'realised': 'realized',
    'recognise': 'recognize', 'recognised': 'recognized',
    'analyse': 'analyze', 'analysed': 'analyzed',
    'summarise': 'summarize', 'summarised': 'summarized',
    'optimise': 'optimize', 'optimised': 'optimized',
    'normalise': 'normalize', 'normalised': 'normalized',
    'minimise': 'minimize', 'minimised': 'minimized',
    'maximise': 'maximize', 'maximised': 'maximized',
    'utilise': 'utilize', 'utilised': 'utilized',
    'specialise': 'specialize', 'specialised': 'specialized',
    'customise': 'customize', 'customised': 'customized',
    'apologise': 'apologize', 'apologised': 'apologized',
    'catalogue': 'catalog', 'catalogues': 'catalogs',
    'dialogue': 'dialog', 'dialogues': 'dialogs',
    'programme': 'program', 'programmes': 'programs',
    'centre': 'center', 'centres': 'centers',
    'metre': 'meter', 'metres': 'meters',
    'litre': 'liter', 'litres': 'liters',
    'theatre': 'theater', 'theatres': 'theaters',
    'defence': 'defense', 'offence': 'offense',
    'licence': 'license', 'licences': 'licenses',
    'practise': 'practice',
    'grey': 'gray', 'greys': 'grays',
    'tyre': 'tire', 'tyres': 'tires',
    'cheque': 'check', 'cheques': 'checks',
    'jewellery': 'jewelry',
    'traveller': 'traveler', 'travellers': 'travelers',
    'cancelled': 'canceled', 'cancelling': 'canceling',
    'modelling': 'modeling', 'modelled': 'modeled',
    'labelling': 'labeling', 'labelled': 'labeled',
    'travelling': 'traveling', 'travelled': 'traveled',
    'enrolment': 'enrollment', 'enrolments': 'enrollments',
    'fulfilment': 'fulfillment',
    'judgement': 'judgment',
    'ageing': 'aging',
    'aluminium': 'aluminum',
    'paediatric': 'pediatric', 'paediatrics': 'pediatrics',
    'anaesthetic': 'anesthetic', 'anaesthesia': 'anesthesia',
    'orthopaedic': 'orthopedic',
    'encyclopaedia': 'encyclopedia',
    'manoeuvre': 'maneuver', 'manoeuvres': 'maneuvers',
    'aeroplane': 'airplane', 'aeroplanes': 'airplanes',
}

# Duration pattern components
DURATION_PATTERNS = [
    # "2h30m", "2h 30m", "2hrs 30mins"
    (re.compile(r'(\d+)\s*(?:h|hr|hrs|hours?)\s*(?:(\d+)\s*(?:m|min|mins|minutes?))?\s*(?:(\d+)\s*(?:s|sec|secs|seconds?))?', re.IGNORECASE), 'hms'),
    # "90 minutes", "90 mins", "90m"
    (re.compile(r'^(\d+(?:\.\d+)?)\s*(?:m|min|mins|minutes?)$', re.IGNORECASE), 'min'),
    # "2 hours", "2 hrs"
    (re.compile(r'^(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hours?)$', re.IGNORECASE), 'hr'),
    # "90 seconds", "90 secs", "90s"
    (re.compile(r'^(\d+(?:\.\d+)?)\s*(?:s|sec|secs|seconds?)$', re.IGNORECASE), 'sec'),
    # "1 day 3 hours", "2d 5h"
    (re.compile(r'(\d+)\s*(?:d|days?)\s*(?:(\d+)\s*(?:h|hr|hrs|hours?))?', re.IGNORECASE), 'dh'),
    # "1:30:00" or "1:30" (h:m:s or h:m)
    (re.compile(r'^(\d+):(\d{2})(?::(\d{2}))?$'), 'colon'),
]

# Default cleaning configuration
DEFAULT_CLEANING_CONFIG = {
    # ─── Row-level ───
    'remove_duplicates': True,              # Remove exact duplicate rows
    'remove_empty_rows': True,              # Remove rows where all cells are empty/null
    'max_null_pct': 0.8,                    # Remove rows with >80% null cells (0.0-1.0, None=off)
    'remove_columns_pct': None,             # Remove columns with >N% nulls (None=off, e.g. 0.9)

    # ─── Cell-level text ───
    'trim_whitespace': True,                # Strip leading/trailing whitespace
    'remove_extra_spaces': True,            # Collapse multiple spaces → single space
    'remove_control_chars': True,           # Remove \t, \r, \n, etc. within cells
    'normalize_unicode': True,              # NFC normalization (composed form)
    'remove_bom': True,                     # Remove BOM, ZWNJ, ZWS, NBSP characters
    'remove_html_tags': False,              # Strip <tag> content (off by default)
    'remove_urls': False,                   # Remove http(s):// URLs (off by default)
    'remove_emails': False,                 # Remove email addresses (off by default)
    'remove_non_printable': True,           # Remove non-printable chars (keep Unicode letters)
    'remove_non_ascii': False,              # Remove non-ASCII chars (off — keeps Thai, CJK, etc.)

    # ─── Null handling ───
    'standardize_nulls': True,              # Convert NA, N/A, null, -, etc. → empty string
    'null_fill_strategy': None,             # None, 'forward', 'backward', 'mean', 'median', 'mode', or a literal value
    'null_fill_columns': None,              # List of columns to apply fill (None=all)

    # ─── Numeric cleaning ───
    'fix_currency': True,                   # Remove $€£¥฿ etc. from number cells
    'fix_thousands': True,                  # Remove thousand separators (1,000 → 1000)
    'fix_percentages': True,                # 50% → 50 (remove % symbol)
    'fix_negative_parens': True,            # (100) → -100 (accounting format)
    'fix_scientific': True,                 # 1.5E+03 → 1500

    # ─── Boolean ───
    'standardize_booleans': False,          # Convert Yes/No/Y/N/1/0 → TRUE/FALSE (off by default)

    # ─── Case ───
    'case_mode': None,                      # None, 'upper', 'lower', 'title', 'proper'
    'case_columns': None,                   # List of columns to apply case (None=all text)

    # ─── Outliers ───
    'remove_outliers': False,               # Detect & remove outliers (off by default)
    'outlier_method': 'iqr',                # 'iqr' or 'zscore'
    'outlier_threshold': 1.5,               # IQR multiplier (1.5) or Z-score threshold (3.0)
    'outlier_action': 'remove',             # 'remove', 'cap', 'null' (replace with null)
    'outlier_columns': None,                # List of numeric columns (None=all numeric)

    # ─── Date parsing ───
    'fix_dates': False,                     # Parse date strings → ISO format (off by default)
    'date_columns': None,                   # List of column names/indices (None=auto-detect)
    'date_output_format': '%Y-%m-%d',       # Output date format
    'fix_buddhist_era': False,              # Convert Buddhist year (2567) → Gregorian (2024)

    # ─── Validation (flag only, no removal) ───
    'validate_emails': False,               # Flag invalid email formats
    'validate_phones': False,               # Flag invalid phone numbers
    'validate_ranges': None,                # Dict: {'column': (min, max)} — flag out-of-range

    # ─── Encoding ───
    'fix_encoding': True,                   # Try to fix mojibake / encoding issues
    'input_encoding': 'utf-8-sig',          # Input file encoding
    'output_encoding': 'utf-8',             # Output file encoding

    # ─── Phase 2: Text Enhancement ───
    'remove_diacritics': False,             # cafe -> cafe, naive -> naive
    'remove_emoji': False,                  # Strip all emoji characters
    'regex_replacements': None,             # List of {'pattern': r'...', 'replacement': '...'}
    'pad_columns': None,                    # Dict: {'zip': (5, '0', 'left')} = (width, char, side)
    'normalize_whitespace_types': True,     # Full-width spaces, tabs -> regular space

    # ─── Phase 2: Numeric Utilities ───
    'round_decimals': None,                 # Round numeric cols to N decimal places (None=off)
    'clamp_ranges': None,                   # Dict: {'col': (min, max)} = clamp values
    'fix_fractions': False,                 # Unicode fractions 1/2 3/4 -> 0.5, 0.75

    # ─── Phase 2: Privacy & Security ───
    'mask_pii': False,                      # Mask credit cards, SSNs, IBANs, Thai IDs
    'mask_emails_privacy': False,           # john@ex.com -> j***@ex.com

    # ─── Phase 2: Fuzzy Dedup ───
    'fuzzy_dedup': False,                   # Fuzzy duplicate detection (Levenshtein)
    'fuzzy_dedup_columns': None,            # Columns to compare (None=all text)
    'fuzzy_dedup_threshold': 0.85,          # Similarity threshold (0.0-1.0)

    # ─── Phase 2: Encoding ───
    'fix_mojibake': False,                  # Fix common UTF-8 in Latin1 garbled text
    'fix_fullwidth': False,                 # Full-width -> half-width (CJK)

    # ─── Phase 2: Domain-Specific ───
    'normalize_phones': False,              # Normalize phone numbers
    'phone_country_code': '+1',             # Default country code for phone normalization
    'normalize_urls': False,                # Lowercase, strip tracking params
    'fix_coordinates': False,               # DMS -> decimal GPS coordinates
    'format_postal_codes': None,            # Country code: 'US', 'UK', etc.
    'standardize_locations': False,         # Expand abbreviations: CA -> California
    'location_mode': 'expand',              # 'expand' or 'abbreviate'

    # ─── Phase 2: Cross-validation ───
    'cross_validate': None,                 # List of {'rule': 'col_a > col_b', 'columns': ['a','b']}

    # ═══ Phase 3: Structural Fixes ═══
    'fix_column_count': False,              # Pad/trim rows to match header count
    'split_multi_value': None,              # Dict: {'col': ';'} = split cell by delimiter into rows
    'split_columns': None,                  # Dict: {'Full Name': (' ', ['First', 'Last'])}
    'fix_embedded_newlines': True,          # Replace \n \r in cells with space
    'fix_quoted_strings': True,             # Remove redundant surrounding quotes
    'fix_escape_sequences': False,          # Convert literal \\n \\t to space
    'auto_generate_headers': False,         # Generate Column_1.. if headers empty/duplicate

    # ═══ Phase 3: Text Normalization ═══
    'extract_numbers': None,                # List of column names to extract numbers from
    'compress_repeated_chars': False,       # "helloooo" → "hello"
    'strip_honorifics': False,              # Remove Mr./Mrs./Dr./นาย/นาง
    'expand_abbreviations': False,          # St. → Street, Ave. → Avenue
    'fix_mixed_case': False,                # "jOhN" → "John" (smart title case)
    'strip_edge_punctuation': False,        # ",hello." → "hello"
    'normalize_whitespace_types': True,     # Tabs, NBSP → regular space (already in P2, kept)

    # ═══ Phase 3: Data Consistency ═══
    'standardize_gender': False,            # M/F/Male/Female/ชาย/หญิง → M/F
    'convert_units': None,                  # Dict: {'Weight': ('kg', 'lbs')}
    'normalize_spelling': False,            # colour→color, organisation→organization
    'consolidate_categories': None,         # Dict: {'col': {'NYC': 'New York', 'N.Y.': 'New York'}}
    'normalize_scale': None,                # Dict: {'col': (0, 100, 0.0, 1.0)} = (old_min,old_max,new_min,new_max)
    'parse_durations': None,                # List of column names → convert to minutes

    # ═══ Phase 3: Smart Dedup & Cleanup ═══
    'smart_dedup': False,                   # Dedup keeping most complete row
    'smart_dedup_columns': None,            # Key columns for smart dedup
    'remove_constant_columns': False,       # Remove columns where all values are identical
    'sample_rows': None,                    # Int: randomly sample N rows (None=off)

    # ═══ Phase 3: JSON/Structured Data ═══
    'extract_json_fields': None,            # Dict: {'col': ['field1','field2']}
    'extract_key_value': None,              # Dict: {'col': ('=', ',')} = (kv_sep, pair_sep)
}


# ─── Cell-Level Cleaning Helpers ───

def _clean_text(value, config):
    """Clean a single text cell value based on config."""
    if not isinstance(value, str):
        return value

    # BOM and zero-width characters
    if config.get('remove_bom', True):
        for ch in ['\ufeff', '\u200c', '\u200b', '\u200d', '\u200e', '\u200f',
                   '\u2060', '\u2061', '\u2062', '\u2063', '\ufffe']:
            value = value.replace(ch, '')
        value = value.replace('\u00a0', ' ')  # NBSP → space

    # Control characters (keep \n for now, remove others)
    if config.get('remove_control_chars', True):
        value = ''.join(ch for ch in value
                       if ch == '\n' or ch >= ' ' or ch == '\t')
        value = value.replace('\t', ' ').replace('\r', '').replace('\n', ' ')

    # Non-printable characters
    if config.get('remove_non_printable', True):
        value = ''.join(ch for ch in value
                       if ch.isprintable() or _unicodedata.category(ch).startswith('L'))

    # Remove non-ASCII (careful: off by default to keep Thai/CJK)
    if config.get('remove_non_ascii', False):
        value = value.encode('ascii', 'ignore').decode('ascii')

    # Unicode normalization (NFC — composed form)
    if config.get('normalize_unicode', True):
        value = _unicodedata.normalize('NFC', value)

    # HTML tags
    if config.get('remove_html_tags', False):
        value = re.sub(r'<[^>]+>', '', value)

    # URLs
    if config.get('remove_urls', False):
        value = re.sub(r'https?://\S+', '', value)

    # Emails
    if config.get('remove_emails', False):
        value = re.sub(r'[\w.+-]+@[\w-]+\.[\w.-]+', '', value)

    # Trim whitespace
    if config.get('trim_whitespace', True):
        value = value.strip()

    # Collapse extra spaces
    if config.get('remove_extra_spaces', True):
        value = re.sub(r' {2,}', ' ', value)

    return value


def _clean_number(value, config):
    """
    Attempt to clean a numeric string.
    Returns cleaned string (still a string, not float).
    Returns original value if it doesn't look numeric after cleaning.
    """
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v

    # Accounting negative format: (100) → -100
    if config.get('fix_negative_parens', True):
        m = re.match(r'^\(([0-9,.\s]+)\)$', v)
        if m:
            v = '-' + m.group(1)

    # Remove currency symbols
    if config.get('fix_currency', True):
        for ch in CURRENCY_SYMBOLS:
            v = v.replace(ch, '')
        # Also common text currency
        for cur in ['USD', 'EUR', 'GBP', 'JPY', 'THB', 'CNY', 'KRW', 'INR',
                     'AUD', 'CAD', 'CHF', 'SGD', 'HKD', 'NZD', 'SEK', 'NOK',
                     'DKK', 'BRL', 'RUB', 'ZAR', 'MXN', 'ARS', 'CLP', 'COP',
                     'PEN', 'VND', 'IDR', 'MYR', 'PHP', 'TWD', 'BDT', 'PKR']:
            if v.upper().endswith(cur) or v.upper().startswith(cur):
                v = re.sub(re.escape(cur), '', v, flags=re.IGNORECASE).strip()

    # Remove percentage sign
    if config.get('fix_percentages', True):
        v = v.replace('%', '')

    # Remove thousand separators (commas in 1,000,000)
    if config.get('fix_thousands', True):
        # Only remove commas that are thousand separators (not decimal)
        # Pattern: digits, comma, exactly 3 digits (repeated)
        if re.match(r'^-?[\d,]+(\.\d+)?$', v):
            v = v.replace(',', '')
        # European format: dots as thousand sep, comma as decimal
        elif re.match(r'^-?[\d.]+,\d+$', v):
            v = v.replace('.', '').replace(',', '.')

    # Scientific notation (keep as-is, Python can parse it)
    # But normalize: 1.5E+03 → stays as-is

    v = v.strip()
    return v


def _parse_date(value, config):
    """
    Try to parse a date string into ISO format.
    Returns ISO string on success, original value on failure.
    """
    import datetime as _dt
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v

    # Unix timestamp (seconds since epoch)
    try:
        ts = float(v)
        if 1e9 < ts < 2e10:  # ~2001 to ~2603
            return _dt.datetime.fromtimestamp(ts).strftime(config.get('date_output_format', '%Y-%m-%d'))
        if 1e12 < ts < 2e13:  # milliseconds
            return _dt.datetime.fromtimestamp(ts / 1000).strftime(config.get('date_output_format', '%Y-%m-%d'))
    except (ValueError, OSError, OverflowError):
        pass

    # Buddhist Era (Thai calendar: year + 543)
    if config.get('fix_buddhist_era', False):
        m = re.match(r'^(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{4})$', v)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
            if 2400 < y < 2700:  # Likely Buddhist era
                y -= 543
                try:
                    return _dt.date(y, mo, d).strftime(config.get('date_output_format', '%Y-%m-%d'))
                except ValueError:
                    pass

    # Try known formats
    for fmt in DATE_FORMATS:
        try:
            parsed = _dt.datetime.strptime(v, fmt)
            return parsed.strftime(config.get('date_output_format', '%Y-%m-%d'))
        except ValueError:
            continue

    return value  # Return original if no format matched


def _is_numeric_str(value):
    """Check if a string can be parsed as a number (including after stripping currency/thousands/pct)."""
    if not isinstance(value, str):
        return False
    v = value.strip()
    if not v:
        return False
    try:
        float(v)
        return True
    except (ValueError, TypeError):
        pass
    # Try after stripping common numeric decorations
    v2 = v
    # Accounting parens: (100) → -100
    if v2.startswith('(') and v2.endswith(')'):
        v2 = v2[1:-1]
    # Currency symbols
    for ch in CURRENCY_SYMBOLS:
        v2 = v2.replace(ch, '')
    # Percentage
    v2 = v2.replace('%', '').strip()
    # Thousand separators (comma-period style)
    if re.match(r'^-?[\d,]+(\.\d+)?$', v2):
        v2 = v2.replace(',', '')
    # European thousand separators (period-comma style)
    elif re.match(r'^-?[\d.]+,\d+$', v2):
        v2 = v2.replace('.', '').replace(',', '.')
    try:
        float(v2)
        return True
    except (ValueError, TypeError):
        return False


def _detect_column_type(values):
    """
    Auto-detect column type from a list of string values.
    Returns: 'numeric', 'date', 'boolean', 'text'
    """
    import datetime as _dt
    non_empty = [v for v in values if v and str(v).strip() and str(v).strip().lower() not in NULL_VALUES]
    if not non_empty:
        return 'text'

    sample = non_empty[:100]  # Sample first 100 non-empty values

    # Check numeric
    numeric_count = sum(1 for v in sample if _is_numeric_str(str(v)))
    if numeric_count / len(sample) > 0.7:
        return 'numeric'

    # Check boolean
    bool_count = sum(1 for v in sample if str(v).strip().lower() in BOOL_TRUE | BOOL_FALSE)
    if bool_count / len(sample) > 0.7:
        return 'boolean'

    # Check date
    date_count = 0
    for v in sample[:30]:  # Smaller sample for dates (parsing is expensive)
        for fmt in DATE_FORMATS[:10]:  # Try top-10 common formats
            try:
                _dt.datetime.strptime(str(v).strip(), fmt)
                date_count += 1
                break
            except ValueError:
                continue
    if len(sample[:30]) > 0 and date_count / len(sample[:30]) > 0.6:
        return 'date'

    return 'text'


def _detect_outliers_iqr(values, threshold=1.5):
    """
    Detect outliers using IQR method.
    Returns: (lower_bound, upper_bound, outlier_indices)
    """
    nums = [(i, float(v)) for i, v in enumerate(values)
            if isinstance(v, str) and _is_numeric_str(v) or isinstance(v, (int, float))]
    if len(nums) < 4:
        return None, None, []

    sorted_vals = sorted(n[1] for n in nums)
    q1_idx = len(sorted_vals) // 4
    q3_idx = 3 * len(sorted_vals) // 4
    q1 = sorted_vals[q1_idx]
    q3 = sorted_vals[q3_idx]
    iqr = q3 - q1
    lower = q1 - threshold * iqr
    upper = q3 + threshold * iqr

    outlier_indices = [i for i, v in nums if v < lower or v > upper]
    return lower, upper, outlier_indices


def _detect_outliers_zscore(values, threshold=3.0):
    """
    Detect outliers using Z-score method.
    Returns: (mean, std, outlier_indices)
    """
    nums = [(i, float(v)) for i, v in enumerate(values)
            if isinstance(v, str) and _is_numeric_str(v) or isinstance(v, (int, float))]
    if len(nums) < 4:
        return None, None, []

    vals = [n[1] for n in nums]
    mean = _statistics.mean(vals)
    std = _statistics.stdev(vals) if len(vals) > 1 else 0
    if std == 0:
        return mean, std, []

    outlier_indices = [i for i, v in nums if abs((v - mean) / std) > threshold]
    return mean, std, outlier_indices


def _validate_email(value):
    """Basic email format validation. Returns True if valid."""
    if not isinstance(value, str):
        return False
    return bool(re.match(r'^[\w.+-]+@[\w-]+\.[\w.-]+$', value.strip()))


def _validate_phone(value):
    """Basic phone number validation (digits, +, -, spaces, parens). Returns True if valid."""
    if not isinstance(value, str):
        return False
    digits_only = re.sub(r'[\s\-\(\)\.\+]', '', value.strip())
    return 7 <= len(digits_only) <= 15 and digits_only.isdigit()


# ─── Phase 2 Cell-Level Helpers ───

def _remove_diacritics(value):
    """Remove diacritics/accents: cafe -> cafe, naive -> naive."""
    if not isinstance(value, str):
        return value
    nfkd = _unicodedata.normalize('NFKD', value)
    return ''.join(ch for ch in nfkd if not _unicodedata.combining(ch))


def _remove_emoji(value):
    """Remove all emoji characters from a string."""
    if not isinstance(value, str):
        return value
    # Comprehensive emoji pattern (simplified for reliability)
    emoji_pattern = re.compile(
        '['
        '\U0001F600-\U0001F64F'   # emoticons
        '\U0001F300-\U0001F5FF'   # symbols & pictographs
        '\U0001F680-\U0001F6FF'   # transport & map
        '\U0001F1E0-\U0001F1FF'   # flags
        '\U00002702-\U000027B0'   # dingbats
        '\U000024C2-\U0001F251'   # enclosed chars
        '\U0001F900-\U0001F9FF'   # supplemental symbols
        '\U0001FA00-\U0001FA6F'   # chess symbols
        '\U0001FA70-\U0001FAFF'   # symbols extended-A
        '\U00002600-\U000026FF'   # misc symbols
        '\U0000FE00-\U0000FE0F'   # variation selectors
        '\U0000200D'              # ZWJ
        '\U00002B50'              # star
        '\U0000203C-\U00003299'   # misc symbols & CJK
        ']+', flags=re.UNICODE)
    return emoji_pattern.sub('', value)


def _mask_pii_value(value):
    """Mask PII patterns (credit cards, SSNs, IBANs, etc.) in a string."""
    if not isinstance(value, str):
        return value
    for pattern, mask in PII_PATTERNS:
        value = pattern.sub(mask, value)
    return value


def _mask_email_privacy(value):
    """Mask email for privacy: john.doe@example.com -> j*******@example.com."""
    if not isinstance(value, str):
        return value
    m = re.match(r'^([\w.+-]+)@([\w-]+\.[\w.-]+)$', value.strip())
    if m:
        local = m.group(1)
        domain = m.group(2)
        if len(local) <= 2:
            masked = local[0] + '*'
        else:
            masked = local[0] + '*' * (len(local) - 1)
        return f'{masked}@{domain}'
    return value


def _fix_mojibake(value):
    """Fix common mojibake (garbled UTF-8 read as Latin-1)."""
    if not isinstance(value, str):
        return value
    for garbled, correct in MOJIBAKE_MAP.items():
        value = value.replace(garbled, correct)
    # Also try re-encoding as Latin-1 -> UTF-8
    try:
        fixed = value.encode('latin-1').decode('utf-8')
        if fixed != value:
            return fixed
    except (UnicodeDecodeError, UnicodeEncodeError):
        pass
    return value


def _fix_fullwidth(value):
    """Convert full-width characters to half-width (CJK compatibility)."""
    if not isinstance(value, str):
        return value
    return value.translate(FULLWIDTH_TABLE)


def _normalize_phone(value, country_code='+1'):
    """Normalize phone number to international format."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    # Extract only digits and leading +
    has_plus = v.startswith('+')
    digits = re.sub(r'[^\d]', '', v)
    if not digits or len(digits) < 7:
        return value  # Too short, return as-is

    # Already international format (10+ digits with +)
    if has_plus and len(digits) >= 10:
        return '+' + digits

    # US/Canada: 10 digits -> +1-XXX-XXX-XXXX
    if country_code == '+1' and len(digits) == 10:
        return f'+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}'
    if country_code == '+1' and len(digits) == 11 and digits[0] == '1':
        return f'+1-{digits[1:4]}-{digits[4:7]}-{digits[7:]}'

    # Thailand: 10 digits -> +66-XX-XXX-XXXX
    if country_code == '+66' and len(digits) == 10 and digits[0] == '0':
        return f'+66-{digits[1:3]}-{digits[3:6]}-{digits[6:]}'

    # Generic: prepend country code if not too long
    if not has_plus and len(digits) <= 12:
        cc_digits = re.sub(r'[^\d]', '', country_code)
        if not digits.startswith(cc_digits):
            return country_code + '-' + digits

    return '+' + digits if has_plus else value


def _normalize_url(value):
    """Normalize URL: lowercase scheme/host, strip tracking params."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    # Only process things that look like URLs
    if not re.match(r'https?://', v, re.IGNORECASE):
        return value

    # Lowercase scheme and host
    m = re.match(r'(https?://[^/\s?#]+)(.*)', v, re.IGNORECASE)
    if m:
        host = m.group(1).lower()
        rest = m.group(2)
        v = host + rest

    # Strip common tracking parameters
    tracking_params = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term',
                       'utm_content', 'fbclid', 'gclid', 'ref', 'mc_cid', 'mc_eid']
    if '?' in v:
        base, query = v.split('?', 1)
        params = query.split('&')
        clean_params = [p for p in params
                       if not any(p.startswith(tp + '=') for tp in tracking_params)]
        if clean_params:
            v = base + '?' + '&'.join(clean_params)
        else:
            v = base

    # Remove trailing slash
    if v.endswith('/') and v.count('/') > 3:
        v = v.rstrip('/')

    return v


def _fix_coordinate(value):
    """Convert DMS (degrees/minutes/seconds) GPS coordinates to decimal."""
    if not isinstance(value, str):
        return value
    v = value.strip()

    # DMS format: 40 26 46 N or 40 26'46"N or 40.446195
    m = re.match(r'''(\d+)\s*[^\d]*\s*(\d+)\s*[^\d]*\s*([\d.]+)\s*[^\d]*\s*([NSEWnsew])''', v)
    if m:
        deg = float(m.group(1))
        mins = float(m.group(2))
        secs = float(m.group(3))
        direction = m.group(4).upper()
        decimal = deg + mins / 60 + secs / 3600
        if direction in ('S', 'W'):
            decimal = -decimal
        return f'{decimal:.6f}'

    return value


def _levenshtein_ratio(s1, s2):
    """Calculate Levenshtein similarity ratio (0.0 to 1.0)."""
    if not s1 and not s2:
        return 1.0
    if not s1 or not s2:
        return 0.0
    len1, len2 = len(s1), len(s2)
    if len1 > len2:
        s1, s2 = s2, s1
        len1, len2 = len2, len1

    current_row = list(range(len1 + 1))
    for i in range(1, len2 + 1):
        prev_row = current_row
        current_row = [i] + [0] * len1
        for j in range(1, len1 + 1):
            add = prev_row[j] + 1
            delete = current_row[j - 1] + 1
            change = prev_row[j - 1] + (0 if s2[i-1] == s1[j-1] else 1)
            current_row[j] = min(add, delete, change)

    distance = current_row[len1]
    max_len = max(len1, len2)
    return 1.0 - (distance / max_len) if max_len > 0 else 1.0


def _format_postal_code(value, country='US'):
    """Format postal/zip code according to country standard."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v

    if country == 'US':
        # US ZIP: 5 or 9 digits (ZIP+4)
        digits = re.sub(r'[^\d]', '', v)
        if len(digits) == 5:
            return digits
        elif len(digits) == 9:
            return f'{digits[:5]}-{digits[5:]}'
        elif len(digits) < 5:
            return digits.zfill(5)
    elif country == 'UK':
        # UK: A9 9AA, A99 9AA, A9A 9AA, AA9 9AA, AA99 9AA, AA9A 9AA
        v = v.upper().replace(' ', '')
        if len(v) >= 5:
            return v[:-3] + ' ' + v[-3:]
    elif country == 'CA':
        # Canada: A1A 1A1
        v = v.upper().replace(' ', '')
        if len(v) == 6:
            return v[:3] + ' ' + v[3:]
    elif country == 'JP':
        # Japan: 123-4567
        digits = re.sub(r'[^\d]', '', v)
        if len(digits) == 7:
            return f'{digits[:3]}-{digits[3:]}'
    elif country == 'TH':
        # Thailand: 5 digits
        digits = re.sub(r'[^\d]', '', v)
        return digits.zfill(5) if len(digits) <= 5 else digits

    return v


def _fix_fraction(value):
    """Convert Unicode fraction characters and text fractions to decimals."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    # Unicode fractions
    for frac, decimal in FRACTION_MAP.items():
        v = v.replace(frac, decimal)
    # Text fractions: 1/2, 3/4, etc. (standalone only)
    m = re.match(r'^(\d+)/(\d+)$', v)
    if m:
        num, den = int(m.group(1)), int(m.group(2))
        if den != 0:
            return str(round(num / den, 4))
    return v


def profile_data(csv_path, skip_rows=0, delimiter=',', encoding='utf-8-sig'):
    """
    Generate a comprehensive data profile/summary for a CSV file.

    Returns a dict with per-column statistics:
    {
        'row_count': int,
        'column_count': int,
        'columns': {
            'col_name': {
                'type': str,             # detected type
                'total': int,            # total rows
                'non_null': int,         # non-empty count
                'null_count': int,       # empty count
                'null_pct': float,       # % empty
                'unique': int,           # unique values
                'top_values': list,      # top 5 most common
                'min': str/float,        # min value (numeric) or shortest string
                'max': str/float,        # max value (numeric) or longest string
                'mean': float,           # mean (numeric only)
                'median': float,         # median (numeric only)
                'std': float,            # std dev (numeric only)
                'avg_length': float,     # average string length (text only)
                'pattern_samples': list, # sample patterns (e.g., AAAA-9999)
            }
        }
    }
    """
    rows = []
    headers = []
    with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
        for _ in range(skip_rows):
            f.readline()
        reader = _csv_mod.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if i == 0:
                headers = [h.strip() for h in row]
            else:
                rows.append(row)

    ncols = len(headers)
    rows = [r + [''] * (ncols - len(r)) if len(r) < ncols else r[:ncols] for r in rows]

    profile = {
        'row_count': len(rows),
        'column_count': ncols,
        'columns': {},
    }

    for c_idx in range(ncols):
        col_vals = [rows[r][c_idx] for r in range(len(rows))]
        col_name = headers[c_idx]
        non_null = [v for v in col_vals if v.strip()]
        null_count = len(col_vals) - len(non_null)

        col_info = {
            'type': _detect_column_type(col_vals),
            'total': len(col_vals),
            'non_null': len(non_null),
            'null_count': null_count,
            'null_pct': round(null_count / len(col_vals) * 100, 1) if col_vals else 0,
            'unique': len(set(non_null)),
        }

        # Top values (most common)
        if non_null:
            from collections import Counter
            counter = Counter(non_null)
            col_info['top_values'] = counter.most_common(5)

        # Numeric stats
        numeric_vals = [float(v) for v in non_null if _is_numeric_str(v)]
        if numeric_vals and col_info['type'] == 'numeric':
            col_info['min'] = min(numeric_vals)
            col_info['max'] = max(numeric_vals)
            col_info['mean'] = round(_statistics.mean(numeric_vals), 4)
            col_info['median'] = _statistics.median(numeric_vals)
            col_info['std'] = round(_statistics.stdev(numeric_vals), 4) if len(numeric_vals) > 1 else 0
        elif non_null:
            # Text stats
            lengths = [len(v) for v in non_null]
            col_info['min'] = min(non_null, key=len)
            col_info['max'] = max(non_null, key=len)
            col_info['avg_length'] = round(sum(lengths) / len(lengths), 1)

        # Pattern samples (replace letters with A, digits with 9)
        patterns = set()
        for v in non_null[:50]:
            p = re.sub(r'[A-Za-z]', 'A', v)
            p = re.sub(r'\d', '9', p)
            patterns.add(p)
        col_info['pattern_samples'] = list(patterns)[:5]

        profile['columns'][col_name] = col_info

    return profile


# ─── Phase 3 Helpers: Messy Data Handling ───

def _extract_number(value):
    """Extract the first number from a mixed text string. e.g. 'Age: 25 years' → '25'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    # Try to find a decimal/integer number
    m = re.search(r'-?\d+(?:\.\d+)?', v)
    if m:
        return m.group(0)
    return v


def _compress_repeated_chars(value, max_repeat=2):
    """Compress repeated characters. 'helloooo' → 'helloo', 'yesssss' → 'yess'."""
    if not isinstance(value, str):
        return value
    if len(value) < 3:
        return value
    # Compress runs of 3+ same char to max_repeat
    result = []
    i = 0
    while i < len(value):
        char = value[i]
        count = 1
        while i + count < len(value) and value[i + count] == char:
            count += 1
        result.append(char * min(count, max_repeat))
        i += count
    return ''.join(result)


def _strip_honorific(value):
    """Remove honorific prefixes from names. 'Mr. John Smith' → 'John Smith'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    for h in HONORIFICS:
        if v.startswith(h + ' '):
            v = v[len(h):].strip()
            break
        elif v.startswith(h + '.'):
            v = v[len(h) + 1:].strip() if not h.endswith('.') else v[len(h):].strip()
            break
    return v


def _expand_abbreviation(value):
    """Expand common abbreviations. 'St.' → 'Street', 'Ave.' → 'Avenue'."""
    if not isinstance(value, str):
        return value
    words = value.split()
    result = []
    for w in words:
        key = w.lower().rstrip('.,;:')
        if key in ABBREVIATION_MAP:
            result.append(ABBREVIATION_MAP[key])
        else:
            result.append(w)
    return ' '.join(result)


def _fix_mixed_case(value):
    """Fix mixed case text. 'jOhN sMiTh' → 'John Smith'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    # Check if it's actually mixed case (not all upper, not all lower, not already title)
    words = v.split()
    needs_fix = False
    for w in words:
        if len(w) > 1 and not w.isupper() and not w.islower() and not w.istitle():
            needs_fix = True
            break
    if needs_fix:
        return v.title()
    return v


def _strip_edge_punctuation(value):
    """Remove leading/trailing punctuation. ',hello.' → 'hello', '...test...' → 'test'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v
    # Strip common leading/trailing punctuation (keep quotes, parens for now)
    v = v.strip('.,;:!?*#~-_…·•')
    return v.strip()


def _standardize_gender_value(value):
    """Standardize gender values. 'Male'/'female'/'ชาย'/'F' → 'M'/'F'."""
    if not isinstance(value, str):
        return value
    v = value.strip().lower()
    if v in GENDER_MAP:
        return GENDER_MAP[v]
    return value


def _convert_unit_value(value, from_unit, to_unit):
    """Convert a numeric value from one unit to another."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v

    # Extract numeric part
    m = re.match(r'^(-?\d+(?:\.\d+)?)\s*(?:' + re.escape(from_unit) + r')?\s*$', v, re.IGNORECASE)
    if not m:
        # Try just a number
        m = re.match(r'^(-?\d+(?:\.\d+)?)$', v)
    if m:
        num = float(m.group(1))
        key = (from_unit.lower(), to_unit.lower())
        # Temperature special handling
        if key == ('c', 'f') or key == ('celsius', 'fahrenheit'):
            return str(round(num * 9 / 5 + 32, 2))
        elif key == ('f', 'c') or key == ('fahrenheit', 'celsius'):
            return str(round((num - 32) * 5 / 9, 2))
        elif key in UNIT_CONVERSIONS:
            return str(round(num * UNIT_CONVERSIONS[key], 4))
    return value


def _normalize_spelling_word(value):
    """Normalize British to American spelling. 'colour' → 'color'."""
    if not isinstance(value, str):
        return value
    words = value.split()
    changed = False
    result = []
    for w in words:
        # Preserve case
        lower = w.lower()
        if lower in SPELLING_VARIANTS:
            replacement = SPELLING_VARIANTS[lower]
            # Match original case
            if w.isupper():
                result.append(replacement.upper())
            elif w[0].isupper():
                result.append(replacement.capitalize())
            else:
                result.append(replacement)
            changed = True
        else:
            result.append(w)
    return ' '.join(result) if changed else value


def _parse_duration_value(value):
    """Parse duration string to minutes. '2h30m' → '150', '1:30' → '90'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if not v:
        return v

    for pattern, fmt in DURATION_PATTERNS:
        m = pattern.match(v)
        if m:
            if fmt == 'hms':
                hours = int(m.group(1))
                mins = int(m.group(2)) if m.group(2) else 0
                secs = int(m.group(3)) if m.group(3) else 0
                return str(round(hours * 60 + mins + secs / 60, 2))
            elif fmt == 'min':
                return str(round(float(m.group(1)), 2))
            elif fmt == 'hr':
                return str(round(float(m.group(1)) * 60, 2))
            elif fmt == 'sec':
                return str(round(float(m.group(1)) / 60, 2))
            elif fmt == 'dh':
                days = int(m.group(1))
                hours = int(m.group(2)) if m.group(2) else 0
                return str(days * 24 * 60 + hours * 60)
            elif fmt == 'colon':
                hours = int(m.group(1))
                mins = int(m.group(2))
                secs = int(m.group(3)) if m.group(3) else 0
                return str(round(hours * 60 + mins + secs / 60, 2))
    return v


def _extract_json_value(value, fields):
    """Extract fields from JSON string. Returns dict of field→value."""
    import json as _json_mod
    if not isinstance(value, str):
        return {}
    v = value.strip()
    if not v.startswith('{'):
        return {}
    try:
        data = _json_mod.loads(v)
        return {f: str(data.get(f, '')) for f in fields}
    except (ValueError, TypeError):
        return {}


def _extract_kv_value(value, kv_sep='=', pair_sep=','):
    """Extract key-value pairs. 'name=John, age=30' → {'name': 'John', 'age': '30'}."""
    if not isinstance(value, str):
        return {}
    v = value.strip()
    if not v:
        return {}
    result = {}
    pairs = v.split(pair_sep)
    for pair in pairs:
        if kv_sep in pair:
            key, val = pair.split(kv_sep, 1)
            result[key.strip()] = val.strip()
    return result


def _fix_quoted_string(value):
    """Remove redundant wrapping quotes. '\"hello\"' → 'hello', \"'world'\" → 'world'."""
    if not isinstance(value, str):
        return value
    v = value.strip()
    if len(v) >= 2:
        if (v[0] == '"' and v[-1] == '"') or (v[0] == "'" and v[-1] == "'"):
            inner = v[1:-1].strip()
            # Only strip if inner doesn't contain the quote char
            if v[0] not in inner:
                return inner
    # Handle triple quotes
    if len(v) >= 6:
        if v[:3] == '"""' and v[-3:] == '"""':
            return v[3:-3].strip()
        if v[:3] == "'''" and v[-3:] == "'''":
            return v[3:-3].strip()
    return v


def _fix_escape_sequence(value):
    """Convert literal escape sequences to their characters. '\\n' → ' ', '\\t' → ' '."""
    if not isinstance(value, str):
        return value
    v = value
    v = v.replace('\\n', ' ').replace('\\t', ' ').replace('\\r', ' ')
    v = v.replace('\\\\', '\\')
    return v


def _smart_dedup_merge(row_a, row_b):
    """Merge two similar rows, keeping the most complete data from each."""
    merged = []
    for a, b in zip(row_a, row_b):
        va, vb = a.strip(), b.strip()
        if va and vb:
            merged.append(va if len(va) >= len(vb) else vb)  # Keep longer/more complete
        elif va:
            merged.append(va)
        elif vb:
            merged.append(vb)
        else:
            merged.append('')
    return merged


# ─── Main Data Cleaning Function ───

def clean_csv(csv_path, output_path=None, config=None, skip_rows=0, delimiter=','):
    """
    Comprehensive CSV data cleaning — covers every known technique.

    Performs cleaning in optimal order:
      1. Read & parse CSV
      2. Remove junk/header rows (skip_rows)
      3. Clean header names (BOM, whitespace, zero-width chars)
      4. Standardize null values
      5. Clean text cells (trim, control chars, unicode, HTML, URLs)
      6. Clean numeric cells (currency, thousands, percentages, parens)
      7. Parse dates (20+ formats, Buddhist era, Unix timestamps)
      8. Standardize booleans
      9. Case standardization
     10. Remove empty rows
     11. Remove duplicate rows
     12. Handle outliers (IQR / Z-score)
     13. Fill missing values (forward/backward/mean/median/mode/literal)
     14. Remove high-null columns
     15. Validate (emails, phones, ranges)

    Args:
        csv_path: Absolute path to input CSV file
        output_path: Path for cleaned CSV (None = overwrite input)
        config: Dict of cleaning options (see DEFAULT_CLEANING_CONFIG)
        skip_rows: Number of junk rows to skip before header
        delimiter: CSV field separator character

    Returns:
        tuple: (output_path, cleaning_report)
        cleaning_report = {
            'input_rows': int, 'output_rows': int,
            'input_cols': int, 'output_cols': int,
            'nulls_standardized': int, 'duplicates_removed': int,
            'empty_rows_removed': int, 'outliers_handled': int,
            'text_cells_cleaned': int, 'numbers_cleaned': int,
            'dates_parsed': int, 'booleans_standardized': int,
            'columns_removed': list, 'validation_warnings': list,
            'column_types': dict,
        }
    """
    cfg = {**DEFAULT_CLEANING_CONFIG}
    if config:
        cfg.update(config)

    report = {
        'input_rows': 0, 'output_rows': 0,
        'input_cols': 0, 'output_cols': 0,
        'nulls_standardized': 0, 'duplicates_removed': 0,
        'empty_rows_removed': 0, 'outliers_handled': 0,
        'text_cells_cleaned': 0, 'numbers_cleaned': 0,
        'dates_parsed': 0, 'booleans_standardized': 0,
        'columns_removed': [], 'validation_warnings': [],
        'column_types': {},
        # Phase 2 counters
        'diacritics_removed': 0, 'emoji_removed': 0,
        'pii_masked': 0, 'emails_masked': 0,
        'mojibake_fixed': 0, 'fullwidth_fixed': 0,
        'phones_normalized': 0, 'urls_normalized': 0,
        'coordinates_fixed': 0, 'postal_codes_formatted': 0,
        'locations_standardized': 0, 'fractions_fixed': 0,
        'values_rounded': 0, 'values_clamped': 0,
        'fuzzy_dupes_removed': 0, 'regex_replacements_applied': 0,
        'values_padded': 0, 'cross_validation_warnings': [],
        # Phase 3 counters
        'columns_fixed_count': 0, 'rows_split': 0, 'columns_split': 0,
        'newlines_fixed': 0, 'quotes_fixed': 0, 'escapes_fixed': 0,
        'headers_generated': 0, 'numbers_extracted': 0,
        'chars_compressed': 0, 'honorifics_stripped': 0,
        'abbreviations_expanded': 0, 'mixed_case_fixed': 0,
        'edge_punct_stripped': 0, 'genders_standardized': 0,
        'units_converted': 0, 'spellings_normalized': 0,
        'categories_consolidated': 0, 'scales_normalized': 0,
        'durations_parsed': 0, 'smart_dupes_merged': 0,
        'constant_columns_removed': [], 'json_fields_extracted': 0,
        'kv_pairs_extracted': 0, 'rows_sampled': False,
    }

    # ── Step 1: Read CSV ──
    rows = []
    headers = []
    encoding = cfg.get('input_encoding', 'utf-8-sig')
    with open(csv_path, 'r', encoding=encoding, errors='replace') as f:
        for _ in range(skip_rows):
            f.readline()
        reader = _csv_mod.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if i == 0:
                headers = row
            else:
                rows.append(row)

    report['input_rows'] = len(rows)
    report['input_cols'] = len(headers)

    # ── Step 2: Clean headers ──
    clean_headers = []
    for h in headers:
        h = h.strip()
        for ch in ['\ufeff', '\u200c', '\u200b', '\u200d', '\u200e', '\u200f', '\u2060']:
            h = h.replace(ch, '')
        h = h.replace('\u00a0', ' ').strip()
        if cfg.get('normalize_unicode', True):
            h = _unicodedata.normalize('NFC', h)
        clean_headers.append(h)
    headers = clean_headers
    ncols = len(headers)

    # Pad rows to header length
    rows = [r + [''] * (ncols - len(r)) if len(r) < ncols else r[:ncols] for r in rows]

    # ── Step 3: Standardize nulls ──
    if cfg.get('standardize_nulls', True):
        for r_idx, row in enumerate(rows):
            for c_idx in range(ncols):
                val = row[c_idx].strip() if isinstance(row[c_idx], str) else str(row[c_idx])
                if val.lower() in NULL_VALUES:
                    rows[r_idx][c_idx] = ''
                    report['nulls_standardized'] += 1

    # ── Step 4: Clean text cells ──
    for r_idx, row in enumerate(rows):
        for c_idx in range(ncols):
            original = row[c_idx]
            cleaned = _clean_text(row[c_idx], cfg)
            if cleaned != original:
                report['text_cells_cleaned'] += 1
            rows[r_idx][c_idx] = cleaned

    # ── Step 5: Auto-detect column types ──
    col_types = {}
    for c_idx in range(ncols):
        col_values = [rows[r][c_idx] for r in range(len(rows))]
        col_types[headers[c_idx]] = _detect_column_type(col_values)
    report['column_types'] = col_types

    # ── Step 6: Clean numeric cells ──
    if any(cfg.get(k) for k in ['fix_currency', 'fix_thousands', 'fix_percentages',
                                  'fix_negative_parens', 'fix_scientific']):
        for c_idx in range(ncols):
            if col_types.get(headers[c_idx]) == 'numeric':
                for r_idx in range(len(rows)):
                    original = rows[r_idx][c_idx]
                    cleaned = _clean_number(original, cfg)
                    if cleaned != original:
                        report['numbers_cleaned'] += 1
                    rows[r_idx][c_idx] = cleaned

    # ── Step 7: Parse dates ──
    if cfg.get('fix_dates', False):
        date_cols = cfg.get('date_columns')
        if date_cols is None:
            # Auto-detect date columns
            date_cols = [c_idx for c_idx in range(ncols)
                        if col_types.get(headers[c_idx]) == 'date']
        elif isinstance(date_cols, list):
            date_cols = [headers.index(c) if isinstance(c, str) else c for c in date_cols]

        for c_idx in date_cols:
            for r_idx in range(len(rows)):
                original = rows[r_idx][c_idx]
                if original.strip():
                    parsed = _parse_date(original, cfg)
                    if parsed != original:
                        report['dates_parsed'] += 1
                    rows[r_idx][c_idx] = parsed

    # ── Step 8: Standardize booleans ──
    if cfg.get('standardize_booleans', False):
        for c_idx in range(ncols):
            if col_types.get(headers[c_idx]) == 'boolean':
                for r_idx in range(len(rows)):
                    val = rows[r_idx][c_idx].strip().lower()
                    if val in BOOL_TRUE:
                        rows[r_idx][c_idx] = 'TRUE'
                        report['booleans_standardized'] += 1
                    elif val in BOOL_FALSE:
                        rows[r_idx][c_idx] = 'FALSE'
                        report['booleans_standardized'] += 1

    # ── Step 9: Case standardization ──
    case_mode = cfg.get('case_mode')
    if case_mode:
        case_cols = cfg.get('case_columns')
        target_indices = list(range(ncols))
        if case_cols:
            target_indices = [headers.index(c) if isinstance(c, str) else c for c in case_cols]
        for c_idx in target_indices:
            if col_types.get(headers[c_idx]) in ('text', None):
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v:
                        if case_mode == 'upper':
                            rows[r_idx][c_idx] = v.upper()
                        elif case_mode == 'lower':
                            rows[r_idx][c_idx] = v.lower()
                        elif case_mode in ('title', 'proper'):
                            rows[r_idx][c_idx] = v.title()

    # ── Step 10: Remove empty rows ──
    if cfg.get('remove_empty_rows', True):
        before = len(rows)
        rows = [r for r in rows if any(cell.strip() for cell in r)]
        report['empty_rows_removed'] = before - len(rows)

    # ── Step 10b: Remove high-null rows ──
    max_null_pct = cfg.get('max_null_pct')
    if max_null_pct is not None and 0 < max_null_pct < 1:
        before = len(rows)
        threshold = int(ncols * max_null_pct)
        rows = [r for r in rows if sum(1 for c in r if not c.strip()) <= threshold]
        report['empty_rows_removed'] += (before - len(rows))

    # ── Step 11: Remove duplicates ──
    if cfg.get('remove_duplicates', True):
        before = len(rows)
        seen = set()
        unique_rows = []
        for row in rows:
            key = tuple(row)
            if key not in seen:
                seen.add(key)
                unique_rows.append(row)
        rows = unique_rows
        report['duplicates_removed'] = before - len(rows)

    # ── Step 12: Handle outliers ──
    if cfg.get('remove_outliers', False):
        outlier_cols = cfg.get('outlier_columns')
        if outlier_cols is None:
            outlier_cols = [c_idx for c_idx in range(ncols)
                          if col_types.get(headers[c_idx]) == 'numeric']
        elif isinstance(outlier_cols, list):
            outlier_cols = [headers.index(c) if isinstance(c, str) else c for c in outlier_cols]

        method = cfg.get('outlier_method', 'iqr')
        threshold = cfg.get('outlier_threshold', 1.5 if method == 'iqr' else 3.0)
        action = cfg.get('outlier_action', 'remove')

        outlier_row_indices = set()
        for c_idx in outlier_cols:
            col_vals = [rows[r][c_idx] for r in range(len(rows))]
            if method == 'iqr':
                lower, upper, indices = _detect_outliers_iqr(col_vals, threshold)
            else:
                _, _, indices = _detect_outliers_zscore(col_vals, threshold)
                lower, upper = None, None

            if action == 'remove':
                outlier_row_indices.update(indices)
            elif action == 'null':
                for idx in indices:
                    rows[idx][c_idx] = ''
            elif action == 'cap' and method == 'iqr' and lower is not None:
                for idx in indices:
                    try:
                        v = float(rows[idx][c_idx])
                        rows[idx][c_idx] = str(max(lower, min(upper, v)))
                    except (ValueError, TypeError):
                        pass
            report['outliers_handled'] += len(indices)

        if action == 'remove' and outlier_row_indices:
            rows = [r for i, r in enumerate(rows) if i not in outlier_row_indices]

    # ── Step 13: Fill missing values ──
    strategy = cfg.get('null_fill_strategy')
    if strategy:
        fill_cols = cfg.get('null_fill_columns')
        if fill_cols:
            fill_indices = [headers.index(c) if isinstance(c, str) else c for c in fill_cols]
        else:
            fill_indices = list(range(ncols))

        for c_idx in fill_indices:
            if strategy == 'forward':
                last_val = ''
                for r_idx in range(len(rows)):
                    if rows[r_idx][c_idx].strip():
                        last_val = rows[r_idx][c_idx]
                    else:
                        rows[r_idx][c_idx] = last_val
            elif strategy == 'backward':
                last_val = ''
                for r_idx in range(len(rows) - 1, -1, -1):
                    if rows[r_idx][c_idx].strip():
                        last_val = rows[r_idx][c_idx]
                    else:
                        rows[r_idx][c_idx] = last_val
            elif strategy in ('mean', 'median', 'mode'):
                col_vals = [rows[r][c_idx] for r in range(len(rows))]
                numeric_vals = [float(v) for v in col_vals if _is_numeric_str(v)]
                if numeric_vals:
                    if strategy == 'mean':
                        fill_val = str(round(_statistics.mean(numeric_vals), 4))
                    elif strategy == 'median':
                        fill_val = str(_statistics.median(numeric_vals))
                    else:  # mode
                        try:
                            fill_val = str(_statistics.mode(numeric_vals))
                        except _statistics.StatisticsError:
                            fill_val = str(_statistics.mean(numeric_vals))
                    for r_idx in range(len(rows)):
                        if not rows[r_idx][c_idx].strip():
                            rows[r_idx][c_idx] = fill_val
                else:
                    # Text mode: fill with most common value
                    non_empty = [v for v in col_vals if v.strip()]
                    if non_empty:
                        try:
                            fill_val = _statistics.mode(non_empty)
                        except _statistics.StatisticsError:
                            fill_val = non_empty[0]
                        for r_idx in range(len(rows)):
                            if not rows[r_idx][c_idx].strip():
                                rows[r_idx][c_idx] = fill_val
            else:
                # Literal value
                for r_idx in range(len(rows)):
                    if not rows[r_idx][c_idx].strip():
                        rows[r_idx][c_idx] = str(strategy)

    # ── Step 14: Remove high-null columns ──
    remove_col_pct = cfg.get('remove_columns_pct')
    if remove_col_pct is not None and 0 < remove_col_pct <= 1:
        keep_indices = []
        for c_idx in range(ncols):
            null_count = sum(1 for r in rows if not r[c_idx].strip())
            if len(rows) > 0 and null_count / len(rows) > remove_col_pct:
                report['columns_removed'].append(headers[c_idx])
            else:
                keep_indices.append(c_idx)
        if len(keep_indices) < ncols:
            headers = [headers[i] for i in keep_indices]
            rows = [[r[i] for i in keep_indices] for r in rows]
            ncols = len(headers)

    # ── Step 15: Validation (flag only) ──
    if cfg.get('validate_emails', False):
        for c_idx in range(ncols):
            if 'email' in headers[c_idx].lower():
                invalid = sum(1 for r in rows
                            if r[c_idx].strip() and not _validate_email(r[c_idx]))
                if invalid:
                    report['validation_warnings'].append(
                        f'Column "{headers[c_idx]}": {invalid} invalid email(s)')

    if cfg.get('validate_phones', False):
        for c_idx in range(ncols):
            if any(kw in headers[c_idx].lower() for kw in ['phone', 'mobile', 'tel', 'fax']):
                invalid = sum(1 for r in rows
                            if r[c_idx].strip() and not _validate_phone(r[c_idx]))
                if invalid:
                    report['validation_warnings'].append(
                        f'Column "{headers[c_idx]}": {invalid} invalid phone number(s)')

    validate_ranges = cfg.get('validate_ranges')
    if validate_ranges:
        for col_name, (rmin, rmax) in validate_ranges.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                out_of_range = 0
                for r in rows:
                    if r[c_idx].strip() and _is_numeric_str(r[c_idx]):
                        v = float(r[c_idx])
                        if v < rmin or v > rmax:
                            out_of_range += 1
                if out_of_range:
                    report['validation_warnings'].append(
                        f'Column "{col_name}": {out_of_range} value(s) outside [{rmin}, {rmax}]')

    # ═══════════════════════════════════════════════════════════════
    # PHASE 2 CLEANING STEPS (Steps 16-27)
    # ═══════════════════════════════════════════════════════════════

    # ── Step 16: Fix mojibake / full-width characters ──
    if cfg.get('fix_mojibake', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    fixed = _fix_mojibake(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['mojibake_fixed'] += 1

    if cfg.get('fix_fullwidth', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    fixed = _fix_fullwidth(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['fullwidth_fixed'] += 1

    # ── Step 17: Diacritics removal ──
    if cfg.get('remove_diacritics', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    cleaned = _remove_diacritics(v)
                    if cleaned != v:
                        rows[r_idx][c_idx] = cleaned
                        report['diacritics_removed'] += 1

    # ── Step 18: Emoji removal ──
    if cfg.get('remove_emoji', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    cleaned = _remove_emoji(v)
                    if cleaned != v:
                        rows[r_idx][c_idx] = cleaned
                        report['emoji_removed'] += 1

    # ── Step 19: Fix fractions ──
    if cfg.get('fix_fractions', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    fixed = _fix_fraction(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['fractions_fixed'] += 1

    # ── Step 20: Regex replacements ──
    regex_rules = cfg.get('regex_replacements')
    if regex_rules:
        for rule in regex_rules:
            pat = re.compile(rule['pattern'])
            repl = rule['replacement']
            for r_idx in range(len(rows)):
                for c_idx in range(ncols):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        new_v = pat.sub(repl, v)
                        if new_v != v:
                            rows[r_idx][c_idx] = new_v
                            report['regex_replacements_applied'] += 1

    # ── Step 21: PII masking ──
    if cfg.get('mask_pii', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip():
                    masked = _mask_pii_value(v)
                    if masked != v:
                        rows[r_idx][c_idx] = masked
                        report['pii_masked'] += 1

    if cfg.get('mask_emails_privacy', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if 'email' in headers[c_idx].lower():
                    v = rows[r_idx][c_idx]
                    if v.strip() and '@' in v:
                        masked = _mask_email_privacy(v)
                        if masked != v:
                            rows[r_idx][c_idx] = masked
                            report['emails_masked'] += 1

    # ── Step 22: Phone normalization ──
    if cfg.get('normalize_phones', False):
        cc = cfg.get('phone_country_code', '+1')
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if any(kw in headers[c_idx].lower() for kw in ['phone', 'mobile', 'tel', 'fax', 'cell']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        normalized = _normalize_phone(v, cc)
                        if normalized != v:
                            rows[r_idx][c_idx] = normalized
                            report['phones_normalized'] += 1

    # ── Step 23: URL normalization ──
    if cfg.get('normalize_urls', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if any(kw in headers[c_idx].lower() for kw in ['url', 'link', 'website', 'href']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        normalized = _normalize_url(v)
                        if normalized != v:
                            rows[r_idx][c_idx] = normalized
                            report['urls_normalized'] += 1

    # ── Step 24: GPS coordinate fix ──
    if cfg.get('fix_coordinates', False):
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if any(kw in headers[c_idx].lower() for kw in ['lat', 'lon', 'coord', 'gps', 'latitude', 'longitude']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        fixed = _fix_coordinate(v)
                        if fixed != v:
                            rows[r_idx][c_idx] = fixed
                            report['coordinates_fixed'] += 1

    # ── Step 25: Postal code formatting ──
    postal_country = cfg.get('format_postal_codes')
    if postal_country:
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if any(kw in headers[c_idx].lower() for kw in ['zip', 'postal', 'postcode', 'zip_code']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        formatted = _format_postal_code(v, postal_country)
                        if formatted != v:
                            rows[r_idx][c_idx] = formatted
                            report['postal_codes_formatted'] += 1

    # ── Step 25b: Location standardization ──
    if cfg.get('standardize_locations', False):
        loc_mode = cfg.get('location_mode', 'expand')
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                if any(kw in headers[c_idx].lower() for kw in ['state', 'country', 'region', 'province', 'location']):
                    v = rows[r_idx][c_idx].strip()
                    if v:
                        if loc_mode == 'expand' and v.upper() in LOCATION_ABBREV:
                            rows[r_idx][c_idx] = LOCATION_ABBREV[v.upper()]
                            report['locations_standardized'] += 1
                        elif loc_mode == 'abbreviate':
                            # Reverse lookup
                            rev = {full.lower(): abbr for abbr, full in LOCATION_ABBREV.items()}
                            if v.lower() in rev:
                                rows[r_idx][c_idx] = rev[v.lower()]
                                report['locations_standardized'] += 1

    # ── Step 26: Fuzzy deduplication ──
    if cfg.get('fuzzy_dedup', False) and len(rows) > 1:
        threshold = cfg.get('fuzzy_dedup_threshold', 0.85)
        fuzzy_cols = cfg.get('fuzzy_dedup_columns')
        if fuzzy_cols:
            fuzzy_indices = [headers.index(c) if isinstance(c, str) else c for c in fuzzy_cols]
        else:
            fuzzy_indices = [i for i in range(ncols)
                           if col_types.get(headers[i]) in ('text', None)]

        # Build comparison strings per row
        row_keys = []
        for row in rows:
            key = ' '.join(row[i].strip().lower() for i in fuzzy_indices if i < len(row))
            row_keys.append(key)

        # Find fuzzy duplicates (compare each to previous)
        remove_indices = set()
        for i in range(1, len(rows)):
            if i in remove_indices:
                continue
            for j in range(i):
                if j in remove_indices:
                    continue
                if _levenshtein_ratio(row_keys[i], row_keys[j]) >= threshold:
                    remove_indices.add(i)  # Keep older, remove newer duplicate
                    break

        if remove_indices:
            rows = [r for idx, r in enumerate(rows) if idx not in remove_indices]
            report['fuzzy_dupes_removed'] = len(remove_indices)

    # ── Step 26b: Rounding ──
    round_n = cfg.get('round_decimals')
    if round_n is not None:
        for r_idx in range(len(rows)):
            for c_idx in range(ncols):
                v = rows[r_idx][c_idx]
                if v.strip() and _is_numeric_str(v):
                    try:
                        rounded = str(round(float(v), round_n))
                        if rounded != v:
                            rows[r_idx][c_idx] = rounded
                            report['values_rounded'] += 1
                    except (ValueError, TypeError):
                        pass

    # ── Step 26c: Clamping ──
    clamp_cfg = cfg.get('clamp_ranges')
    if clamp_cfg:
        for col_name, (cmin, cmax) in clamp_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v.strip() and _is_numeric_str(v):
                        try:
                            fv = float(v)
                            clamped = max(cmin, min(cmax, fv))
                            if clamped != fv:
                                rows[r_idx][c_idx] = str(clamped)
                                report['values_clamped'] += 1
                        except (ValueError, TypeError):
                            pass

    # ── Step 26d: String padding ──
    pad_cfg = cfg.get('pad_columns')
    if pad_cfg:
        for col_name, pad_spec in pad_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                width = pad_spec[0] if len(pad_spec) > 0 else 5
                char = pad_spec[1] if len(pad_spec) > 1 else '0'
                side = pad_spec[2] if len(pad_spec) > 2 else 'left'
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx].strip()
                    if v and len(v) < width:
                        if side == 'left':
                            rows[r_idx][c_idx] = v.rjust(width, char)
                        else:
                            rows[r_idx][c_idx] = v.ljust(width, char)
                        report['values_padded'] += 1

    # ── Step 27: Cross-column validation ──
    cross_rules = cfg.get('cross_validate')
    if cross_rules:
        for rule_def in cross_rules:
            rule_str = rule_def.get('rule', '')
            rule_cols = rule_def.get('columns', [])
            violations = 0
            for r_idx in range(len(rows)):
                try:
                    # Build evaluation context with column values
                    ctx = {}
                    for col_name in rule_cols:
                        if col_name in headers:
                            c_idx = headers.index(col_name)
                            v = rows[r_idx][c_idx].strip()
                            try:
                                ctx[col_name.replace(' ', '_')] = float(v) if _is_numeric_str(v) else v
                            except (ValueError, TypeError):
                                ctx[col_name.replace(' ', '_')] = v

                    # Simple evaluator (only comparisons, no exec)
                    expr = rule_str
                    for col_name in rule_cols:
                        safe_name = col_name.replace(' ', '_')
                        expr = expr.replace(col_name, repr(ctx.get(safe_name, '')))

                    # Only allow safe operations
                    if not eval(expr, {"__builtins__": {}}, {}):
                        violations += 1
                except Exception:
                    pass

            if violations:
                report['cross_validation_warnings'].append(
                    f'Rule "{rule_str}": {violations} violation(s)')

    # ═══════════════════════════════════════════════════════════════
    # PHASE 3 CLEANING STEPS (Steps 28-39)
    # ═══════════════════════════════════════════════════════════════

    # ── Step 28: Structural fixes ──
    if cfg.get('fix_column_count', False):
        for r_idx in range(len(rows)):
            row = rows[r_idx]
            if len(row) < ncols:
                rows[r_idx] = row + [''] * (ncols - len(row))
                report['columns_fixed_count'] += 1
            elif len(row) > ncols:
                rows[r_idx] = row[:ncols]
                report['columns_fixed_count'] += 1

    if cfg.get('fix_embedded_newlines', True):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if '\n' in v or '\r' in v:
                    rows[r_idx][c_idx] = v.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ')
                    report['newlines_fixed'] += 1

    if cfg.get('fix_quoted_strings', True):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v and len(v) >= 2 and (v[0] in '"\'' and v[-1] in '"\''):
                    fixed = _fix_quoted_string(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['quotes_fixed'] += 1

    if cfg.get('fix_escape_sequences', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v and ('\\n' in v or '\\t' in v or '\\r' in v):
                    fixed = _fix_escape_sequence(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['escapes_fixed'] += 1

    if cfg.get('auto_generate_headers', False):
        seen = set()
        new_headers = []
        for i, h in enumerate(headers):
            if not h or h in seen:
                new_h = f'Column_{i + 1}'
                new_headers.append(new_h)
                report['headers_generated'] += 1
            else:
                new_headers.append(h)
            seen.add(new_headers[-1])
        headers = new_headers

    # ── Step 29: Multi-value cell splitting ──
    split_cfg = cfg.get('split_multi_value')
    if split_cfg and rows:
        for col_name, delimiter_char in split_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                new_rows = []
                for row in rows:
                    v = row[c_idx].strip()
                    if v and delimiter_char in v:
                        parts = [p.strip() for p in v.split(delimiter_char) if p.strip()]
                        if len(parts) > 1:
                            for part in parts:
                                new_row = list(row)
                                new_row[c_idx] = part
                                new_rows.append(new_row)
                            report['rows_split'] += len(parts) - 1
                            continue
                    new_rows.append(row)
                rows = new_rows

    # ── Step 30: Column splitting ──
    split_col_cfg = cfg.get('split_columns')
    if split_col_cfg:
        for col_name, (sep, new_names) in split_col_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                num_new = len(new_names)
                # Add new column headers
                for nn in new_names:
                    if nn not in headers:
                        headers.append(nn)
                        for row in rows:
                            row.append('')
                new_indices = [headers.index(nn) for nn in new_names]
                ncols = len(headers)
                for row in rows:
                    v = row[c_idx].strip()
                    if v:
                        parts = v.split(sep, num_new - 1)
                        for j, ni in enumerate(new_indices):
                            if j < len(parts):
                                row[ni] = parts[j].strip()
                report['columns_split'] += 1

    # ── Step 31: Text normalization ──
    extract_num_cols = cfg.get('extract_numbers')
    if extract_num_cols:
        for col_name in extract_num_cols:
            if col_name in headers:
                c_idx = headers.index(col_name)
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v.strip() and not _is_numeric_str(v):
                        extracted = _extract_number(v)
                        if extracted != v:
                            rows[r_idx][c_idx] = extracted
                            report['numbers_extracted'] += 1

    if cfg.get('compress_repeated_chars', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v.strip() and len(v) > 2:
                    compressed = _compress_repeated_chars(v)
                    if compressed != v:
                        rows[r_idx][c_idx] = compressed
                        report['chars_compressed'] += 1

    if cfg.get('strip_honorifics', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                if any(kw in headers[c_idx].lower() for kw in ['name', 'person', 'contact', 'customer']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        stripped = _strip_honorific(v)
                        if stripped != v:
                            rows[r_idx][c_idx] = stripped
                            report['honorifics_stripped'] += 1

    if cfg.get('expand_abbreviations', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                if any(kw in headers[c_idx].lower() for kw in ['address', 'street', 'location', 'addr']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        expanded = _expand_abbreviation(v)
                        if expanded != v:
                            rows[r_idx][c_idx] = expanded
                            report['abbreviations_expanded'] += 1

    if cfg.get('fix_mixed_case', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v.strip() and col_types.get(headers[c_idx] if c_idx < len(headers) else '') in ('text', None):
                    fixed = _fix_mixed_case(v)
                    if fixed != v:
                        rows[r_idx][c_idx] = fixed
                        report['mixed_case_fixed'] += 1

    if cfg.get('strip_edge_punctuation', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v.strip():
                    stripped = _strip_edge_punctuation(v)
                    if stripped != v:
                        rows[r_idx][c_idx] = stripped
                        report['edge_punct_stripped'] += 1

    # ── Step 32: Data consistency ──
    if cfg.get('standardize_gender', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                if any(kw in headers[c_idx].lower() for kw in ['gender', 'sex', 'เพศ']):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        std = _standardize_gender_value(v)
                        if std != v:
                            rows[r_idx][c_idx] = std
                            report['genders_standardized'] += 1

    unit_cfg = cfg.get('convert_units')
    if unit_cfg:
        for col_name, (from_u, to_u) in unit_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        converted = _convert_unit_value(v, from_u, to_u)
                        if converted != v:
                            rows[r_idx][c_idx] = converted
                            report['units_converted'] += 1

    if cfg.get('normalize_spelling', False):
        for r_idx in range(len(rows)):
            for c_idx in range(min(len(rows[r_idx]), ncols)):
                v = rows[r_idx][c_idx]
                if v.strip() and col_types.get(headers[c_idx] if c_idx < len(headers) else '') in ('text', None):
                    normalized = _normalize_spelling_word(v)
                    if normalized != v:
                        rows[r_idx][c_idx] = normalized
                        report['spellings_normalized'] += 1

    cat_cfg = cfg.get('consolidate_categories')
    if cat_cfg:
        for col_name, mapping in cat_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                # Build case-insensitive lookup
                ci_map = {k.lower(): v for k, v in mapping.items()}
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx].strip()
                    if v and v.lower() in ci_map:
                        rows[r_idx][c_idx] = ci_map[v.lower()]
                        report['categories_consolidated'] += 1

    scale_cfg = cfg.get('normalize_scale')
    if scale_cfg:
        for col_name, (old_min, old_max, new_min, new_max) in scale_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                old_range = old_max - old_min
                new_range = new_max - new_min
                if old_range != 0:
                    for r_idx in range(len(rows)):
                        v = rows[r_idx][c_idx]
                        if v.strip() and _is_numeric_str(v):
                            try:
                                fv = float(v)
                                scaled = new_min + (fv - old_min) / old_range * new_range
                                rows[r_idx][c_idx] = str(round(scaled, 4))
                                report['scales_normalized'] += 1
                            except (ValueError, TypeError):
                                pass

    dur_cols = cfg.get('parse_durations')
    if dur_cols:
        for col_name in dur_cols:
            if col_name in headers:
                c_idx = headers.index(col_name)
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v.strip():
                        parsed = _parse_duration_value(v)
                        if parsed != v:
                            rows[r_idx][c_idx] = parsed
                            report['durations_parsed'] += 1

    # ── Step 33: Smart dedup (keep most complete) ──
    if cfg.get('smart_dedup', False) and len(rows) > 1:
        sd_cols = cfg.get('smart_dedup_columns')
        if sd_cols:
            key_indices = [headers.index(c) for c in sd_cols if c in headers]
        else:
            key_indices = list(range(ncols))

        # Group by key
        groups = {}
        for i, row in enumerate(rows):
            key = tuple(row[ki].strip().lower() for ki in key_indices if ki < len(row))
            if key not in groups:
                groups[key] = []
            groups[key].append(i)

        # Merge groups with multiple rows
        new_rows = []
        used = set()
        for key, indices in groups.items():
            if len(indices) == 1:
                new_rows.append(rows[indices[0]])
            else:
                # Merge all rows in group
                merged = rows[indices[0]]
                for idx in indices[1:]:
                    merged = _smart_dedup_merge(merged, rows[idx])
                    report['smart_dupes_merged'] += 1
                new_rows.append(merged)
            used.update(indices)
        rows = new_rows

    # ── Step 34: Remove constant columns ──
    if cfg.get('remove_constant_columns', False) and rows:
        cols_to_remove = []
        for c_idx in range(ncols):
            vals = set(rows[r_idx][c_idx].strip() for r_idx in range(len(rows)) if c_idx < len(rows[r_idx]))
            vals.discard('')
            if len(vals) <= 1:  # All same value or all empty
                cols_to_remove.append(c_idx)

        if cols_to_remove:
            removed_names = [headers[i] for i in cols_to_remove]
            headers = [h for i, h in enumerate(headers) if i not in cols_to_remove]
            rows = [[v for i, v in enumerate(row) if i not in cols_to_remove] for row in rows]
            ncols = len(headers)
            report['constant_columns_removed'] = removed_names

    # ── Step 35: Row sampling ──
    sample_n = cfg.get('sample_rows')
    if sample_n and isinstance(sample_n, int) and sample_n < len(rows):
        import random as _rnd
        rows = _rnd.sample(rows, sample_n)
        report['rows_sampled'] = True

    # ── Step 36: JSON field extraction ──
    json_cfg = cfg.get('extract_json_fields')
    if json_cfg:
        for col_name, fields in json_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                # Add new columns for fields
                for f_name in fields:
                    new_col = f'{col_name}_{f_name}'
                    if new_col not in headers:
                        headers.append(new_col)
                        for row in rows:
                            row.append('')
                ncols = len(headers)
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx]
                    if v.strip().startswith('{'):
                        extracted = _extract_json_value(v, fields)
                        for f_name in fields:
                            new_col = f'{col_name}_{f_name}'
                            ni = headers.index(new_col)
                            rows[r_idx][ni] = extracted.get(f_name, '')
                        report['json_fields_extracted'] += 1

    # ── Step 37: Key-value extraction ──
    kv_cfg = cfg.get('extract_key_value')
    if kv_cfg:
        for col_name, (kv_sep, pair_sep) in kv_cfg.items():
            if col_name in headers:
                c_idx = headers.index(col_name)
                # First pass: collect all possible keys
                all_keys = set()
                for row in rows:
                    v = row[c_idx].strip()
                    if v and kv_sep in v:
                        extracted = _extract_kv_value(v, kv_sep, pair_sep)
                        all_keys.update(extracted.keys())
                # Add columns for keys
                for key in sorted(all_keys):
                    new_col = f'{col_name}_{key}'
                    if new_col not in headers:
                        headers.append(new_col)
                        for row in rows:
                            row.append('')
                ncols = len(headers)
                # Second pass: extract values
                for r_idx in range(len(rows)):
                    v = rows[r_idx][c_idx].strip()
                    if v and kv_sep in v:
                        extracted = _extract_kv_value(v, kv_sep, pair_sep)
                        for key, val in extracted.items():
                            new_col = f'{col_name}_{key}'
                            if new_col in headers:
                                ni = headers.index(new_col)
                                rows[r_idx][ni] = val
                        report['kv_pairs_extracted'] += 1

    # ── Write output ──
    report['output_rows'] = len(rows)
    report['output_cols'] = len(headers)

    out_path = output_path or csv_path
    out_encoding = cfg.get('output_encoding', 'utf-8')
    with open(out_path, 'w', encoding=out_encoding, newline='') as f:
        writer = _csv_mod.writer(f, delimiter=delimiter)
        writer.writerow(headers)
        writer.writerows(rows)

    return out_path, report


def print_cleaning_report(report):
    """Pretty-print a cleaning report from clean_csv()."""
    print('=' * 60)
    print('  Data Cleaning Report')
    print('=' * 60)
    print(f'  Rows:    {report["input_rows"]} → {report["output_rows"]}')
    print(f'  Columns: {report["input_cols"]} → {report["output_cols"]}')
    print()

    stats = [
        ('Nulls standardized', report.get('nulls_standardized', 0)),
        ('Text cells cleaned', report.get('text_cells_cleaned', 0)),
        ('Numbers cleaned', report.get('numbers_cleaned', 0)),
        ('Dates parsed', report.get('dates_parsed', 0)),
        ('Booleans standardized', report.get('booleans_standardized', 0)),
        ('Empty rows removed', report.get('empty_rows_removed', 0)),
        ('Duplicates removed', report.get('duplicates_removed', 0)),
        ('Outliers handled', report.get('outliers_handled', 0)),
    ]
    for label, count in stats:
        if count > 0:
            print(f'  ✅ {label}: {count}')

    if report.get('columns_removed'):
        print(f'  🗑️ Columns removed: {", ".join(report["columns_removed"])}')

    if report.get('validation_warnings'):
        print()
        for w in report['validation_warnings']:
            print(f'  ⚠️ {w}')

    if report.get('column_types'):
        print()
        print('  Column types detected:')
        for col, ctype in report['column_types'].items():
            print(f'    {col}: {ctype}')

    print('=' * 60)


# ─── M Expression Cleaning Steps Generator ───

def build_m_cleaning_steps(columns, config=None):
    """
    Generate Power Query M expression steps for in-PBI data cleaning.
    Designed to be used with build_m_expression() or standalone.

    Args:
        columns: List of {'name': str, 'type': str} column definitions
        config: Dict with cleaning options (subset of DEFAULT_CLEANING_CONFIG):
            - remove_duplicates: bool
            - remove_empty_rows: bool
            - trim_text: bool
            - clean_text: bool (Text.Clean — remove non-printable)
            - case_mode: 'upper'/'lower'/'title'/None
            - replace_nulls: dict {col_name: default_value}
            - error_handling: bool (Table.ReplaceErrorValues)

    Returns:
        list: M expression step strings ready to inject into a let...in block.
              Each step has the format:
              '  StepName = M_Expression(PreviousStep, ...)'
              Returns (steps, last_step_name)
    """
    cfg = {
        'remove_duplicates': True,
        'remove_empty_rows': True,
        'trim_text': True,
        'clean_text': True,
        'case_mode': None,
        'replace_nulls': None,  # dict: {col_name: default_value}
        'error_handling': True,
    }
    if config:
        cfg.update(config)

    steps = []
    last_step = 'CleanedHeaders'  # Assumes this comes after header cleaning

    # 1. Remove duplicates
    if cfg.get('remove_duplicates'):
        steps.append(f'  Deduped = Table.Distinct({last_step})')
        last_step = 'Deduped'

    # 2. Remove blank rows
    if cfg.get('remove_empty_rows'):
        steps.append(f'  NoBlankRows = Table.SelectRows({last_step}, each not List.IsEmpty('
                     f'List.RemoveMatchingItems(Record.FieldValues(_), {{"", null}})))')
        last_step = 'NoBlankRows'

    # 3. Trim & Clean text columns
    text_cols = [c for c in columns if c.get('type', 'string') in ('string', 'text')]
    if text_cols and (cfg.get('trim_text') or cfg.get('clean_text')):
        transforms = []
        for col in text_cols:
            name = col['name']
            if cfg.get('trim_text') and cfg.get('clean_text'):
                transforms.append(f'{{"{name}", each Text.Trim(Text.Clean(_)), type text}}')
            elif cfg.get('trim_text'):
                transforms.append(f'{{"{name}", Text.Trim, type text}}')
            elif cfg.get('clean_text'):
                transforms.append(f'{{"{name}", Text.Clean, type text}}')
        if transforms:
            transforms_str = ', '.join(transforms)
            steps.append(f'  CleanedText = Table.TransformColumns({last_step}, {{{transforms_str}}})')
            last_step = 'CleanedText'

    # 4. Case standardization
    case_mode = cfg.get('case_mode')
    if case_mode and text_cols:
        func_map = {'upper': 'Text.Upper', 'lower': 'Text.Lower',
                     'title': 'Text.Proper', 'proper': 'Text.Proper'}
        m_func = func_map.get(case_mode)
        if m_func:
            transforms = [f'{{"{c["name"]}", {m_func}, type text}}' for c in text_cols]
            transforms_str = ', '.join(transforms)
            steps.append(f'  CaseFixed = Table.TransformColumns({last_step}, {{{transforms_str}}})')
            last_step = 'CaseFixed'

    # 5. Replace null values
    replace_nulls = cfg.get('replace_nulls')
    if replace_nulls and isinstance(replace_nulls, dict):
        for col_name, default_val in replace_nulls.items():
            step_name = f'NullFilled_{col_name.replace(" ", "_")}'
            if isinstance(default_val, str):
                val_expr = f'"{default_val}"'
            elif isinstance(default_val, (int, float)):
                val_expr = str(default_val)
            else:
                val_expr = f'"{default_val}"'
            steps.append(f'  {step_name} = Table.ReplaceValue({last_step}, null, {val_expr}, '
                        f'Replacer.ReplaceValue, {{"{col_name}"}})')
            last_step = step_name

    # 6. Error handling (replace error values with null)
    if cfg.get('error_handling') and columns:
        replacements = ', '.join(f'{{"{c["name"]}", null}}' for c in columns)
        steps.append(f'  ErrorsHandled = Table.ReplaceErrorValues({last_step}, {{{replacements}}})')
        last_step = 'ErrorsHandled'

    return steps, last_step


# ─── M Expression Builder (prevents comma/syntax errors by construction) ───

def build_m_expression(csv_path, columns=None, include_error_handling=True,
                       skip_rows=0, delimiter=","):
    """
    Build a correct M (Power Query) expression for CSV import.
    All commas and 'in' clause are correct by design.

    When skip_rows > 0, uses Lines.FromBinary approach:
      1. Read entire file as text lines (Lines.FromBinary)
      2. Skip junk lines (List.Skip) — removes BEFORE CSV parsing
      3. Rejoin clean lines (Text.Combine)
      4. Convert back to binary (Text.ToBinary)
      5. Parse clean CSV with Csv.Document

    This guarantees Csv.Document sees the header as Row 1,
    ensuring correct column count and column name detection.

    Args:
        csv_path: Absolute path to CSV file (backslashes will be escaped)
        columns: List of {'name': str, 'type': str} for TransformColumnTypes
                 If None, skips type transform step
        include_error_handling: If True (default), adds Table.ReplaceErrorValues step
                                 to handle inf/nan/error values in CSV data
        skip_rows: Number of junk/comment rows to skip before the real header row.
                   Common in CSVs with "REPORT EXPORT WIZARD", "System Message",
                   or other metadata lines before the actual data header.
                   Use 0 (default) for CSVs where row 1 is the header.
        delimiter: CSV field delimiter. Default "," (comma).
                   Use "|" for pipe-delimited, ";" for semicolon-delimited files.

    Returns:
        List of M expression lines (correct syntax guaranteed)
    """
    csv_path = csv_path.replace('\\', '\\\\')

    steps = []

    if skip_rows > 0:
        # Lines.FromBinary approach — skip junk BEFORE CSV parsing
        # This ensures Csv.Document sees header as the first row
        steps.append(f'  RawContents = File.Contents("{csv_path}")')
        steps.append(f'  AllLines = Lines.FromBinary(RawContents, null, null, 65001)')
        steps.append(f'  CleanLines = List.Skip(AllLines, {skip_rows})')
        steps.append(f'  CombinedText = Text.Combine(CleanLines, "#(cr)#(lf)")')
        steps.append(f'  CleanBinary = Text.ToBinary(CombinedText, 65001)')
        steps.append(f'  Source = Csv.Document(CleanBinary, [Delimiter="{delimiter}", Encoding=65001, QuoteStyle=QuoteStyle.None])')
    else:
        steps.append(f'  Source = Csv.Document(File.Contents("{csv_path}"), [Delimiter="{delimiter}", Encoding=65001, QuoteStyle=QuoteStyle.None])')

    steps.append(f'  PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true])')
    # Clean column names: remove BOM (U+FEFF), ZWNJ (U+200C), ZWS (U+200B), NBSP, then trim whitespace
    # This prevents "column wasn't found" errors from invisible Unicode chars in CSV headers
    steps.append('  CleanedHeaders = Table.TransformColumnNames(PromotedHeaders, each '
                 'let t1 = Text.Replace(_, "#(FEFF)", ""), '
                 't2 = Text.Replace(t1, "#(200C)", ""), '
                 't3 = Text.Replace(t2, "#(200B)", ""), '
                 't4 = Text.Replace(t3, "#(00A0)", " ") '
                 'in Text.Trim(t4))')

    last_step = 'CleanedHeaders'

    # Add TransformColumnTypes if columns have type info
    # NOTE: Only add when NOT using skip_rows, because with dirty CSVs
    # the Power Query column names may differ from expected names
    if columns and skip_rows == 0:
        type_pairs = []
        for c in columns:
            ctype = c.get('type', 'string')
            m_type = M_TYPE_MAP.get(ctype, 'type text')
            type_pairs.append(f'{{"{c["name"]}", {m_type}}}')
        if type_pairs:
            types_str = ', '.join(type_pairs)
            steps.append(f'  ChangedTypes = Table.TransformColumnTypes(CleanedHeaders, {{{types_str}}})')
            last_step = 'ChangedTypes'

    # Add ReplaceErrorValues if requested
    # NOTE: Only add when NOT using skip_rows (same reason as above)
    if include_error_handling and columns and skip_rows == 0:
        replacements = ', '.join(f'{{"{c["name"]}", null}}' for c in columns)
        steps.append(f'  CleanedErrors = Table.ReplaceErrorValues({last_step}, {{{replacements}}})')
        last_step = 'CleanedErrors'

    # Build final expression with correct commas
    # Rule: every step EXCEPT the last one gets a trailing comma
    lines = ['let']
    for i, step in enumerate(steps):
        if i < len(steps) - 1:
            lines.append(step + ',')
        else:
            lines.append(step)
    lines.append('in')
    lines.append(f'  {last_step}')

    return lines


# ─── Model.bim Builder (Fix #5 — Relationships/Star Schema) ───

def make_model_bim(project_name, tables, relationships=None):
    """
    Build model.bim with multiple tables and relationships.
    tables = [{'name': 'Sales', 'csv_path': '...', 'columns': [{'name':'col','type':'string'}],
               'measures': [{'name':'Total','expression':'SUM(...)','format':'#,##0'}],
               'skip_rows': 9, 'delimiter': ','}]
    relationships = [{'from_table':'Sales','from_col':'product_id',
                      'to_table':'Products','to_col':'product_id'}]

    Table dict keys:
      name (str): Table name in the model
      csv_path (str): Absolute path to CSV file
      columns (list): [{'name': 'col', 'type': 'string'}]
      measures (list): Optional DAX measures
      m_expression (list): Optional custom M expression lines (overrides auto-generation)
      skip_rows (int): Number of junk/metadata rows to skip before header (default: 0)
      delimiter (str): CSV field delimiter (default: ","). Use "|" or ";" as needed.
    """
    model_tables = []
    for t in tables:
        # Auto-detect columns from CSV if not explicitly provided
        user_cols = t.get('columns', [])
        if not user_cols and t.get('csv_path'):
            try:
                detected = read_csv_headers(
                    t['csv_path'],
                    skip_rows=t.get('skip_rows', 0),
                    delimiter=t.get('delimiter', ',')
                )
                user_cols = [{'name': c, 'type': 'string'} for c in detected]
            except Exception:
                pass

        cols = [{'name': c['name'], 'dataType': c.get('type','string'),
                 'sourceColumn': c['name']} for c in user_cols]
        measures = [{'name': m['name'], 'expression': m['expression'],
                     'formatString': m.get('format','')} for m in t.get('measures',[])]
        # Support custom M expressions (e.g., with Table.TransformColumnTypes)
        m_expr = t.get('m_expression', None)
        if m_expr is None:
            # Auto-generate M expression using build_m_expression
            # Supports skip_rows and delimiter from table dict
            m_expr = build_m_expression(
                csv_path=t.get('csv_path', ''),
                columns=user_cols if user_cols else None,
                include_error_handling=False,
                skip_rows=t.get('skip_rows', 0),
                delimiter=t.get('delimiter', ',')
            )
        partition = {
            'name': t['name'], 'mode': 'import',
            'source': {'type': 'm', 'expression': m_expr}
        }
        tbl = {'name': t['name'], 'columns': cols, 'partitions': [partition]}
        if measures:
            tbl['measures'] = measures
        model_tables.append(tbl)

    model = {
        'name': project_name,
        'compatibilityLevel': 1567,
        'model': {
            'culture': 'en-US',
            'defaultPowerBIDataSourceVersion': 'powerBI_V3',
            'tables': model_tables
        }
    }

    if relationships:
        rels = []
        for i, r in enumerate(relationships):
            rels.append({
                'name': f'{r["from_table"]}_{r["from_col"]}_{r["to_table"]}_{r["to_col"]}',
                'fromTable': r['from_table'], 'fromColumn': r['from_col'],
                'toTable': r['to_table'], 'toColumn': r['to_col'],
                'crossFilteringBehavior': r.get('cross_filter', 1)
            })
        model['model']['relationships'] = rels

    return model


# ─── Report Builder (Fix #4 — Multi-page) ───

def make_report_json(pages, page_bg=None):
    """
    Build complete report.json with multiple pages.
    pages = [{'name': 'Overview', 'visuals': [visual_container, ...]}, ...]
    page_bg: Optional page background color (e.g. '#F0F2F5' for light gray)
    """
    report_config = {
        'version': '5.66',  # PBI Desktop uses 5.66 (downgraded from 5.70)
        'themeCollection': {'baseTheme': {'name': 'CY24SU11',
            'version': {'visual':'2.6.0','report':'3.1.0','page':'2.3.0'}, 'type': 2}},
        'activeSectionIndex': 0,
        'defaultDrillFilterOtherVisuals': True,
        'linguisticSchemaSyncVersion': 2,
        'models': [{'id': 0, 'name': '', 'tables': []}],
        'settings': {
            'useNewFilterPaneExperience': True, 'allowChangeFilterTypes': True,
            'useStylableVisualContainerHeader': True, 'queryLimitOption': 6,
            'useEnhancedTooltips': True, 'exportDataMode': 1,
            'useDefaultAggregateDisplayName': True
        }
    }
    sections = []
    for i, page in enumerate(pages):
        # Build page-level config with optional background color
        page_config = {}
        if page_bg:
            page_config['background'] = {
                'color': {'solid': {'color': page_bg}},
                'transparency': 0
            }
        sec = {
            'config': json.dumps(page_config, separators=(',', ':')) if page_config else '{}',
            'displayName': page['name'],
            'displayOption': 1, 'filters': '[]',
            'height': 720.0, 'width': 1280.0,
            'name': _id(), 'ordinal': i,
            'visualContainers': page.get('visuals', [])
        }
        sections.append(sec)

    return {
        'config': json.dumps(report_config, separators=(',',':')),
        'layoutOptimization': 0,
        'resourcePackages': [{'resourcePackage': {
            'disabled': False,
            'items': [{'name': 'CY24SU11', 'path': 'BaseThemes/CY24SU11.json', 'type': 202}],
            'name': 'SharedResources', 'type': 2
        }}],
        'sections': sections
    }


# ─── Theme Builder (Fix #9) ───

def make_custom_theme(name='Custom', bg_color='#1E1E2E', fg_color='#FFFFFF',
                      accent_colors=None):
    """Generate custom theme config for report.json"""
    colors = accent_colors or ['#89B4FA','#F38BA8','#A6E3A1','#FAB387','#CBA6F7',
                                '#94E2D5','#F9E2AF','#EBA0AC','#74C7EC','#B4BEFE']
    return {
        'name': name,
        'dataColors': colors,
        'background': bg_color,
        'foreground': fg_color,
        'tableAccent': colors[0]
    }


# ─── Bookmarks (Fix #14) ───

def make_bookmark(name, display_name, visual_states=None):
    """
    Create a bookmark entry.
    visual_states = {'visual_name': True/False} — True=visible
    """
    return {
        'name': name,
        'displayName': display_name,
        'explorationState': {
            'version': '1.0',
            'activeSection': None,
            'filters': {'byVisual': visual_states or {}}
        }
    }


# ─── Validation & Auto-Fix System ───
import re as _re

VALID_DATA_TYPES = {'string', 'int64', 'double', 'dateTime', 'boolean', 'decimal'}
VALID_AGG_FUNCTIONS = {0, 1, 2, 3, 4, 5, 6}  # Sum,Avg,Count,Min,Max,CountNonNull,Median
NON_DATA_VISUALS = {'textbox', 'shape', 'image', 'actionButton', 'bookmarkNavigator', 'groupVisual'}

# Known-good built-in visual types for PBIP format (confirmed working in PBI Desktop Feb 2026)
VALID_BUILTIN_VISUALS = {
    # Data charts
    'barChart', 'columnChart', 'clusteredBarChart', 'clusteredColumnChart',
    'lineChart', 'areaChart', 'lineClusteredColumnComboChart', 'lineStackedColumnComboChart',
    'donutChart', 'pieChart', 'waterfallChart',
    'scatterChart', 'treemap', 'gauge', 'kpi',
    # Tables
    'table', 'tableEx', 'matrix', 'pivotTable', 'multiRowCard',
    # Cards
    'card',
    # Maps
    'map', 'filledMap',
    # Slicers
    'slicer',
    # Non-data
    'textbox', 'shape', 'image', 'actionButton', 'bookmarkNavigator', 'groupVisual',
    # Decomposition/AI
    'decompositionTreeVisual', 'qnaVisual', 'keyDriversVisual',
}

# Visual type aliases: types that may cause CustomVisualNotFound → safe replacement
# stackedColumnChart, stackedBarChart etc. may not be recognized in PBIP format
# The safe approach: use clustered variants with Series role for stacking
VISUAL_TYPE_ALIASES = {
    'stackedColumnChart': 'clusteredColumnChart',
    'stackedBarChart': 'clusteredBarChart',
    'stackedAreaChart': 'areaChart',
    'hundredPercentStackedBarChart': 'clusteredBarChart',
    'hundredPercentStackedColumnChart': 'clusteredColumnChart',
    'hundredPercentStackedAreaChart': 'areaChart',
    'ribbonChart': 'clusteredBarChart',
    'annotatedTimeline': 'lineChart',
    'funnelChart': 'clusteredBarChart',  # NOT a built-in PBIP visual! Causes CustomVisualNotFound
}
VALID_PBIR_VERSIONS = {'4.0'}
VALID_COMPAT_LEVELS = {1550, 1560, 1561, 1562, 1563, 1564, 1565, 1566, 1567, 1568, 1569, 1570, 1571, 1572, 1573, 1574, 1575, 1576, 1577, 1580, 1600, 1604, 1605}
M_TYPE_MAP = {'string': 'type text', 'int64': 'Int64.Type', 'double': 'type number', 'dateTime': 'type date', 'boolean': 'type logical', 'decimal': 'type number'}
UUID_PATTERN = _re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', _re.I)
MAX_PATH_LENGTH = 260  # Windows path limit


def _ai_debug(r, rule_id, severity, file_path, location, current_value, expected, fix_instruction, context=''):
    """Add AI-readable debug context for non-auto-fixable issues."""
    r['ai_debug'].append({
        'rule': rule_id,
        'severity': severity,  # 'critical', 'error', 'warning'
        'file': str(file_path),
        'location': location,
        'current': str(current_value)[:500],
        'expected': str(expected),
        'fix': fix_instruction,
        'context': str(context)[:500]
    })


def validate_pbip(project_dir):
    """
    Comprehensive PBIP validation — catches ALL common errors BEFORE opening in Power BI Desktop.
    Returns dict: {'errors': [...], 'warnings': [...], 'info': [...], 'fixable': [...]}
    """
    r = {'errors': [], 'warnings': [], 'info': [], 'fixable': [], 'ai_debug': []}
    project_dir = Path(project_dir)

    if not project_dir.exists():
        r['errors'].append(f'❌ Project dir not found: {project_dir}')
        _print_results(r)
        return r

    # ═══ Path Length Check (Windows 260 limit) ═══
    proj_path_len = len(str(project_dir.resolve()))
    if proj_path_len > MAX_PATH_LENGTH - 60:
        r['warnings'].append(f'⚠️ [PATH-001] Project path very long ({proj_path_len} chars) — may hit 260 char Windows limit')

    # ═══ File Encoding Check ═══
    for json_file in project_dir.rglob('*.json'):
        try:
            json_file.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            r['fixable'].append(('ENC-001', 'fix_encoding', str(json_file)))
            r['errors'].append(f'❌ [ENC-001] File not UTF-8: {json_file.name} (auto-fixable)')

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 1: File Structure
    # ═══════════════════════════════════════════════════════════════════
    pbip_files = list(project_dir.glob('*.pbip'))
    if not pbip_files:
        r['errors'].append('❌ [STRUCT-001] Missing .pbip file')
        _ai_debug(r, 'STRUCT-001', 'critical', project_dir, 'root directory', 'no .pbip file', '.pbip file required',
            f'Create a .pbip file in {project_dir}. Content: {{"version": "1.0", "artifacts": [{{"report": {{"path": "<ReportFolder>.Report"}}}}]}}. '
            f'The report path should match the .Report folder name in the project directory.')
    elif len(pbip_files) > 1:
        r['errors'].append(f'❌ [STRUCT-002] Multiple .pbip files: {[f.name for f in pbip_files]}')
        _ai_debug(r, 'STRUCT-002', 'critical', project_dir, 'root directory',
            [f.name for f in pbip_files], 'exactly 1 .pbip file',
            f'Delete extra .pbip files, keep only one. Files found: {[str(f) for f in pbip_files]}')
    else:
        try:
            pdata = json.loads(pbip_files[0].read_text(encoding='utf-8'))
            if 'artifacts' not in pdata:
                r['fixable'].append(('STRUCT-003', 'pbip_missing_artifacts', str(pbip_files[0])))
                r['errors'].append('❌ [STRUCT-003] .pbip missing "artifacts" key (auto-fixable)')
            else:
                arts = pdata['artifacts']
                if not any(a.get('report', {}) for a in arts):
                    r['warnings'].append('⚠️ [STRUCT-004] .pbip artifacts missing report reference')
        except json.JSONDecodeError as e:
            r['errors'].append(f'❌ [STRUCT-005] .pbip invalid JSON: {e}')
            _ai_debug(r, 'STRUCT-005', 'critical', pbip_files[0], '.pbip file', str(e), 'valid JSON',
                f'Fix JSON syntax error in {pbip_files[0].name}. Error: {e}. '
                f'Expected format: {{"version": "1.0", "artifacts": [{{"report": {{"path": "<Name>.Report"}}}}]}}')

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 2: Report Folder
    # ═══════════════════════════════════════════════════════════════════
    report_dirs = list(project_dir.glob('*.Report'))
    report_dir = None
    if not report_dirs:
        r['errors'].append('❌ [RPT-001] Missing .Report folder')
        _ai_debug(r, 'RPT-001', 'critical', project_dir, 'root directory', 'no .Report folder', '<Name>.Report folder',
            f'Create a .Report folder in {project_dir}. It must contain: report.json, definition.pbir, and .platform files.')
    else:
        report_dir = report_dirs[0]

        # 2a. report.json
        rpt_json_path = report_dir / 'report.json'
        if not rpt_json_path.exists():
            r['errors'].append('❌ [RPT-002] Missing report.json')
            _ai_debug(r, 'RPT-002', 'critical', report_dir, '.Report folder', 'missing report.json', 'report.json file',
                'Create report.json with: {"config": "<stringified config JSON>", "sections": [<page objects>], "$schema": "..."}. '
                'This is the main file that defines all pages and visuals in the Power BI report.')

        # 2b. definition.pbir
        pbir_path = report_dir / 'definition.pbir'
        if not pbir_path.exists():
            r['fixable'].append(('RPT-003', 'missing_definition_pbir', str(report_dir)))
            r['errors'].append('❌ [RPT-003] Missing definition.pbir (auto-fixable)')
        else:
            try:
                pbir = json.loads(pbir_path.read_text(encoding='utf-8'))
                ver = pbir.get('version', '')
                if ver not in VALID_PBIR_VERSIONS:
                    r['fixable'].append(('RPT-004', 'wrong_pbir_version', str(pbir_path), ver))
                    r['errors'].append(f'❌ [RPT-004] definition.pbir version="{ver}" must be "4.0" (auto-fixable)')
                ds = pbir.get('datasetReference', {})
                if not ds.get('byPath', {}).get('path'):
                    r['errors'].append('❌ [RPT-005] definition.pbir missing datasetReference.byPath.path')
                    _ai_debug(r, 'RPT-005', 'error', pbir_path, 'datasetReference.byPath.path', 'missing', '../<Name>.SemanticModel',
                        'Add datasetReference.byPath.path pointing to the SemanticModel folder. '
                        f'Expected: {{"byPath": {{"path": "../<Name>.SemanticModel"}}, "byConnection": null}}')
                else:
                    ref_path = ds['byPath']['path']
                    expected_model = next(project_dir.glob('*.SemanticModel'), None)
                    if expected_model and expected_model.name not in ref_path:
                        r['fixable'].append(('RPT-006', 'wrong_model_ref', str(pbir_path), expected_model.name))
                        r['errors'].append(f'❌ [RPT-006] definition.pbir points to "{ref_path}" but model is "{expected_model.name}" (auto-fixable)')
            except json.JSONDecodeError as e:
                r['errors'].append(f'❌ [RPT-007] definition.pbir invalid JSON: {e}')
                _ai_debug(r, 'RPT-007', 'critical', pbir_path, 'definition.pbir', str(e), 'valid JSON',
                    f'Fix JSON syntax in definition.pbir. Error: {e}. '
                    f'Expected format: {{"version": "4.0", "datasetReference": {{"byPath": {{"path": "../<Name>.SemanticModel"}}}}}}')

        # 2c. .platform
        rpt_logical_id = None
        platform_rpt = report_dir / '.platform'
        if not platform_rpt.exists():
            r['fixable'].append(('RPT-008', 'missing_platform_report', str(report_dir)))
            r['warnings'].append('⚠️ [RPT-008] Missing .platform in Report (auto-fixable)')
        else:
            try:
                plat = json.loads(platform_rpt.read_text(encoding='utf-8'))
                if plat.get('metadata', {}).get('type') != 'Report':
                    r['fixable'].append(('RPT-009', 'fix_platform_type', str(plat_rpt), 'Report'))
                    r['errors'].append(f'❌ [RPT-009] .platform type must be "Report" (auto-fixable), got "{plat.get("metadata", {}).get("type")}"')
                rpt_logical_id = plat.get('config', {}).get('logicalId', '')
                if not rpt_logical_id:
                    r['warnings'].append('⚠️ [RPT-010] .platform missing logicalId')
                elif not UUID_PATTERN.match(rpt_logical_id):
                    r['fixable'].append(('RPT-012', 'invalid_uuid_report', str(platform_rpt)))
                    r['errors'].append(f'❌ [RPT-012] .platform logicalId "{rpt_logical_id}" is not valid UUID (auto-fixable)')
            except json.JSONDecodeError:
                r['errors'].append('❌ [RPT-011] .platform invalid JSON')
                _ai_debug(r, 'RPT-011', 'error', platform_rpt, '.platform (Report)', 'invalid JSON', 'valid JSON',
                    'Fix JSON syntax in .platform file. Expected format: '
                    '{"$schema": "...", "config": {"version": "1.0", "logicalId": "<uuid>"}, "metadata": {"type": "Report", "displayName": "<name>"}}')

        # RPT-013: report.json config must have models array
        if rpt_json_path and rpt_json_path.exists():
            try:
                _rdata = json.loads(rpt_json_path.read_text(encoding='utf-8'))
                rpt_config_str = _rdata.get('config', '{}')
                if isinstance(rpt_config_str, str):
                    rpt_cfg = json.loads(rpt_config_str)
                else:
                    rpt_cfg = rpt_config_str
                models = rpt_cfg.get('models')
                if models is None:
                    r['fixable'].append(('RPT-013', 'fix_report_models', str(rpt_json_path)))
                    r['errors'].append('❌ [RPT-013] report config missing "models" array — visuals won\'t bind to data! (auto-fixable)')

                # THEME-001: Check theme file
                theme_name = rpt_cfg.get('themeCollection', {}).get('baseTheme', {}).get('name')
                if theme_name and theme_name not in ['CY24SU02', 'CY24SU04', 'CY24SU06', 'CY24SU11', 'FitToPage']:
                    theme_path = report_dir / 'StaticResources' / 'SharedResources' / 'BaseThemes' / f'{theme_name}.json'
                    if not theme_path.exists():
                        r['warnings'].append(f'⚠️ [THEME-001] Custom theme "{theme_name}" specified but file not found in StaticResources')
                        _ai_debug(r, 'THEME-001', 'warning', report_dir, f'config.themeCollection.baseTheme.name',
                            theme_name, f'existing theme file at {theme_path}',
                            f'Create theme file at: {theme_path}, or change theme name to a built-in (e.g., CY24SU11).')

                # BKM-001 & BKM-002: Bookmarks validation
                if 'bookmarks' in rpt_cfg:
                    for bi, bkm in enumerate(rpt_cfg['bookmarks']):
                        try:
                            if not isinstance(bkm, dict) or 'name' not in bkm:
                                r['errors'].append(f'❌ [BKM-002] Bookmark {bi} has invalid data structure (missing name)')
                                _ai_debug(r, 'BKM-002', 'error', rpt_json_path, f'config.bookmarks[{bi}]',
                                    str(bkm)[:200], 'dict with name key',
                                    f'Fix bookmark {bi}: must be a dict with at least a "name" key. Example: {{"name": "Bookmark1", "explorationState": "{{}}"}}.')
                            else:
                                state_str = bkm.get('explorationState', '{}')
                                state = json.loads(state_str) if isinstance(state_str, str) else state_str
                                # BKM-001: Check if bookmark has targets
                                if not state.get('filters', {}).get('byVisual'):
                                    r['warnings'].append(f'⚠️ [BKM-001] Bookmark "{bkm.get("name")}" has no target visuals (Ghost Bookmark)')
                        except Exception:
                            r['errors'].append(f'❌ [BKM-002] Bookmark {bi} has invalid or malformed explorationState')

                # RPT-014: section name/displayName check
                page_names = set()
                for si, _sec in enumerate(_rdata.get('sections', [])):
                    page_name = _sec.get('displayName')
                    if page_name:
                        if page_name in page_names:
                            r['errors'].append(f'❌ [RPT-018] Duplicate page name "{page_name}" in report.json')
                            _ai_debug(r, 'RPT-018', 'error', rpt_json_path, f'sections (displayName)',
                                page_name, 'unique page names',
                                f'Rename one of the duplicate pages. Current duplicate: "{page_name}". '
                                f'Change displayName in one of the sections to make it unique.')
                        page_names.add(page_name)
                    
                    if not _sec.get('name'):
                        r['fixable'].append(('RPT-014', 'fix_section_name', str(rpt_json_path), si))
                        r['errors'].append(f'❌ [RPT-014] Section {si} missing "name" (hex ID) — page may not render (auto-fixable)')
                    if not _sec.get('displayName'):
                        r['fixable'].append(('RPT-014', 'fix_section_displayname', str(rpt_json_path), si))
                        r['warnings'].append(f'⚠️ [RPT-014b] Section {si} missing "displayName" (auto-fixable)')

                    # RPT-015 & RPT-019: page dimensions
                    sw = _sec.get('width', 1280)
                    sh = _sec.get('height', 720)
                    if sw == 0 or sh == 0:
                        r['fixable'].append(('RPT-015', 'fix_section_dims', str(rpt_json_path), si))
                        r['errors'].append(f'❌ [RPT-015] Section {si} has zero width/height ({sw}x{sh}) — page canvas invisible (auto-fixable)')
                    elif sw < 0 or sh < 0 or sw > 10000 or sh > 10000:
                        r['errors'].append(f'❌ [RPT-019] Page "{page_name or si}" has out-of-bounds dimensions ({sw}x{sh})')
                        _ai_debug(r, 'RPT-019', 'error', rpt_json_path, f'sections[{si}].width/height',
                            f'{sw}x{sh}', '1280x720 (standard) or reasonable values',
                            f'Set page dimensions to valid values. Current: width={sw}, height={sh}. '
                            f'Standard: 1280x720, Widescreen: 1920x1080. Max recommended: 3840x2160.')
            except (json.JSONDecodeError, Exception):
                pass

        # RPT-016: Report-level filters validation
        if rpt_json_path and rpt_json_path.exists():
            try:
                _rpt_data = json.loads(rpt_json_path.read_text(encoding='utf-8'))
                rpt_filters = _rpt_data.get('filters', '')
                if rpt_filters and isinstance(rpt_filters, str):
                    try:
                        json.loads(rpt_filters)
                    except json.JSONDecodeError:
                        r['fixable'].append(('RPT-016', 'fix_report_filters', str(rpt_json_path)))
                        r['errors'].append('❌ [RPT-016] report.json has invalid report-level filters JSON string (auto-fixable)')
            except Exception:
                pass

        # RPT-017: File size warning
        if rpt_json_path and rpt_json_path.exists():
            rpt_size_mb = rpt_json_path.stat().st_size / (1024 * 1024)
            if rpt_size_mb > 5:
                r['warnings'].append(f'⚠️ [RPT-017] report.json is {rpt_size_mb:.1f}MB — Power BI Desktop will load slowly (>5MB)')

        # STRUCT-007: .platform and item.config.json conflict
        #   Power BI Desktop CANNOT have both — they are mutually exclusive metadata formats.
        #   .platform is the newer format; item.config.json is legacy.
        plat_rpt = report_dir / '.platform'
        item_cfg_rpt = report_dir / 'item.config.json'
        if plat_rpt.exists() and item_cfg_rpt.exists():
            r['errors'].append('❌ [STRUCT-007] Report folder has BOTH .platform AND item.config.json — Power BI Desktop will refuse to open! Remove item.config.json (auto-fixable)')
            r['fixable'].append(('STRUCT-007', 'platform_itemconfig_conflict', str(item_cfg_rpt)))
        # MDL-038: item.config.json missing in Report (only if .platform also missing)
        elif not item_cfg_rpt.exists() and not plat_rpt.exists():
            r['fixable'].append(('MDL-038', 'missing_item_config_report', str(report_dir)))
            r['warnings'].append('⚠️ [MDL-038] Missing item.config.json in Report folder (auto-fixable)')

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 3: SemanticModel (model.bim) Deep Validation
    # ═══════════════════════════════════════════════════════════════════
    model_tables = {}
    model_dir = None
    model_dirs = list(project_dir.glob('*.SemanticModel'))
    if not model_dirs:
        r['errors'].append('❌ [MDL-001] Missing .SemanticModel folder')
        _ai_debug(r, 'MDL-001', 'critical', project_dir, 'root directory', 'no .SemanticModel folder', '<Name>.SemanticModel folder',
            f'Create a .SemanticModel folder in {project_dir}. It must contain: model.bim and .platform files. '
            f'model.bim defines tables, columns, measures, relationships, and M expressions for data sources.')
    else:
        model_dir = model_dirs[0]
        bim_path = model_dir / 'model.bim'

        # 3a. .platform for model
        mdl_logical_id = None
        plat_mdl = model_dir / '.platform'
        if not plat_mdl.exists():
            r['fixable'].append(('MDL-002', 'missing_platform_model', str(model_dir)))
            r['warnings'].append('⚠️ [MDL-002] Missing .platform in SemanticModel (auto-fixable)')

        # STRUCT-007: .platform and item.config.json conflict in SemanticModel
        item_cfg_mdl = model_dir / 'item.config.json'
        if plat_mdl.exists() and item_cfg_mdl.exists():
            r['errors'].append('❌ [STRUCT-007] SemanticModel folder has BOTH .platform AND item.config.json — Power BI Desktop will refuse to open! Remove item.config.json (auto-fixable)')
            r['fixable'].append(('STRUCT-007', 'platform_itemconfig_conflict', str(item_cfg_mdl)))
        # MDL-037: item.config.json missing in SemanticModel (only if .platform also missing)
        elif not item_cfg_mdl.exists() and not plat_mdl.exists():
            r['fixable'].append(('MDL-037', 'missing_item_config_model', str(model_dir)))
            r['warnings'].append('⚠️ [MDL-037] Missing item.config.json in SemanticModel folder (auto-fixable)')
        else:
            try:
                plat = json.loads(plat_mdl.read_text(encoding='utf-8'))
                if plat.get('metadata', {}).get('type') != 'SemanticModel':
                    r['errors'].append('❌ [MDL-003] .platform type must be "SemanticModel"')
                    _ai_debug(r, 'MDL-003', 'error', plat_mdl, 'metadata.type', plat.get('metadata', {}).get('type'), 'SemanticModel',
                        'Change metadata.type to "SemanticModel" in .platform file. '
                        f'Current value: "{plat.get("metadata", {}).get("type")}".')
                mdl_logical_id = plat.get('config', {}).get('logicalId', '')
                if mdl_logical_id and not UUID_PATTERN.match(mdl_logical_id):
                    r['fixable'].append(('MDL-026', 'invalid_uuid_model', str(plat_mdl)))
                    r['errors'].append(f'❌ [MDL-026] .platform logicalId is not valid UUID (auto-fixable)')
                # Cross-check: Report and Model must have DIFFERENT logicalIds
                if rpt_logical_id and mdl_logical_id and rpt_logical_id == mdl_logical_id:
                    r['fixable'].append(('MDL-027', 'duplicate_logical_ids', str(plat_mdl)))
                    r['errors'].append(f'❌ [MDL-027] Report and Model have SAME logicalId! Must be unique (auto-fixable)')
            except json.JSONDecodeError:
                r['errors'].append('❌ [MDL-004] .platform invalid JSON')
                _ai_debug(r, 'MDL-004', 'error', plat_mdl, '.platform (SemanticModel)', 'invalid JSON', 'valid JSON',
                    'Fix JSON syntax in SemanticModel .platform. Expected: '
                    '{"$schema": "...", "config": {"version": "1.0", "logicalId": "<uuid>"}, "metadata": {"type": "SemanticModel"}}')

        if not bim_path.exists():
            r['errors'].append('❌ [MDL-005] Missing model.bim')
            _ai_debug(r, 'MDL-005', 'critical', model_dir, '.SemanticModel folder', 'no model.bim', 'model.bim file',
                'Create model.bim with Tabular Model schema. Minimum: '
                '{"compatibilityLevel": 1567, "model": {"defaultPowerBIDataSourceVersion": "powerBI_V3", "tables": [...]}}')
        else:
            try:
                mdata = json.loads(bim_path.read_text(encoding='utf-8'))

                # 3b. Top-level keys
                if 'compatibilityLevel' not in mdata:
                    r['errors'].append('❌ [MDL-006] model.bim missing "compatibilityLevel"')
                    _ai_debug(r, 'MDL-006', 'error', bim_path, 'root', 'missing', 'compatibilityLevel: 1567',
                        'Add "compatibilityLevel": 1567 at the top level of model.bim JSON. Valid values: 1550-1605.')
                else:
                    cl = mdata['compatibilityLevel']
                    if cl not in VALID_COMPAT_LEVELS:
                        r['fixable'].append(('MDL-007', 'fix_compat_level', str(bim_path)))
                        r['warnings'].append(f'⚠️ [MDL-007] compatibilityLevel={cl} — unusual (common: 1567+) (auto-fixable)')

                model_obj = mdata.get('model', {})
                if not model_obj:
                    r['errors'].append('❌ [MDL-008] model.bim missing "model" object')
                    _ai_debug(r, 'MDL-008', 'critical', bim_path, 'root', 'missing', '"model": {...}',
                        'Add "model" object to model.bim. It must contain: defaultPowerBIDataSourceVersion, tables array, and optionally relationships.')
                else:
                    if model_obj.get('defaultPowerBIDataSourceVersion') != 'powerBI_V3':
                        r['fixable'].append(('MDL-009', 'wrong_ds_version', str(bim_path)))
                        r['warnings'].append('⚠️ [MDL-009] defaultPowerBIDataSourceVersion should be "powerBI_V3" (auto-fixable)')

                    tables = model_obj.get('tables', [])
                    if not tables:
                        r['errors'].append('❌ [MDL-010] model.bim has no tables')
                        _ai_debug(r, 'MDL-010', 'error', bim_path, 'model.tables', '[]', 'at least 1 table',
                            'Add tables to model.tables array. Each table needs: name, columns, partitions (with M expression for data source).')

                    all_table_names = set()
                    hidden_fields = set() # For MDL-053 check in Visuals
                    RESERVED_DAX = {'CALCULATE', 'SUM', 'AVERAGE', 'MIN', 'MAX', 'IF', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE', 'BLANK', 'FILTER', 'ALL', 'ALLEXCEPT'}

                    for t in tables:
                        tname = t.get('name', '')

                        # MDL-049: Whitespace in Table name
                        if tname != tname.strip():
                            r['fixable'].append(('MDL-049', 'fix_name_whitespace', str(bim_path), 'table', tname))
                            r['warnings'].append(f'⚠️ [MDL-049] Table name "{tname}" has leading or trailing whitespaces (auto-fixable)')
                        
                        # MDL-050: Reserved Keyword
                        if tname.upper() in RESERVED_DAX:
                            r['warnings'].append(f'⚠️ [MDL-050] Table name "{tname}" matches a reserved DAX keyword')
                            
                        # MDL-051: Date Table without Time
                        if tname.lower() in ('date', 'calendar', 'dates') and t.get('dataCategory') != 'Time':
                            r['warnings'].append(f'⚠️ [MDL-051] Table "{tname}" appears to be a Date table but lacks dataCategory="Time"')
                            
                        # MDL-054: Calculated Table missing expression
                        for p in t.get('partitions', []):
                            if p.get('source', {}).get('type') == 'calculated':
                                expr = p.get('source', {}).get('expression')
                                if not expr:
                                    r['fixable'].append(('MDL-054', 'fix_calc_no_expr', str(bim_path), tname, 'table'))
                                    r['errors'].append(f'❌ [MDL-054] Calculated table "{tname}" is missing its DAX expression (auto-fixable)')

                        # STRUCT-006: Table length limit
                        if len(tname) > 100:
                            r['warnings'].append(f'⚠️ [STRUCT-006] Table name "{tname}" exceeds 100 characters length')

                        # Duplicate table names
                        if tname in all_table_names:
                            r['fixable'].append(('MDL-011', 'fix_duplicate_table', str(bim_path), tname))
                            r['errors'].append(f'❌ [MDL-011] Duplicate table name: "{tname}" (auto-fixable)')
                        all_table_names.add(tname)

                        cols = {}
                        for c in t.get('columns', []):
                            cname = c.get('name', '')
                            ctype = c.get('dataType', '')
                            cols[cname] = ctype

                            if c.get('isHidden'):
                                hidden_fields.add(f"{tname}.{cname}")

                            # MDL-049, MDL-050
                            if cname != cname.strip():
                                r['fixable'].append(('MDL-049', 'fix_name_whitespace', str(bim_path), 'column', tname, cname))
                                r['warnings'].append(f'⚠️ [MDL-049] Column name "{cname}" in table "{tname}" has leading or trailing whitespaces (auto-fixable)')
                            if cname.upper() in RESERVED_DAX:
                                r['warnings'].append(f'⚠️ [MDL-050] Column name "{cname}" in table "{tname}" matches a reserved DAX keyword')
                                _ai_debug(r, 'MDL-050', 'warning', bim_path, f'table "{tname}".columns["{cname}"]',
                                    cname, 'non-reserved name',
                                    f'Rename column "{cname}" to avoid conflict with DAX keyword. '
                                    f'Suggestion: prefix with underscore or use descriptive name (e.g., "_{cname}" or "{tname}_{cname}").')

                            # MDL-054: Calculated Column missing expression
                            if c.get('type') == 'calculated' and not c.get('expression'):
                                r['fixable'].append(('MDL-054', 'fix_calc_no_expr', str(bim_path), tname, 'column', cname))
                                r['errors'].append(f'❌ [MDL-054] Calculated column "{cname}" in table "{tname}" is missing its DAX expression (auto-fixable)')

                            # STRUCT-006: Column length limit
                            if len(cname) > 100:
                                r['warnings'].append(f'⚠️ [STRUCT-006] Column "{cname}" in "{tname}" exceeds 100 characters')

                            # MDL-048: Check for geographic names without dataCategory
                            geom_keywords = ['country', 'city', 'state', 'province', 'zip', 'postal', 'latitude', 'longitude']
                            if ctype == 'string' and any(k in cname.lower() for k in geom_keywords) and not c.get('dataCategory'):
                                r['warnings'].append(f'ℹ️ [MDL-048] Column "{cname}" in table "{tname}" looks geographic but lacks dataCategory')

                            # MDL-046: sortByColumn validation
                            sort_by = c.get('sortByColumn')
                            if sort_by and sort_by not in [col.get('name') for col in t.get('columns', [])]:
                                r['errors'].append(f'❌ [MDL-046] Column "{cname}" sorts by "{sort_by}" which does not exist in table "{tname}"')
                                available_cols = [col.get('name') for col in t.get('columns', []) if col.get('name') != cname]
                                _ai_debug(r, 'MDL-046', 'error', bim_path, f'table "{tname}".column "{cname}".sortByColumn',
                                    sort_by, f'one of: {available_cols}',
                                    f'Column "{cname}" has sortByColumn="{sort_by}" but that column does not exist. '
                                    f'Available columns in "{tname}": {available_cols}. Remove sortByColumn or fix the reference.')

                            # Column dataType validation
                            if ctype and ctype not in VALID_DATA_TYPES:
                                r['fixable'].append(('MDL-012', 'fix_invalid_datatype', str(bim_path), tname, cname, ctype))
                                r['errors'].append(f'❌ [MDL-012] Table "{tname}" column "{cname}": invalid dataType "{ctype}" (auto-fixable)')

                            # Column must have sourceColumn
                            if not c.get('sourceColumn') and c.get('type') != 'calculated':
                                r['fixable'].append(('MDL-013', 'fix_missing_source_col', str(bim_path), tname, cname))
                                r['warnings'].append(f'⚠️ [MDL-013] Table "{tname}" column "{cname}": missing sourceColumn (auto-fixable)')

                        measures = {}
                        for m in t.get('measures', []):
                            mname = m.get('name', '')
                            mexpr = m.get('expression', '')
                            measures[mname] = mexpr

                            if m.get('isHidden'):
                                hidden_fields.add(f"{tname}.{mname}")

                            # MDL-049, MDL-050
                            if mname != mname.strip():
                                r['fixable'].append(('MDL-049', 'fix_name_whitespace', str(bim_path), 'measure', tname, mname))
                                r['warnings'].append(f'⚠️ [MDL-049] Measure name "{mname}" in table "{tname}" has leading or trailing whitespaces (auto-fixable)')
                            if mname.upper() in RESERVED_DAX:
                                r['warnings'].append(f'⚠️ [MDL-050] Measure name "{mname}" in table "{tname}" matches a reserved DAX keyword')
                                _ai_debug(r, 'MDL-050', 'warning', bim_path, f'table "{tname}".measures["{mname}"]',
                                    mname, 'non-reserved name',
                                    f'Rename measure "{mname}" to avoid conflict with DAX keyword. '
                                    f'Suggestion: use descriptive name like "Total_{mname}" or "{tname}_{mname}".')

                            # Measure must have expression
                            if not mexpr:
                                r['errors'].append(f'❌ [MDL-014] Table "{tname}" measure "{mname}": missing expression (DAX)')
                                available_cols = list(cols.keys())
                                _ai_debug(r, 'MDL-014', 'error', bim_path, f'table "{tname}".measures["{mname}"].expression',
                                    'empty/missing', 'valid DAX expression',
                                    f'Write a DAX expression for measure "{mname}" in table "{tname}". '
                                    f'Available columns: {available_cols}. '
                                    f'Examples: SUM({tname}[{available_cols[0]}]) or COUNTROWS({tname})' if available_cols else
                                    f'Write a DAX expression. Example: COUNTROWS({tname})')

                            # Basic DAX syntax check
                            if mexpr and isinstance(mexpr, (list, str)):
                                dax = ''.join(mexpr) if isinstance(mexpr, list) else mexpr
                                if dax.count('(') != dax.count(')'):
                                    r['fixable'].append(('MDL-015', 'fix_dax_parens', str(bim_path), tname, mname))
                                    r['errors'].append(f'❌ [MDL-015] Table "{tname}" measure "{mname}": unbalanced parentheses in DAX (auto-fixable)')

                                # MDL-045: Self-referencing measure check
                                if mname in dax and _re.search(r'\b' + _re.escape(mname) + r'\b', dax):
                                    r['fixable'].append(('MDL-045', 'fix_self_ref_measure', str(bim_path), tname, mname))
                                    r['errors'].append(f'❌ [MDL-045] Measure "{mname}" in table "{tname}" references itself in its DAX expression (auto-fixable)')

                        # Column/Measure name collision (ERR-DAX-002 ref)
                        col_measure_overlap = set(cols.keys()) & set(measures.keys())
                        if col_measure_overlap:
                            r['fixable'].append(('MDL-028', 'fix_col_measure_collision', str(bim_path), tname, list(col_measure_overlap)))
                            r['errors'].append(f'❌ [MDL-028] Table "{tname}": column and measure share names: {col_measure_overlap} — causes ambiguity! (auto-fixable)')

                        has_partition = bool(t.get('partitions', []))
                        model_tables[tname] = {'columns': set(cols.keys()), 'measures': set(measures.keys()), 'col_types': cols, 'has_partition': has_partition}

                        if not t.get('columns') and not t.get('measures'):
                            r['fixable'].append(('MDL-016', 'fix_empty_table', str(bim_path), tname))
                            r['warnings'].append(f'⚠️ [MDL-016] Table "{tname}" has no columns (auto-fixable: remove table)')
                        elif not t.get('columns'):
                            r['warnings'].append(f'⚠️ [MDL-016] Table "{tname}" has no columns')
                        if not t.get('partitions'):
                            r['warnings'].append(f'⚠️ [MDL-017] Table "{tname}" has no partitions')
                            _ai_debug(r, 'MDL-017', 'warning', bim_path, f'table "{tname}".partitions',
                                '[]', 'at least 1 partition with M expression',
                                f'Add a partition with M expression to table "{tname}". '
                                f'Minimum: {{"name": "{tname}", "source": {{"type": "m", "expression": ["let ..."]}}}}. '
                                f'The M expression should define how to load data (e.g., from CSV via File.Contents).')

                        # M Expression checks
                        for p in t.get('partitions', []):
                            src = p.get('source', {})
                            if src.get('type') == 'm':
                                m_lines = src.get('expression', [])
                                if not m_lines:
                                    r['errors'].append(f'❌ [MDL-018] Table "{tname}": partition has empty M expression')
                                    _ai_debug(r, 'MDL-018', 'error', bim_path, f'table "{tname}".partitions[].source.expression',
                                        'empty', 'valid M expression array',
                                        f'Add M expression to the partition. For CSV data: '
                                        f'["let", "  Source = Csv.Document(File.Contents(\"data.csv\")),", "in", "  Source"]')
                                    continue

                                # ERR-GEN-009: M expression should be array, not string
                                if isinstance(m_lines, str):
                                    r['fixable'].append(('GEN-009', 'fix_m_expr_format', str(bim_path), tname))
                                    r['warnings'].append(f'⚠️ [GEN-009] Table "{tname}": M expression is string, should be array of lines (auto-fixable)')

                                m_text = ' '.join(m_lines) if isinstance(m_lines, list) else str(m_lines)

                                # ERR-GENQ-002: CSV without TransformColumnTypes
                                if 'Csv.Document' in m_text and 'TransformColumnTypes' not in m_text:
                                    r['fixable'].append(('GENQ-002', 'csv_no_types', str(bim_path), tname))
                                    r['errors'].append(
                                        f'🔥 [GENQ-002] Table "{tname}": CSV import without Table.TransformColumnTypes '
                                        f'→ ALL columns will be text! Aggregations WILL FAIL (auto-fixable)')

                                # ERR-PQ-008: CSV encoding check (should use 65001 = UTF-8)
                                if 'Csv.Document' in m_text and 'Encoding' not in m_text:
                                    r['fixable'].append(('PQ-008', 'fix_csv_encoding', str(bim_path), tname))
                                    r['warnings'].append(f'⚠️ [PQ-008] Table "{tname}": CSV import without explicit Encoding — Thai/Unicode data may display incorrectly (auto-fixable)')

                                # M expression must have "in" keyword
                                if 'let' in m_text.lower() and ' in ' not in m_text.lower() and '\nin' not in m_text.lower():
                                    r['fixable'].append(('MDL-019', 'fix_m_missing_in', str(bim_path), tname))
                                    r['errors'].append(f'❌ [MDL-019] Table "{tname}": M expression has "let" but missing "in" (auto-fixable)')

                                # Check M expression references existing file
                                if 'File.Contents(' in m_text:
                                    file_refs = _re.findall(r'File\.Contents\("([^"]+)"\)', m_text)
                                    for fref in file_refs:
                                        fp = Path(fref)
                                        if not fp.is_absolute():
                                            fp = project_dir / fref
                                        if not fp.exists():
                                            r['warnings'].append(f'⚠️ [MDL-020] Table "{tname}": M references file "{fref}" which does not exist')
                                            _ai_debug(r, 'MDL-020', 'warning', bim_path, f'table "{tname}".M expression',
                                                fref, 'existing file path',
                                                f'File "{fref}" referenced in M expression does not exist. '
                                                f'Either create the file at that path or update the M expression to point to the correct CSV/data file.')

                                # ═══ NEW: M Syntax Validation (Fix double-escape & token errors) ═══

                                # MDL-034: Double-escaped quotes in M expression
                                # This causes "Token ',' expected" error in Power BI
                                if isinstance(m_lines, list):
                                    raw_json = json.dumps(m_lines)
                                    if '\\\\\\"' in raw_json or '\\\\\\\\' in raw_json.replace('\\\\\\\\\\\\\\\\', ''):
                                        # Check for patterns like \\\" which indicate double-escaped quotes
                                        for ml_idx, ml in enumerate(m_lines):
                                            if '\\"' in ml and '{\\"' in ml:
                                                r['fixable'].append(('MDL-034', 'fix_m_double_escape', str(bim_path), tname))
                                                r['errors'].append(
                                                    f'🔥 [MDL-034] Table "{tname}": M expression has double-escaped quotes '
                                                    f'→ causes "Token comma expected" error in Power BI! (auto-fixable)')
                                                break

                                # MDL-035: Unbalanced curly braces in TransformColumnTypes
                                # M requires exactly matched pairs: { {col, type}, {col, type} }
                                if 'TransformColumnTypes' in m_text:
                                    # Extract the types argument portion
                                    tct_match = _re.search(r'TransformColumnTypes\([^,]+,\s*(.+?)\)', m_text)
                                    if tct_match:
                                        types_part = tct_match.group(1)
                                        open_braces = types_part.count('{')
                                        close_braces = types_part.count('}')
                                        if open_braces != close_braces:
                                            r['errors'].append(
                                                f'❌ [MDL-035] Table "{tname}": TransformColumnTypes has unbalanced '
                                                f'braces ({{ ={open_braces}, }} ={close_braces}) → "Token comma expected" error')
                                            _ai_debug(r, 'MDL-035', 'error', bim_path, f'table "{tname}".M expression (TransformColumnTypes)',
                                                f'open={open_braces}, close={close_braces}', 'balanced braces',
                                                f'Fix the TransformColumnTypes braces in table "{tname}". '
                                                f'Each column type pair must be wrapped in {{}}. '
                                                f'Format: Table.TransformColumnTypes(Source, {{{{"Col1", type text}}, {{"Col2", Int64.Type}}}})')

                                # MDL-036: CSV import without ReplaceErrorValues
                                # inf/nan values in CSV cause type conversion errors
                                if 'Csv.Document' in m_text and 'TransformColumnTypes' in m_text:
                                    if 'ReplaceErrorValues' not in m_text:
                                        r['fixable'].append(('MDL-036', 'add_replace_error_values', str(bim_path), tname))
                                        r['errors'].append(
                                            f'🔥 [MDL-036] Table "{tname}": CSV import with type casting but no '
                                            f'Table.ReplaceErrorValues — inf/nan values will show as "Error" (auto-fixable)')

                    # Relationship validation
                    rel_pairs = set()
                    active_rels = {} # tuple(from_t, to_t) -> count
                    for rel in model_obj.get('relationships', []):
                        from_t = rel.get('fromTable', '')
                        from_c = rel.get('fromColumn', '')
                        to_t = rel.get('toTable', '')
                        to_c = rel.get('toColumn', '')
                        is_active = rel.get('isActive', True) # Default is True in Tabular models
                        
                        if is_active:
                            pair = tuple(sorted([from_t, to_t]))
                            active_rels[pair] = active_rels.get(pair, 0) + 1

                        # Self-join detection
                        if from_t and from_t == to_t:
                            r['fixable'].append(('MDL-029', 'fix_self_join', str(bim_path), from_t, from_c, to_c))
                            r['warnings'].append(f'⚠️ [MDL-029] Self-join relationship on table "{from_t}" — usually a mistake (auto-fixable: remove)')

                        # Duplicate relationship
                        pair_key = f'{from_t}.{from_c}->{to_t}.{to_c}'
                        if pair_key in rel_pairs:
                            r['fixable'].append(('MDL-030', 'fix_duplicate_relationship', str(bim_path), pair_key))
                            r['errors'].append(f'❌ [MDL-030] Duplicate relationship: {pair_key} (auto-fixable)')
                        rel_pairs.add(pair_key)

                    # MDL-044: Multiple Active Relationships
                    for pair, count in active_rels.items():
                        if count > 1:
                            r['fixable'].append(('MDL-044', 'fix_multi_active_rel', str(bim_path), pair[0], pair[1]))
                            r['errors'].append(f'❌ [MDL-044] Multiple active relationships found between tables {pair[0]} and {pair[1]} (auto-fixable)')

                        if from_t not in model_tables:
                            r['errors'].append(f'❌ [MDL-021] Relationship fromTable "{from_t}" not found')
                            _ai_debug(r, 'MDL-021', 'error', bim_path, f'relationships[].fromTable',
                                from_t, f'one of: {list(model_tables.keys())}',
                                f'Relationship references table "{from_t}" which does not exist. '
                                f'Available tables: {list(model_tables.keys())}. Fix the fromTable name or remove this relationship.')
                        elif from_c not in model_tables[from_t]['columns']:
                            r['errors'].append(f'❌ [MDL-022] Relationship fromColumn "{from_c}" not in table "{from_t}"')
                            _ai_debug(r, 'MDL-022', 'error', bim_path, f'relationships[].fromColumn (table "{from_t}")',
                                from_c, f'one of: {list(model_tables[from_t]["columns"])}',
                                f'Column "{from_c}" not found in table "{from_t}". '
                                f'Available columns: {list(model_tables[from_t]["columns"])}. Fix column name or remove relationship.')

                        if to_t not in model_tables:
                            r['errors'].append(f'❌ [MDL-023] Relationship toTable "{to_t}" not found')
                            _ai_debug(r, 'MDL-023', 'error', bim_path, f'relationships[].toTable',
                                to_t, f'one of: {list(model_tables.keys())}',
                                f'Relationship references table "{to_t}" which does not exist. '
                                f'Available tables: {list(model_tables.keys())}. Fix the toTable name or remove this relationship.')
                        elif to_c not in model_tables[to_t]['columns']:
                            r['errors'].append(f'❌ [MDL-024] Relationship toColumn "{to_c}" not in table "{to_t}"')
                            _ai_debug(r, 'MDL-024', 'error', bim_path, f'relationships[].toColumn (table "{to_t}")',
                                to_c, f'one of: {list(model_tables[to_t]["columns"])}',
                                f'Column "{to_c}" not found in table "{to_t}". '
                                f'Available columns: {list(model_tables[to_t]["columns"])}. Fix column name or remove relationship.')

                # MDL-031: Inactive relationship check
                for rel in model_obj.get('relationships', []):
                    if 'isActive' in rel and rel['isActive'] is False:
                        r['fixable'].append(('MDL-031', 'fix_inactive_rel', str(bim_path), rel.get('fromTable',''), rel.get('fromColumn',''), rel.get('toTable',''), rel.get('toColumn','')))
                        r['warnings'].append(f'⚠️ [MDL-031] Inactive relationship: {rel.get("fromTable")}.{rel.get("fromColumn")} → {rel.get("toTable")}.{rel.get("toColumn")} — will not filter visuals (auto-fixable: remove)')

                # MDL-032: Table has no columns
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if not t.get('columns') and not t.get('measures'):
                        r['errors'].append(f'❌ [MDL-032] Table "{tname}" has no columns and no measures — visuals will be empty')
                        _ai_debug(r, 'MDL-032', 'error', bim_path, f'table "{tname}"',
                            'no columns, no measures', 'at least 1 column or measure',
                            f'Add columns to table "{tname}" or remove this empty table from model.bim.')

                # MDL-033: Partition source type check
                for t in model_obj.get('tables', []):
                    for p in t.get('partitions', []):
                        p_type = p.get('source', {}).get('type')
                        if p_type and p_type not in ('m', 'calculated', 'none'):
                            r['fixable'].append(('MDL-033', 'fix_partition_type', str(bim_path), t.get('name','')))
                            r['warnings'].append(f'⚠️ [MDL-033] Table "{t.get("name")}": partition type="{p_type}" — unusual (auto-fixable: set to "m")')

                # MDL-039: DAX measure references non-existent table
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        # Extract table references from DAX like SUM(TableName[Column])
                        dax_table_refs = _re.findall(r"(\w+)\[", dax)
                        for dax_ref in dax_table_refs:
                            if dax_ref not in all_table_names and dax_ref not in ('BLANK', 'TRUE', 'FALSE', 'IF', 'VAR', 'RETURN'):
                                r['fixable'].append(('MDL-039', 'fix_dax_table_ref', str(bim_path), tname, mname, dax_ref))
                                r['errors'].append(f'❌ [MDL-039] Table "{tname}" measure "{mname}": DAX references table "{dax_ref}" which does not exist in model (auto-fixable: comment out measure)')

                # MDL-040 & MDL-052: Relationship column type checking
                for rel in model_obj.get('relationships', []):
                    from_t = rel.get('fromTable', '')
                    from_c = rel.get('fromColumn', '')
                    to_t = rel.get('toTable', '')
                    to_c = rel.get('toColumn', '')
                    if from_t in model_tables and to_t in model_tables:
                        from_type = model_tables[from_t].get('col_types', {}).get(from_c)
                        to_type = model_tables[to_t].get('col_types', {}).get(to_c)
                        
                        if from_type and to_type and from_type != to_type:
                            r['warnings'].append(
                                f'⚠️ [MDL-040] Relationship {from_t}.{from_c} ({from_type}) → {to_t}.{to_c} ({to_type}): '
                                f'column types don\'t match — may cause filter/join issues')
                            _ai_debug(r, 'MDL-040', 'warning', bim_path, f'relationship {from_t}.{from_c} → {to_t}.{to_c}',
                                f'{from_type} vs {to_type}', 'matching data types',
                                f'Change one column\'s dataType to match. {from_t}.{from_c}={from_type}, {to_t}.{to_c}={to_type}.')
                                
                        if from_type in ('double', 'decimal') or to_type in ('double', 'decimal'):
                            r['warnings'].append(f'⚠️ [MDL-052] Relationship uses Float/Decimal columns {from_t}.{from_c} → {to_t}.{to_c} (Precision mismatch risk)')

                # MDL-042: Absolute CSV file paths in M expressions
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for p in t.get('partitions', []):
                        src = p.get('source', {})
                        if src.get('type') == 'm':
                            m_lines = src.get('expression', [])
                            m_text = ' '.join(m_lines) if isinstance(m_lines, list) else str(m_lines)
                            abs_paths = _re.findall(r'File\.Contents\("([A-Za-z]:\\[^"]+)"\)', m_text)
                            for abs_path in abs_paths:
                                r['warnings'].append(
                                    f'⚠️ [MDL-042] Table "{tname}": M expression uses absolute path "{abs_path}" '
                                    f'— moving project to another machine will break data source')

                # MDL-043: RLS Expression Validation
                for role in model_obj.get('roles', []):
                    rname = role.get('name', 'Unknown')
                    for tp in role.get('tablePermissions', []):
                        tname_rls = tp.get('name', '')
                        expr = tp.get('filterExpression', '')
                        if expr:
                            dax = ''.join(expr) if isinstance(expr, list) else expr
                            if dax.count('(') != dax.count(')'):
                                r['errors'].append(f'❌ [MDL-043] RLS role "{rname}" on table "{tname_rls}": unbalanced parentheses in filterExpression')
                                _ai_debug(r, 'MDL-043', 'error', bim_path, f'roles["{rname}"].tablePermissions["{tname_rls}"].filterExpression',
                                    dax[:200], 'balanced parentheses',
                                    f'Fix DAX filter expression for RLS role "{rname}". Open parens: {dax.count("(")}, Close: {dax.count(")")}')
                            if tname_rls and tname_rls not in all_table_names:
                                r['errors'].append(f'❌ [MDL-043] RLS role "{rname}" assigned to non-existent table "{tname_rls}"')
                                _ai_debug(r, 'MDL-043', 'error', bim_path, f'roles["{rname}"].tablePermissions[].name',
                                    tname_rls, f'one of: {list(all_table_names)}',
                                    f'RLS role \"{rname}\" references table \"{tname_rls}\" which does not exist. Available: {list(all_table_names)}.')

                # ═══ NEW: DAX Best Practices (MDL-055 → MDL-062) ═══
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    table_measures = t.get('measures', [])

                    # MDL-058: Table has > 100 measures (complexity warning)
                    if len(table_measures) > 100:
                        r['warnings'].append(f'⚠️ [MDL-058] Table "{tname}" has {len(table_measures)} measures — considered very complex')
                        _ai_debug(r, 'MDL-058', 'warning', bim_path, f'table "{tname}".measures',
                            str(len(table_measures)), '< 100 measures per table',
                            f'Consider splitting measures into multiple display folders or a dedicated measures table.')

                    for m in table_measures:
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)

                        # MDL-055: Division without DIVIDE()
                        if '/' in dax and 'DIVIDE(' not in dax.upper():
                            # Only flag if it looks like actual division (not in comments or strings)
                            div_matches = _re.findall(r'(?<!\w)/(?!\*)', dax)
                            if div_matches:
                                r['fixable'].append(('MDL-055', 'fix_use_divide', str(bim_path), tname, mname))
                                r['warnings'].append(f'⚠️ [MDL-055] Measure "{mname}" in "{tname}" uses "/" instead of DIVIDE() — risk of division by zero error (auto-fixable)')

                        # MDL-060: IFERROR is a performance anti-pattern
                        if 'IFERROR(' in dax.upper():
                            r['warnings'].append(f'⚠️ [MDL-060] Measure "{mname}" in "{tname}" uses IFERROR() — performance anti-pattern, consider DIVIDE() or IF(ISBLANK())')
                            _ai_debug(r, 'MDL-060', 'warning', bim_path, f'table "{tname}".measures["{mname}"]',
                                'uses IFERROR()', 'DIVIDE() or IF(ISBLANK(...))',
                                f'Replace IFERROR with DIVIDE() for division or IF(ISBLANK(...)) for null checks. IFERROR scans entire expression twice.')

                        # MDL-061: COUNTROWS with filter (should be CALCULATE + COUNTROWS)
                        if _re.search(r'COUNTROWS\s*\(\s*FILTER\s*\(', dax, _re.IGNORECASE):
                            r['warnings'].append(f'⚠️ [MDL-061] Measure "{mname}" in "{tname}" uses COUNTROWS(FILTER(...)) — use CALCULATE(COUNTROWS(...), ...) instead for better performance')
                            _ai_debug(r, 'MDL-061', 'warning', bim_path, f'table "{tname}".measures["{mname}"]',
                                'COUNTROWS(FILTER(...))', 'CALCULATE(COUNTROWS(Table), FilterCondition)',
                                f'Replace COUNTROWS(FILTER(Table, Condition)) with CALCULATE(COUNTROWS(Table), Condition) for better performance.')

                    # MDL-059: Column name with special characters
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if cname and _re.search(r'[^\w\s\-\.]', cname):
                            r['warnings'].append(f'⚠️ [MDL-059] Column "{cname}" in "{tname}" contains special characters — requires quoting in DAX')
                            _ai_debug(r, 'MDL-059', 'warning', bim_path, f'table "{tname}".columns["{cname}"]',
                                cname, 'alphanumeric + spaces only',
                                f'Rename column to remove special characters, or always use \'Table Name\'[Column Name] syntax in DAX.')

                    # MDL-062: Calculated column that could be a measure
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            # If calc column is not used in sortByColumn or relationships, suggest measure
                            is_sort_ref = any(col.get('sortByColumn') == cname for col in t.get('columns', []))
                            is_rel_ref = any(
                                rel.get('fromColumn') == cname or rel.get('toColumn') == cname
                                for rel in model_obj.get('relationships', [])
                                if rel.get('fromTable') == tname or rel.get('toTable') == tname
                            )
                            if not is_sort_ref and not is_rel_ref:
                                r['info'].append(f'ℹ️ [MDL-062] Calculated column "{cname}" in "{tname}" could potentially be a measure (not used in sort/relationships)')

                    # MDL-056: Numeric attribute column should have summarizeBy: "none"
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        ctype = c.get('dataType', '')
                        summarize = c.get('summarizeBy')
                        # Numeric columns whose name suggests they're attributes (ID, key, code, number, year, month, etc.)
                        attr_keywords = ['id', 'key', 'code', 'number', 'num', 'year', 'month', 'day', 'quarter', 'week', 'zip', 'postal']
                        if ctype in ('int64', 'double', 'decimal') and any(k in cname.lower() for k in attr_keywords):
                            if summarize != 'none' and summarize is not None:
                                r['fixable'].append(('MDL-056', 'fix_summarize_none', str(bim_path), tname, cname))
                                r['warnings'].append(f'⚠️ [MDL-056] Column "{cname}" in "{tname}" looks like an attribute but has summarization enabled — SUM of IDs is meaningless (auto-fixable)')

                # MDL-057: Duplicate measure definitions
                all_measure_defs = {}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        dax_normalized = ' '.join(dax.split()).strip()
                        if dax_normalized and dax_normalized in all_measure_defs:
                            prev = all_measure_defs[dax_normalized]
                            r['warnings'].append(f'⚠️ [MDL-057] Measure "{mname}" in "{tname}" has same DAX as "{prev}" — duplicate definition')
                            _ai_debug(r, 'MDL-057', 'warning', bim_path, f'table "{tname}".measures["{mname}"]',
                                dax_normalized[:100], f'unique DAX (duplicate of {prev})',
                                f'This measure has identical DAX to "{prev}". Consider removing the duplicate or using CALCULATE with different filters.')
                        else:
                            all_measure_defs[dax_normalized] = f'{tname}.{mname}'

                # ═══ NEW: Model Quality (MDL-063 → MDL-067) ═══

                # MDL-063: Orphan table (no relationships)
                rel_tables = set()
                for rel in model_obj.get('relationships', []):
                    rel_tables.add(rel.get('fromTable', ''))
                    rel_tables.add(rel.get('toTable', ''))
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    # Skip tables with measures only (measure tables) and Date tables
                    has_partitions = bool(t.get('partitions', []))
                    has_columns = bool(t.get('columns', []))
                    if tname not in rel_tables and has_partitions and has_columns:
                        r['warnings'].append(f'⚠️ [MDL-063] Table "{tname}" has no relationships — orphan/isolated table, visuals may not filter correctly')
                        _ai_debug(r, 'MDL-063', 'warning', bim_path, f'table "{tname}"',
                            'no relationships', 'at least 1 relationship',
                            f'Table "{tname}" is isolated. Add a relationship to connect it to the model, or remove it if unused. '
                            f'Available tables: {list(model_tables.keys())}')

                # MDL-065: Circular dependency detection (simple check: A→B and B→A)
                rel_graph = {}
                for rel in model_obj.get('relationships', []):
                    ft = rel.get('fromTable', '')
                    tt = rel.get('toTable', '')
                    if ft and tt:
                        rel_graph.setdefault(ft, set()).add(tt)
                for src, dests in rel_graph.items():
                    for dest in dests:
                        if dest in rel_graph and src in rel_graph.get(dest, set()):
                            r['errors'].append(f'❌ [MDL-065] Circular relationship detected: "{src}" ↔ "{dest}" — may cause ambiguous filter paths')
                            _ai_debug(r, 'MDL-065', 'error', bim_path, f'relationships',
                                f'{src} ↔ {dest}', 'no circular dependencies',
                                f'Tables "{src}" and "{dest}" have bidirectional relationships. Set one as inactive or use USERELATIONSHIP().')

                # MDL-066: Date table without isMarkAsDateTable
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    col_names = [c.get('name', '').lower() for c in t.get('columns', [])]
                    has_date_cols = any(k in cn for cn in col_names for k in ['date', 'datekey', 'calendar'])
                    is_date_table = tname.lower() in ('date', 'calendar', 'dates', 'dim_date', 'dimdate')
                    if (has_date_cols or is_date_table) and not any(
                        a.get('name') == 'MarkAsDateTable' for a in t.get('annotations', [])
                    ):
                        r['info'].append(f'ℹ️ [MDL-066] Table "{tname}" looks like a Date table but is not marked as Date Table')
                        _ai_debug(r, 'MDL-066', 'info', bim_path, f'table "{tname}".annotations',
                            'no MarkAsDateTable', 'annotation marking it as Date table',
                            f'Mark "{tname}" as Date table to enable time intelligence functions like SAMEPERIODLASTYEAR, YTD, etc.')

                # MDL-067: Table name starts with underscore
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if tname.startswith('_') and not t.get('isHidden'):
                        r['info'].append(f'ℹ️ [MDL-067] Table "{tname}" starts with underscore but is not hidden — convention mismatch')

                # ═══ NEW: model.bim Validation (MDL-068 → MDL-082) ═══

                # MDL-068: Measure missing formatString
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        fmt = m.get('formatString', '')
                        dax_raw = m.get('expression', '')
                        dax = ''.join(dax_raw) if isinstance(dax_raw, list) else str(dax_raw)
                        # Only flag if measure likely returns a number (has SUM/AVG/COUNT/etc)
                        agg_funcs = ['SUM(', 'AVERAGE(', 'COUNT(', 'MIN(', 'MAX(', 'CALCULATE(', 'DIVIDE(']
                        if not fmt and any(fn in dax.upper() for fn in agg_funcs):
                            r['fixable'].append(('MDL-068', 'fix_measure_format', str(bim_path), tname, mname))
                            r['warnings'].append(f'⚠️ [MDL-068] Measure "{mname}" in "{tname}" has no formatString — numbers display as raw values (auto-fixable)')

                # MDL-069: FK column in relationship but not hidden
                for rel in model_obj.get('relationships', []):
                    from_t = rel.get('fromTable', '')
                    from_c = rel.get('fromColumn', '')
                    if from_t and from_c:
                        for t in model_obj.get('tables', []):
                            if t.get('name') == from_t:
                                for c in t.get('columns', []):
                                    if c.get('name') == from_c and not c.get('isHidden'):
                                        r['fixable'].append(('MDL-069', 'fix_hide_fk', str(bim_path), from_t, from_c))
                                        r['warnings'].append(f'⚠️ [MDL-069] Column "{from_c}" in "{from_t}" is FK in relationship but not hidden — users see redundant field (auto-fixable)')

                # MDL-070: Bi-directional crossFilter in relationship
                for rel in model_obj.get('relationships', []):
                    cf = rel.get('crossFilteringBehavior', 'oneDirection')
                    if cf == 'bothDirections' or cf == 'bidirectional':
                        ft = rel.get('fromTable', '?')
                        tt = rel.get('toTable', '?')
                        r['warnings'].append(f'⚠️ [MDL-070] Relationship {ft}→{tt} uses bi-directional cross-filtering — may cause performance issues and ambiguity')
                        _ai_debug(r, 'MDL-070', 'warning', bim_path, f'relationship {ft}→{tt}',
                            cf, 'oneDirection (single)',
                            f'Bi-directional filtering between "{ft}" and "{tt}" can cause slower queries and ambiguous filter paths. '
                            f'Use single-direction unless specifically needed for many-to-many patterns.')

                # MDL-071: Many-to-many relationship
                for rel in model_obj.get('relationships', []):
                    card = rel.get('fromCardinality', '')
                    to_card = rel.get('toCardinality', '')
                    if card == 'many' and to_card == 'many':
                        ft = rel.get('fromTable', '?')
                        tt = rel.get('toTable', '?')
                        r['warnings'].append(f'⚠️ [MDL-071] Many-to-many relationship between "{ft}" and "{tt}" — increased resource usage, verify necessity')
                        _ai_debug(r, 'MDL-071', 'warning', bim_path, f'relationship {ft}→{tt}',
                            'many-to-many', 'one-to-many preferred',
                            f'Many-to-many relationship between "{ft}" and "{tt}". Consider using a bridge table or restructuring to one-to-many.')

                # MDL-072: Hierarchy with missing/invalid column references
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    col_names = {c.get('name', '') for c in t.get('columns', [])}
                    for h in t.get('hierarchies', []):
                        hname = h.get('name', '?')
                        for lvl in h.get('levels', []):
                            lvl_col = lvl.get('column', '')
                            if lvl_col and lvl_col not in col_names:
                                r['errors'].append(f'❌ [MDL-072] Hierarchy "{hname}" in "{tname}" references non-existent column "{lvl_col}"')
                                _ai_debug(r, 'MDL-072', 'error', bim_path, f'table "{tname}".hierarchies["{hname}"]',
                                    lvl_col, f'valid column from: {sorted(col_names)}',
                                    f'Hierarchy level references column "{lvl_col}" which does not exist in table "{tname}". '
                                    f'Fix the column name or remove the hierarchy level.')

                # MDL-073: Geographic column without dataCategory
                geo_keywords = {'city', 'state', 'country', 'region', 'latitude', 'longitude', 'lat', 'lng', 'lon',
                               'zip', 'zipcode', 'postal', 'address', 'province', 'county', 'continent'}
                geo_categories = {'City', 'State', 'StateOrProvince', 'Country', 'CountryRegion', 'Latitude', 'Longitude',
                                 'Place', 'Address', 'PostalCode', 'Continent', 'County'}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        dc = c.get('dataCategory', '')
                        if cname.lower().replace('_', '') in geo_keywords and not dc:
                            r['fixable'].append(('MDL-073', 'fix_data_category', str(bim_path), tname, cname))
                            r['info'].append(f'ℹ️ [MDL-073] Column "{cname}" in "{tname}" looks geographic but has no dataCategory set — map visuals may not work (auto-fixable)')

                # MDL-074: Calculated column uses RELATED() (performance anti-pattern)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            expr = c.get('expression', '')
                            dax = ''.join(expr) if isinstance(expr, list) else str(expr)
                            if 'RELATED(' in dax.upper():
                                r['warnings'].append(f'⚠️ [MDL-074] Calculated column "{cname}" in "{tname}" uses RELATED() — increases model size, consider using measure instead')
                                _ai_debug(r, 'MDL-074', 'warning', bim_path, f'table "{tname}".columns["{cname}"]',
                                    'RELATED() in calculated column', 'measure or direct column',
                                    f'RELATED() in calculated columns consumes storage for every row. Convert to a measure using CALCULATE() or add the column at source level.')

                # MDL-075: Measure not in displayFolder
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    measures = t.get('measures', [])
                    if len(measures) > 5:  # Only flag if table has many measures
                        for m in measures:
                            mname = m.get('name', '')
                            df = m.get('displayFolder', '')
                            if not df:
                                r['info'].append(f'ℹ️ [MDL-075] Measure "{mname}" in "{tname}" has no displayFolder — hard to find among {len(measures)} measures')

                # MDL-076: Measure or column with empty name or expression
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if not mname:
                            r['errors'].append(f'❌ [MDL-076] Table "{tname}" has a measure with empty name — will cause PBI Desktop error')
                            _ai_debug(r, 'MDL-076', 'error', bim_path, f'table "{tname}".measures',
                                'empty name', 'non-empty measure name',
                                f'Every measure must have a name. Add a descriptive name to the measure in table "{tname}".')
                        if not dax.strip():
                            r['errors'].append(f'❌ [MDL-076] Measure "{mname}" in "{tname}" has empty DAX expression')
                            _ai_debug(r, 'MDL-076', 'error', bim_path, f'table "{tname}".measures["{mname}"]',
                                'empty expression', 'valid DAX expression',
                                f'Measure "{mname}" in "{tname}" has no expression. Add a DAX formula like: SUM(Table[Column]).')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if not cname:
                            r['errors'].append(f'❌ [MDL-076] Table "{tname}" has a column with empty name')

                # MDL-077: Partition source is empty or missing
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for p in t.get('partitions', []):
                        pname = p.get('name', '?')
                        src = p.get('source', {})
                        if not src:
                            r['errors'].append(f'❌ [MDL-077] Partition "{pname}" in table "{tname}" has no source — table cannot load data')
                            _ai_debug(r, 'MDL-077', 'error', bim_path, f'table "{tname}".partitions["{pname}"]',
                                'no source', 'valid M expression or calculated source',
                                f'Partition "{pname}" in "{tname}" is missing its source definition. Add M expression or calculated type.')
                        elif src.get('type') == 'm' or src.get('type') == 'powerQuery':
                            expr = src.get('expression', '')
                            m_text = ''.join(expr) if isinstance(expr, list) else str(expr)
                            if not m_text.strip():
                                r['errors'].append(f'❌ [MDL-077] Partition "{pname}" in table "{tname}" has empty M expression — table cannot load data')

                # MDL-078: Table description is empty
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    desc = t.get('description', '')
                    has_measures = bool(t.get('measures', []))
                    has_partitions = bool(t.get('partitions', []))
                    if not desc and has_measures and has_partitions:
                        r['info'].append(f'ℹ️ [MDL-078] Table "{tname}" has no description — add documentation for team collaboration')

                # MDL-079: Model has no culture property
                culture = model_obj.get('culture', '')
                if not culture:
                    r['fixable'].append(('MDL-079', 'fix_model_culture', str(bim_path)))
                    r['warnings'].append(f'⚠️ [MDL-079] Model has no "culture" property — date/number formatting may be inconsistent (auto-fixable)')

                # MDL-080: Inactive relationship without USERELATIONSHIP reference in any measure
                inactive_rels = []
                for rel in model_obj.get('relationships', []):
                    if not rel.get('isActive', True) is False:
                        continue
                    inactive_rels.append((rel.get('fromTable', ''), rel.get('fromColumn', ''),
                                         rel.get('toTable', ''), rel.get('toColumn', '')))
                if inactive_rels:
                    all_dax = ''
                    for t in model_obj.get('tables', []):
                        for m in t.get('measures', []):
                            mexpr = m.get('expression', '')
                            all_dax += (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                    for ft, fc, tt, tc in inactive_rels:
                        # Check if USERELATIONSHIP references this pair
                        ref1 = f"USERELATIONSHIP({ft}[{fc}]".upper()
                        ref2 = f"USERELATIONSHIP({tt}[{tc}]".upper()
                        ref3 = f"'{ft}'[{fc}]".upper()
                        ref4 = f"'{tt}'[{tc}]".upper()
                        if ref1 not in all_dax and ref2 not in all_dax and ref3 not in all_dax and ref4 not in all_dax:
                            r['warnings'].append(f'⚠️ [MDL-080] Inactive relationship {ft}[{fc}]→{tt}[{tc}] is never referenced by USERELATIONSHIP — may be unnecessary')
                            _ai_debug(r, 'MDL-080', 'warning', bim_path, f'relationships (inactive)',
                                f'{ft}[{fc}]→{tt}[{tc}]', 'active or used with USERELATIONSHIP',
                                f'This inactive relationship is never activated. Either make it active, use USERELATIONSHIP() in a measure, or remove it.')

                # MDL-081: Column isHidden but used in hierarchy
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    hidden_cols = {c.get('name', '') for c in t.get('columns', []) if c.get('isHidden')}
                    for h in t.get('hierarchies', []):
                        hname = h.get('name', '?')
                        for lvl in h.get('levels', []):
                            lvl_col = lvl.get('column', '')
                            if lvl_col in hidden_cols:
                                r['errors'].append(f'❌ [MDL-081] Hidden column "{lvl_col}" in "{tname}" is used in hierarchy "{hname}" — users cannot see hierarchy level')
                                _ai_debug(r, 'MDL-081', 'error', bim_path, f'table "{tname}".columns["{lvl_col}"]',
                                    'isHidden=true + in hierarchy', 'isHidden=false or remove from hierarchy',
                                    f'Column "{lvl_col}" is hidden but used in hierarchy "{hname}". Either unhide the column or remove it from the hierarchy.')

                # MDL-082: Duplicate column names within same table
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    col_names_seen = set()
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if cname in col_names_seen:
                            r['errors'].append(f'❌ [MDL-082] Duplicate column name "{cname}" in table "{tname}" — will cause PBI Desktop error')
                            _ai_debug(r, 'MDL-082', 'error', bim_path, f'table "{tname}".columns',
                                f'duplicate: "{cname}"', 'unique column names',
                                f'Table "{tname}" has two columns named "{cname}". Rename one to make all column names unique.')
                        col_names_seen.add(cname)

                # ═══ NEW: BPA-Based Rules (MDL-083 → MDL-097) ═══

                # MDL-083: Invalid sortByColumn reference
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    col_names = {c.get('name', '') for c in t.get('columns', [])}
                    for c in t.get('columns', []):
                        sbc = c.get('sortByColumn', '')
                        cname = c.get('name', '')
                        if sbc and sbc not in col_names:
                            r['errors'].append(f'❌ [MDL-083] Column "{cname}" in "{tname}" has sortByColumn="{sbc}" but that column does not exist')
                            _ai_debug(r, 'MDL-083', 'error', bim_path, f'table "{tname}".columns["{cname}"].sortByColumn',
                                sbc, f'valid column from: {sorted(col_names)}',
                                f'Column "{cname}" references non-existent sortByColumn "{sbc}". Fix the column name or remove sortByColumn.')
                        if sbc and sbc == cname:
                            r['errors'].append(f'❌ [MDL-083] Column "{cname}" in "{tname}" has sortByColumn referencing itself')

                # MDL-084: Floating point (Double) data type — precision issues
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if c.get('dataType') == 'double' and c.get('type', 'data') != 'calculated':
                            r['fixable'].append(('MDL-084', 'fix_float_to_decimal', str(bim_path), tname, cname))
                            r['warnings'].append(f'⚠️ [MDL-084] Column "{cname}" in "{tname}" uses Double (float) — may cause precision errors, use Decimal instead (auto-fixable)')

                # MDL-085: Hidden column not used anywhere (unused — wasted space)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        if not c.get('isHidden'):
                            continue
                        cname = c.get('name', '')
                        # Check if used in: sortByColumn, hierarchy, relationship
                        used_in_sort = any(col.get('sortByColumn') == cname for col in t.get('columns', []))
                        used_in_hier = any(
                            any(lvl.get('column') == cname for lvl in h.get('levels', []))
                            for h in t.get('hierarchies', [])
                        )
                        used_in_rel = any(
                            (rel.get('fromTable') == tname and rel.get('fromColumn') == cname) or
                            (rel.get('toTable') == tname and rel.get('toColumn') == cname)
                            for rel in model_obj.get('relationships', [])
                        )
                        # Check if referenced in any DAX measure
                        dax_ref = f"[{cname}]"
                        used_in_dax = any(
                            dax_ref in (''.join(m.get('expression', '')) if isinstance(m.get('expression', ''), list) else str(m.get('expression', '')))
                            for t2 in model_obj.get('tables', [])
                            for m in t2.get('measures', [])
                        )
                        if not used_in_sort and not used_in_hier and not used_in_rel and not used_in_dax:
                            r['info'].append(f'ℹ️ [MDL-085] Hidden column "{cname}" in "{tname}" appears unused — consider removing to save space')

                # MDL-086: Auto date/time tables detected (__PBI_LocalDateTable)
                auto_date_tables = [t.get('name', '') for t in model_obj.get('tables', [])
                                   if any(a.get('name', '') == '__PBI_LocalDateTable' for a in t.get('annotations', []))]
                if auto_date_tables:
                    r['warnings'].append(f'⚠️ [MDL-086] Model has {len(auto_date_tables)} auto date/time tables — creates hidden tables for every date column, increases model size')
                    _ai_debug(r, 'MDL-086', 'warning', bim_path, 'model annotations',
                        f'{len(auto_date_tables)} auto date tables', 'custom Date table instead',
                        f'Disable auto date/time in PBI Desktop: File > Options > Current File > Data Load > uncheck "Auto date/time". '
                        f'Create a single shared Calendar/Date table instead.')

                # MDL-087: Relationship column names should match (naming convention)
                for rel in model_obj.get('relationships', []):
                    fc = rel.get('fromColumn', '')
                    tc = rel.get('toColumn', '')
                    ft = rel.get('fromTable', '?')
                    tt = rel.get('toTable', '?')
                    # Check if column names match (for single relationships) or end with toColumn name
                    same_pair_count = sum(1 for r2 in model_obj.get('relationships', [])
                                        if r2.get('fromTable') == ft and r2.get('toTable') == tt)
                    if same_pair_count == 1 and fc != tc:
                        r['info'].append(f'ℹ️ [MDL-087] Relationship {ft}[{fc}]→{tt}[{tc}]: column names differ — convention is to use same name')
                    elif same_pair_count > 1 and not fc.endswith(tc):
                        r['info'].append(f'ℹ️ [MDL-087] Relationship {ft}[{fc}]→{tt}[{tc}]: FK column name should end with "{tc}" (naming convention)')

                # MDL-088: Visible column/table uses CamelCase (naming convention)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if not t.get('isHidden') and _re.match(r'^[a-z]', tname):
                        r['info'].append(f'ℹ️ [MDL-088] Table "{tname}" name starts with lowercase — convention is uppercase first letter')

                # MDL-089: Single-attribute dimension table
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    visible_cols = [c for c in t.get('columns', []) if not c.get('isHidden')]
                    non_rel_visible = [c for c in visible_cols
                                      if not any(r2.get('fromColumn') == c.get('name') or r2.get('toColumn') == c.get('name')
                                                for r2 in model_obj.get('relationships', [])
                                                if r2.get('fromTable') == tname or r2.get('toTable') == tname)]
                    rel_count = sum(1 for r2 in model_obj.get('relationships', []) if r2.get('toTable') == tname)
                    if len(non_rel_visible) <= 1 and rel_count == 1 and not t.get('measures'):
                        r['info'].append(f'ℹ️ [MDL-089] Table "{tname}" is a single-attribute dimension — consider denormalizing into fact table')

                # MDL-090: Table with >10 visible columns/hierarchies without display folders
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    visible_no_df = sum(1 for c in t.get('columns', [])
                                       if not c.get('isHidden') and not c.get('displayFolder'))
                    visible_no_df += sum(1 for h in t.get('hierarchies', [])
                                        if not h.get('isHidden') and not h.get('displayFolder'))
                    if visible_no_df > 10:
                        r['info'].append(f'ℹ️ [MDL-090] Table "{tname}" has {visible_no_df} visible columns/hierarchies without display folders — consider organizing')

                # MDL-091: Data type mismatch in relationship columns
                for rel in model_obj.get('relationships', []):
                    ft = rel.get('fromTable', '')
                    fc = rel.get('fromColumn', '')
                    tt = rel.get('toTable', '')
                    tc = rel.get('toColumn', '')
                    from_type = None
                    to_type = None
                    for t in model_obj.get('tables', []):
                        if t.get('name') == ft:
                            for c in t.get('columns', []):
                                if c.get('name') == fc:
                                    from_type = c.get('dataType')
                        if t.get('name') == tt:
                            for c in t.get('columns', []):
                                if c.get('name') == tc:
                                    to_type = c.get('dataType')
                    if from_type and to_type and from_type != to_type:
                        r['errors'].append(f'❌ [MDL-091] Relationship {ft}[{fc}]→{tt}[{tc}]: data type mismatch ({from_type} vs {to_type})')
                        _ai_debug(r, 'MDL-091', 'error', bim_path, f'relationship {ft}[{fc}]→{tt}[{tc}]',
                            f'{from_type} vs {to_type}', 'same data type on both columns',
                            f'Relationship columns must have matching data types. "{fc}" is {from_type} but "{tc}" is {to_type}. '
                            f'Change one column to match the other.')

                # MDL-092: Missing lineageTag on columns
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    missing_lt = sum(1 for c in t.get('columns', []) if not c.get('lineageTag'))
                    total_cols = len(t.get('columns', []))
                    if total_cols > 0 and missing_lt == total_cols:
                        r['fixable'].append(('MDL-092', 'fix_lineage_tags', str(bim_path), tname))
                        r['info'].append(f'ℹ️ [MDL-092] Table "{tname}" has no lineageTag on any column — needed for TMDL format persistence (auto-fixable)')

                # MDL-093: Duplicate measure names across tables
                all_measure_names = {}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        if mname in all_measure_names:
                            prev_table = all_measure_names[mname]
                            r['errors'].append(f'❌ [MDL-093] Duplicate measure name "{mname}" across tables "{prev_table}" and "{tname}" — will cause ambiguous references')
                            _ai_debug(r, 'MDL-093', 'error', bim_path, f'measures',
                                f'"{mname}" in {prev_table} and {tname}', 'unique measure names across model',
                                f'Measure names must be unique across the entire model. Rename one of the "{mname}" measures.')
                        else:
                            all_measure_names[mname] = tname

                # MDL-094: sourceColumn mismatch (column references non-existent source)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        sc = c.get('sourceColumn', '')
                        cname = c.get('name', '')
                        ctype = c.get('type', 'data')
                        # Only check data columns (not calculated, not rowNumber)
                        if ctype == 'data' and sc and sc != cname:
                            # sourceColumn should match the partition query column — just flag mismatches
                            pass  # Complex to validate without running the M expression

                # MDL-095: Hidden measure (BPA: hidden measures not referenced should be removed)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        if not m.get('isHidden'):
                            continue
                        mname = m.get('name', '')
                        # Check if any other measure references this hidden measure
                        ref = f"[{mname}]"
                        is_referenced = any(
                            ref in (''.join(m2.get('expression', '')) if isinstance(m2.get('expression', ''), list) else str(m2.get('expression', '')))
                            for t2 in model_obj.get('tables', [])
                            for m2 in t2.get('measures', [])
                            if m2.get('name', '') != mname
                        )
                        if not is_referenced:
                            r['info'].append(f'ℹ️ [MDL-095] Hidden measure "{mname}" in "{tname}" is not referenced by any other measure — consider removing')

                # MDL-096: Table with no columns (structural error)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    cols = t.get('columns', [])
                    if not cols and t.get('partitions'):
                        r['errors'].append(f'❌ [MDL-096] Table "{tname}" has partitions but no columns defined — PBI Desktop will error')
                        _ai_debug(r, 'MDL-096', 'error', bim_path, f'table "{tname}"',
                            '0 columns', 'at least 1 column',
                            f'Table "{tname}" has data partitions but no column definitions. Add column metadata or remove the table.')

                # MDL-097: Visible numeric column without formatString (from BPA)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        dt = c.get('dataType', '')
                        fmt = c.get('formatString', '')
                        if not c.get('isHidden') and not fmt and dt in ('int64', 'double', 'decimal', 'dateTime'):
                            r['fixable'].append(('MDL-097', 'fix_col_format', str(bim_path), tname, cname, dt))
                            r['info'].append(f'ℹ️ [MDL-097] Visible {dt} column "{cname}" in "{tname}" has no formatString — display may be inconsistent (auto-fixable)')

                # ═══ FINAL: Exhaustive Validation (MDL-098 → MDL-112) ═══

                # MDL-098: Numeric column SummarizeBy not set to None (BPA: META_SUMMARIZE_NONE)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        dt = c.get('dataType', '')
                        sb = c.get('summarizeBy', 'none')
                        if not c.get('isHidden') and dt in ('int64', 'double', 'decimal') and sb != 'none':
                            r['fixable'].append(('MDL-098', 'fix_summarize_none', str(bim_path), tname, cname))
                            r['warnings'].append(f'⚠️ [MDL-098] Visible numeric column "{cname}" in "{tname}" has summarizeBy="{sb}" — should be "none" to avoid unintentional aggregation (auto-fixable)')

                # MDL-099: Non-attribute columns with isAvailableInMdx=true (performance waste)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if c.get('isHidden') and c.get('isAvailableInMdx', True) is True:
                            # Only flag if column is used only in relationship
                            used_in_rel = any(
                                (rel.get('fromTable') == tname and rel.get('fromColumn') == cname) or
                                (rel.get('toTable') == tname and rel.get('toColumn') == cname)
                                for rel in model_obj.get('relationships', [])
                            )
                            if used_in_rel:
                                r['fixable'].append(('MDL-099', 'fix_mdx_false', str(bim_path), tname, cname))
                                r['info'].append(f'ℹ️ [MDL-099] Hidden FK column "{cname}" in "{tname}" has isAvailableInMdx=true — set to false for performance (auto-fixable)')

                # MDL-100: RLS role with no filter expression (empty role = no security)
                for role in model_obj.get('roles', []):
                    rname = role.get('name', '?')
                    perms = role.get('tablePermissions', [])
                    if not perms:
                        r['warnings'].append(f'⚠️ [MDL-100] Role "{rname}" has no tablePermissions — grants full access to all data')
                        _ai_debug(r, 'MDL-100', 'warning', bim_path, f'roles["{rname}"]',
                            'no tablePermissions', 'at least one filterExpression',
                            f'Role "{rname}" has no RLS filters. Add tablePermissions with DAX filter expressions.')
                    else:
                        for tp in perms:
                            fe = tp.get('filterExpression', '')
                            tbl = tp.get('name', '?')
                            if not fe:
                                r['warnings'].append(f'⚠️ [MDL-100] Role "{rname}" has empty filterExpression on table "{tbl}"')

                # MDL-101: Calculation group with no calculation items
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    cg = t.get('calculationGroup', None)
                    if cg is not None:
                        items = cg.get('calculationItems', [])
                        if not items:
                            r['warnings'].append(f'⚠️ [MDL-101] Calculation group "{tname}" has no calculation items — useless without items')
                            _ai_debug(r, 'MDL-101', 'warning', bim_path, f'table "{tname}".calculationGroup',
                                '0 items', 'at least 1 calculationItem',
                                f'Add calculation items (e.g., time intelligence patterns) or remove the calculation group.')

                # MDL-102: Perspectives defined but table not included
                perspectives = model_obj.get('perspectives', [])
                if perspectives:
                    for t in model_obj.get('tables', []):
                        tname = t.get('name', '?')
                        if not t.get('isHidden'):
                            in_any_perspective = False
                            for p in perspectives:
                                for pt in p.get('tables', []):
                                    if pt.get('name') == tname:
                                        in_any_perspective = True
                                        break
                                if in_any_perspective:
                                    break
                            if not in_any_perspective:
                                r['info'].append(f'ℹ️ [MDL-102] Visible table "{tname}" is not included in any perspective')

                # MDL-103: Compatibility level too low
                compat = model_obj.get('compatibilityLevel', 0)
                if compat and compat < 1500:
                    r['warnings'].append(f'⚠️ [MDL-103] Model compatibility level is {compat} — consider upgrading to 1550+ for latest features')
                    _ai_debug(r, 'MDL-103', 'warning', bim_path, 'model.compatibilityLevel',
                        str(compat), '1550 or higher',
                        f'Older compatibility levels miss features like calculation groups, compound models, and DirectQuery improvements.')

                # MDL-104: Missing defaultPowerBIDataSourceVersion
                ds_version = model_obj.get('defaultPowerBIDataSourceVersion', '')
                if not ds_version:
                    r['fixable'].append(('MDL-104', 'fix_ds_version', str(bim_path)))
                    r['warnings'].append(f'⚠️ [MDL-104] Model missing "defaultPowerBIDataSourceVersion" — may fail deployment to Premium (auto-fixable)')

                # MDL-105: Circular sortByColumn chain
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    sort_map = {}
                    for c in t.get('columns', []):
                        sbc = c.get('sortByColumn', '')
                        if sbc:
                            sort_map[c.get('name', '')] = sbc
                    # Detect cycles
                    for start_col in sort_map:
                        visited = set()
                        current = start_col
                        while current in sort_map and current not in visited:
                            visited.add(current)
                            current = sort_map[current]
                        if current in visited:
                            r['errors'].append(f'❌ [MDL-105] Circular sortByColumn chain in "{tname}": {" → ".join(visited)} → {current}')
                            _ai_debug(r, 'MDL-105', 'error', bim_path, f'table "{tname}" sortByColumn chain',
                                f'circular: {visited}', 'no circular references',
                                f'Remove one sortByColumn reference to break the cycle.')
                            break

                # MDL-106: Orphan table (no relationships and no measures)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    has_rel = any(
                        rel.get('fromTable') == tname or rel.get('toTable') == tname
                        for rel in model_obj.get('relationships', [])
                    )
                    has_measures = bool(t.get('measures'))
                    has_calc_group = t.get('calculationGroup') is not None
                    is_hidden = t.get('isHidden', False)
                    # Skip Date tables and hidden/calc group tables
                    if not has_rel and not has_measures and not has_calc_group and not is_hidden:
                        r['info'].append(f'ℹ️ [MDL-106] Table "{tname}" has no relationships and no measures — possible orphan table')

                # MDL-107: Object name has leading/trailing spaces
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '')
                    if tname != tname.strip():
                        r['fixable'].append(('MDL-107', 'fix_trim_name', str(bim_path), 'table', tname))
                        r['warnings'].append(f'⚠️ [MDL-107] Table name "{repr(tname)}" has leading/trailing spaces — causes lookup errors (auto-fixable)')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if cname != cname.strip():
                            r['fixable'].append(('MDL-107', 'fix_trim_name', str(bim_path), 'column', tname, cname))
                            r['warnings'].append(f'⚠️ [MDL-107] Column name "{repr(cname)}" in "{tname}" has leading/trailing spaces (auto-fixable)')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        if mname != mname.strip():
                            r['fixable'].append(('MDL-107', 'fix_trim_name', str(bim_path), 'measure', tname, mname))
                            r['warnings'].append(f'⚠️ [MDL-107] Measure name "{repr(mname)}" in "{tname}" has leading/trailing spaces (auto-fixable)')

                # MDL-108: DAX uses IFERROR/ISERROR (anti-pattern)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        if 'IFERROR(' in dax or 'ISERROR(' in dax:
                            r['warnings'].append(f'⚠️ [MDL-108] Measure "{mname}" in "{tname}" uses IFERROR/ISERROR — hides errors, use DIVIDE() or handle specific conditions instead')

                # MDL-109: Two measures with identical DAX expression
                measure_defs = {}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).strip()
                        if dax and len(dax) > 10:  # Skip trivial expressions
                            if dax in measure_defs:
                                prev = measure_defs[dax]
                                r['info'].append(f'ℹ️ [MDL-109] Measures "{prev}" and "{mname}" have identical DAX — consider consolidating')
                            else:
                                measure_defs[dax] = f'{tname}[{mname}]'

                # MDL-110: Measure is direct reference to another measure
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).strip()
                        # Check if expression is just [OtherMeasure] or 'Table'[OtherMeasure]
                        if _re.match(r"^\[.+\]$", dax) or _re.match(r"^'.+'?\[.+\]$", dax):
                            r['info'].append(f'ℹ️ [MDL-110] Measure "{mname}" in "{tname}" is a direct reference to another measure — consider using the original directly')

                # MDL-111: Shared expressions (model.expressions) with errors
                model_expressions = model_obj.get('expressions', [])
                for expr in model_expressions:
                    ename = expr.get('name', '?')
                    eexpr = expr.get('expression', '')
                    m_text = ''.join(eexpr) if isinstance(eexpr, list) else str(eexpr)
                    if not m_text.strip():
                        r['errors'].append(f'❌ [MDL-111] Shared expression "{ename}" has empty body — will cause refresh errors')
                        _ai_debug(r, 'MDL-111', 'error', bim_path, f'expressions["{ename}"]',
                            'empty expression', 'valid M/Power Query expression',
                            f'Shared expression "{ename}" has no body. Add a valid M expression.')

                # MDL-112: Column encodingHint set to value on high-cardinality text
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        eh = c.get('encodingHint', '')
                        dt = c.get('dataType', '')
                        if eh == 'value' and dt == 'string':
                            r['warnings'].append(f'⚠️ [MDL-112] Column "{cname}" in "{tname}" has encodingHint="value" on string type — use "hash" for text columns for better compression')
                            _ai_debug(r, 'MDL-112', 'warning', bim_path, f'table "{tname}".columns["{cname}"]',
                                'encodingHint=value on string', 'encodingHint=hash for strings',
                                f'Value encoding on string columns creates large dictionaries. Hash encoding is typically better for text.')

                # ═══ ULTRA-DEEP: Edge Cases (MDL-113 → MDL-127) ═══

                # MDL-113: OLS (Object-Level Security) on calculated columns (not supported)
                for role in model_obj.get('roles', []):
                    rname = role.get('name', '?')
                    for tp in role.get('tablePermissions', []):
                        tbl_name = tp.get('name', '?')
                        col_perms = tp.get('columnPermissions', [])
                        if col_perms:
                            # Find the actual table to check if columns are calculated
                            for t in model_obj.get('tables', []):
                                if t.get('name') == tbl_name:
                                    calc_cols = {c.get('name') for c in t.get('columns', []) if c.get('type') == 'calculated'}
                                    for cp in col_perms:
                                        cn = cp.get('name', '')
                                        if cn in calc_cols:
                                            r['errors'].append(f'❌ [MDL-113] OLS on calculated column "{cn}" in role "{rname}" (table "{tbl_name}") — not supported by Power BI')
                                            _ai_debug(r, 'MDL-113', 'error', bim_path, f'roles["{rname}"].tablePermissions["{tbl_name}"]',
                                                f'OLS on calculated column "{cn}"', 'OLS only on data columns',
                                                f'Remove OLS from calculated column "{cn}". OLS cannot be applied to calculated columns or tables.')

                # MDL-114: KPI measure with no targetExpression
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        kpi = m.get('kpi', None)
                        if kpi is not None:
                            mname = m.get('name', '')
                            if not kpi.get('targetExpression', ''):
                                r['warnings'].append(f'⚠️ [MDL-114] KPI on measure "{mname}" in "{tname}" has no targetExpression')
                            if not kpi.get('statusExpression', ''):
                                r['warnings'].append(f'⚠️ [MDL-114] KPI on measure "{mname}" in "{tname}" has no statusExpression')

                # MDL-115: Multiple active relationships between same table pair
                active_pairs = {}
                for rel in model_obj.get('relationships', []):
                    if not rel.get('isActive', True) is False:
                        pair = tuple(sorted([rel.get('fromTable', ''), rel.get('toTable', '')]))
                        if pair in active_pairs:
                            r['errors'].append(f'❌ [MDL-115] Multiple active relationships between "{pair[0]}" and "{pair[1]}" — causes ambiguous filter paths')
                            _ai_debug(r, 'MDL-115', 'error', bim_path, f'relationships',
                                f'2+ active rels between {pair}', 'only 1 active relationship per table pair',
                                f'Deactivate one relationship and use USERELATIONSHIP() in specific measures.')
                        else:
                            active_pairs[pair] = True

                # MDL-116: Mixed storage modes (import + directquery) without explicit thought
                storage_modes = set()
                for t in model_obj.get('tables', []):
                    for p in t.get('partitions', []):
                        mode = p.get('mode', 'import')
                        storage_modes.add(mode)
                if len(storage_modes) > 1 and 'directQuery' in storage_modes and 'import' in storage_modes:
                    r['info'].append(f'ℹ️ [MDL-116] Model uses mixed storage modes (import + directQuery) — ensure this is intentional (composite model). Modes found: {storage_modes}')

                # MDL-117: Table with showAsVariationsOnly but no variation target
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if t.get('showAsVariationsOnly'):
                        # Check if any column in any table has a variation pointing to this table
                        is_target = False
                        for t2 in model_obj.get('tables', []):
                            for c in t2.get('columns', []):
                                for v in c.get('variations', []):
                                    if v.get('defaultHierarchy', {}).get('table') == tname:
                                        is_target = True
                                        break
                                if is_target:
                                    break
                            if is_target:
                                break
                        if not is_target:
                            r['errors'].append(f'❌ [MDL-117] Table "{tname}" has showAsVariationsOnly=true but is not a target of any variation — will cause errors')

                # MDL-118: DAX uses deprecated EARLIER function
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        if 'EARLIER(' in dax or 'EARLIEST(' in dax:
                            r['warnings'].append(f'⚠️ [MDL-118] Measure "{mname}" in "{tname}" uses deprecated EARLIER/EARLIEST — use VAR/RETURN instead')
                    # Also check calculated columns
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            cexpr = c.get('expression', '')
                            dax = (''.join(cexpr) if isinstance(cexpr, list) else str(cexpr)).upper()
                            if 'EARLIER(' in dax or 'EARLIEST(' in dax:
                                r['warnings'].append(f'⚠️ [MDL-118] Calculated column "{cname}" in "{tname}" uses deprecated EARLIER/EARLIEST — use VAR/RETURN')

                # MDL-119: Measure uses LOOKUPVALUE when RELATED would work
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            cexpr = c.get('expression', '')
                            dax = (''.join(cexpr) if isinstance(cexpr, list) else str(cexpr)).upper()
                            if 'LOOKUPVALUE(' in dax:
                                r['info'].append(f'ℹ️ [MDL-119] Calculated column "{cname}" in "{tname}" uses LOOKUPVALUE — consider RELATED() for 3-5x better performance if a relationship exists')

                # MDL-120: DAX uses unqualified column references
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        # Simple heuristic: SUM( col ) without Table[ prefix — check for common aggregation with bare column
                        if _re.search(r'(?:SUM|AVERAGE|MIN|MAX|COUNT|COUNTROWS)\s*\(\s*[a-zA-Z_]\w*\s*\)', dax):
                            # Only flag if it doesn't look like a table function
                            if not _re.search(r"(?:SUM|AVERAGE|MIN|MAX|COUNT)\s*\(\s*'[^']+'\[", dax) and not _re.search(r"(?:SUM|AVERAGE|MIN|MAX|COUNT)\s*\(\s*\[", dax):
                                r['info'].append(f'ℹ️ [MDL-120] Measure "{mname}" in "{tname}" may have unqualified column references — use \'Table\'[Column] for clarity')

                # MDL-121: Legacy data source (providerDataSource without structuredDataSource)
                data_sources = model_obj.get('dataSources', [])
                for ds in data_sources:
                    dsname = ds.get('name', '?')
                    ds_type = ds.get('type', '')
                    if ds_type == 'provider':
                        r['info'].append(f'ℹ️ [MDL-121] Legacy provider data source "{dsname}" detected — consider migrating to structured (Power Query M) for better Power BI compatibility')

                # MDL-122: isNullable=true on key column
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if c.get('isKey') and c.get('isNullable', True):
                            r['warnings'].append(f'⚠️ [MDL-122] Key column "{cname}" in "{tname}" has isNullable=true — keys should not contain nulls')

                # MDL-123: isDefaultLabel set on column not in row label
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    default_labels = [c for c in t.get('columns', []) if c.get('isDefaultLabel')]
                    if len(default_labels) > 1:
                        names = [c.get('name', '') for c in default_labels]
                        r['warnings'].append(f'⚠️ [MDL-123] Table "{tname}" has multiple isDefaultLabel columns: {names} — only one is allowed')

                # MDL-124: refreshPolicy without proper polling expression
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    rp = t.get('refreshPolicy', None)
                    if rp is not None:
                        if not rp.get('sourceExpression'):
                            r['warnings'].append(f'⚠️ [MDL-124] Table "{tname}" has refreshPolicy but no sourceExpression — incremental refresh will not work')
                        if not rp.get('rollingWindowGranularity'):
                            r['info'].append(f'ℹ️ [MDL-124] Table "{tname}" has refreshPolicy without rollingWindowGranularity — data retention not configured')

                # MDL-125: Ambiguous relationship paths (A→B→C and A→C causing two paths)
                adjacency = {}
                for rel in model_obj.get('relationships', []):
                    if rel.get('isActive', True) is not False:
                        fromT = rel.get('fromTable', '')
                        toT = rel.get('toTable', '')
                        adjacency.setdefault(fromT, set()).add(toT)
                        adjacency.setdefault(toT, set()).add(fromT)
                # Check for diamond patterns (simplified: flag if table connects to another via 2+ distinct paths)
                # This is computationally expensive for large models, so we do a simple 2-hop check
                for node in adjacency:
                    neighbors = adjacency.get(node, set())
                    for n1 in neighbors:
                        hop2 = adjacency.get(n1, set()) - {node}
                        overlap = hop2 & neighbors
                        if overlap:
                            for o in overlap:
                                r['info'].append(f'ℹ️ [MDL-125] Potential ambiguous filter path: "{node}" → "{o}" (direct) and "{node}" → "{n1}" → "{o}" — may cause unexpected results')
                            break  # Limit output
                    if any(adjacency.get(n1, set()) - {node} & neighbors for n1 in neighbors):
                        break

                # MDL-126: measures with detailRowsDefinition referencing invalid columns
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        drd = m.get('detailRowsDefinition', None)
                        if drd is not None:
                            drd_expr = drd.get('expression', '')
                            drd_text = ''.join(drd_expr) if isinstance(drd_expr, list) else str(drd_expr)
                            if not drd_text.strip():
                                mname = m.get('name', '')
                                r['warnings'].append(f'⚠️ [MDL-126] Measure "{mname}" in "{tname}" has empty detailRowsDefinition expression')

                # MDL-127: Model-level annotations with reserved/problematic names
                model_annotations = model_obj.get('annotations', [])
                reserved_annotations = {'PBI_QueryOrder', 'PBIDesktopVersion', 'PBI_ProTooling'}
                for ann in model_annotations:
                    aname = ann.get('name', '')
                    aval = ann.get('value', '')
                    if aname in reserved_annotations and not aval:
                        r['info'].append(f'ℹ️ [MDL-127] Model annotation "{aname}" is empty — may cause issues with Power BI Desktop')

                # ═══ MAXIMUM DEPTH: Structural & DAX Quality (MDL-128 → MDL-142) ═══

                # MDL-128: Relationship securityFilteringBehavior=BothDirections with RLS
                has_rls = bool(model_obj.get('roles', []))
                if has_rls:
                    for rel in model_obj.get('relationships', []):
                        sfb = rel.get('securityFilteringBehavior', 'oneDirection')
                        if sfb == 'bothDirections':
                            fromT = rel.get('fromTable', '?')
                            toT = rel.get('toTable', '?')
                            r['warnings'].append(f'⚠️ [MDL-128] Relationship "{fromT}" → "{toT}" has securityFilteringBehavior=bothDirections with RLS — can cause "not supported" errors with multiple roles')

                # MDL-129: Relationship references non-existent column
                table_columns = {}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '')
                    table_columns[tname] = {c.get('name', '') for c in t.get('columns', [])}
                for rel in model_obj.get('relationships', []):
                    fromT = rel.get('fromTable', '')
                    fromC = rel.get('fromColumn', '')
                    toT = rel.get('toTable', '')
                    toC = rel.get('toColumn', '')
                    if fromT in table_columns and fromC and fromC not in table_columns.get(fromT, set()):
                        r['errors'].append(f'❌ [MDL-129] Relationship references column "{fromC}" in table "{fromT}" — column does not exist')
                        _ai_debug(r, 'MDL-129', 'error', bim_path, f'relationship {fromT}→{toT}',
                            f'column "{fromC}" not in "{fromT}"', 'valid column reference',
                            f'Fix the fromColumn reference or add the missing column to table "{fromT}".')
                    if toT in table_columns and toC and toC not in table_columns.get(toT, set()):
                        r['errors'].append(f'❌ [MDL-129] Relationship references column "{toC}" in table "{toT}" — column does not exist')
                        _ai_debug(r, 'MDL-129', 'error', bim_path, f'relationship {fromT}→{toT}',
                            f'column "{toC}" not in "{toT}"', 'valid column reference',
                            f'Fix the toColumn reference or add the missing column to table "{toT}".')

                # MDL-130: Table with no partitions (structural error)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    parts = t.get('partitions', [])
                    has_calc = t.get('calculationGroup') is not None
                    # Calculated tables and calc groups may have special partitions
                    if not parts and not has_calc and not tname.startswith('__'):
                        r['errors'].append(f'❌ [MDL-130] Table "{tname}" has no partitions — table will have no data source')

                # MDL-131: dataCategory and dataType mismatch
                geo_type_map = {
                    'latitude': ('double', 'decimal'),
                    'longitude': ('double', 'decimal'),
                    'postalcode': ('string',),
                    'city': ('string',),
                    'stateorprovince': ('string',),
                    'country': ('string',),
                    'county': ('string',),
                    'continent': ('string',),
                    'place': ('string',),
                    'address': ('string',),
                    'weburl': ('string',),
                    'imageurl': ('string',),
                    'barcode': ('string',),
                }
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        dc = (c.get('dataCategory', '') or '').lower()
                        dt = c.get('dataType', '')
                        if dc and dc in geo_type_map:
                            valid_types = geo_type_map[dc]
                            if dt and dt not in valid_types:
                                r['warnings'].append(f'⚠️ [MDL-131] Column "{cname}" in "{tname}" has dataCategory="{dc}" but dataType="{dt}" — expected {valid_types}')

                # MDL-132: Model with no relationships (flat model)
                rels = model_obj.get('relationships', [])
                tables = [t for t in model_obj.get('tables', []) if not t.get('name', '').startswith('__')]
                if not rels and len(tables) > 1:
                    r['warnings'].append(f'⚠️ [MDL-132] Model has {len(tables)} tables but no relationships — flat model may produce incorrect results with cross-table calculations')

                # MDL-133: Table with too many columns (model bloat)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    col_count = len(t.get('columns', []))
                    if col_count > 100:
                        r['warnings'].append(f'⚠️ [MDL-133] Table "{tname}" has {col_count} columns — consider reducing to improve performance')
                    elif col_count > 50:
                        r['info'].append(f'ℹ️ [MDL-133] Table "{tname}" has {col_count} columns — review if all are necessary')

                # MDL-134: DAX CALCULATE with no filter argument (no-op)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        # Pattern: CALCULATE( [Measure] ) with no second argument
                        if _re.search(r'CALCULATE\s*\(\s*\[[^\]]+\]\s*\)', dax, _re.IGNORECASE):
                            r['info'].append(f'ℹ️ [MDL-134] Measure "{mname}" in "{tname}" uses CALCULATE with no filter — effectively a no-op')

                # MDL-135: DAX FILTER(ALL(Table)) anti-pattern
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if _re.search(r'FILTER\s*\(\s*ALL\s*\(', dax, _re.IGNORECASE):
                            r['info'].append(f'ℹ️ [MDL-135] Measure "{mname}" in "{tname}" uses FILTER(ALL(...)) — consider using KEEPFILTERS or moving to CALCULATE filter for better performance')

                # MDL-136: Column with dataType unknown or empty
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        dt = c.get('dataType', '')
                        if not dt:
                            r['warnings'].append(f'⚠️ [MDL-136] Column "{cname}" in "{tname}" has no dataType specified')
                        elif dt == 'unknown':
                            r['errors'].append(f'❌ [MDL-136] Column "{cname}" in "{tname}" has dataType="unknown" — Power BI cannot process this')

                # MDL-137: Relationship with reliesToReferentialIntegrity enabled
                for rel in model_obj.get('relationships', []):
                    if rel.get('reliesToReferentialIntegrity'):
                        fromT = rel.get('fromTable', '?')
                        toT = rel.get('toTable', '?')
                        r['info'].append(f'ℹ️ [MDL-137] Relationship "{fromT}" → "{toT}" uses reliesToReferentialIntegrity — assumes no orphan keys (performance opt, but risky if data is inconsistent)')

                # MDL-138: Table with excludeFromModelRefresh
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if t.get('excludeFromModelRefresh'):
                        r['info'].append(f'ℹ️ [MDL-138] Table "{tname}" is excluded from model refresh — ensure this is intentional')

                # MDL-139: Column with alternateOf referencing non-existent column/table
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        alt = c.get('alternateOf', None)
                        if alt is not None:
                            alt_table = alt.get('baseTable', '')
                            alt_col = alt.get('baseColumn', '')
                            cname = c.get('name', '')
                            if alt_table and alt_table not in table_columns:
                                r['errors'].append(f'❌ [MDL-139] Column "{cname}" in "{tname}" alternateOf references table "{alt_table}" — table does not exist')
                            elif alt_table and alt_col and alt_col not in table_columns.get(alt_table, set()):
                                r['errors'].append(f'❌ [MDL-139] Column "{cname}" in "{tname}" alternateOf references column "{alt_col}" in "{alt_table}" — column does not exist')

                # MDL-140: Calculated table with empty expression
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for p in t.get('partitions', []):
                        if p.get('mode') == 'import' and p.get('source', {}).get('type') == 'calculated':
                            calc_expr = p.get('source', {}).get('expression', '')
                            expr_text = ''.join(calc_expr) if isinstance(calc_expr, list) else str(calc_expr)
                            if not expr_text.strip():
                                r['errors'].append(f'❌ [MDL-140] Calculated table "{tname}" has empty expression — will fail to load')
                                _ai_debug(r, 'MDL-140', 'error', bim_path, f'table "{tname}" calculated partition',
                                    'empty expression', 'valid DAX expression',
                                    f'Add a DAX expression like DATATABLE() or reference to another table.')

                # MDL-141: Measure with no description (documentation gap)
                measures_without_desc = 0
                total_measures = 0
                for t in model_obj.get('tables', []):
                    for m in t.get('measures', []):
                        total_measures += 1
                        if not m.get('description', '').strip():
                            measures_without_desc += 1
                if total_measures > 5 and measures_without_desc > total_measures * 0.8:
                    r['info'].append(f'ℹ️ [MDL-141] {measures_without_desc}/{total_measures} measures have no description — add descriptions for better model documentation')

                # MDL-142: Table name clashes with DAX reserved words
                dax_reserved = {'DATE', 'TIME', 'YEAR', 'MONTH', 'DAY', 'HOUR', 'MINUTE', 'SECOND',
                    'NOW', 'TODAY', 'TRUE', 'FALSE', 'BLANK', 'ERROR', 'CURRENCY', 'FORMAT',
                    'IF', 'SWITCH', 'AND', 'OR', 'NOT', 'IN', 'VAR', 'RETURN', 'TABLE',
                    'COLUMN', 'MEASURE', 'ROW', 'VALUE', 'VALUES', 'FILTER', 'ALL', 'CALENDAR',
                    'CALCULATE', 'SUMMARIZE', 'DISTINCT', 'CONTAINS', 'RELATED', 'PATH'}
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '')
                    if tname.upper() in dax_reserved:
                        r['warnings'].append(f'⚠️ [MDL-142] Table name "{tname}" is a DAX reserved word — must use single quotes in all DAX references (\'{tname}\')')

                # ═══ BEYOND EXHAUSTIVE: Topology & Quality (MDL-143 → MDL-157) ═══

                # MDL-143: Self-referencing relationship (fromTable = toTable)
                for rel in model_obj.get('relationships', []):
                    fromT = rel.get('fromTable', '')
                    toT = rel.get('toTable', '')
                    if fromT and fromT == toT:
                        r['errors'].append(f'❌ [MDL-143] Self-referencing relationship on table "{fromT}" — not supported in Power BI Import mode')
                        _ai_debug(r, 'MDL-143', 'error', bim_path, f'relationship on "{fromT}"',
                            'fromTable = toTable', 'relationships between different tables',
                            f'Use parent-child DAX functions (PATH, PATHITEM) instead of a self-join relationship.')

                # MDL-144: Duplicate relationship (same from/to table+column pair)
                seen_rels = set()
                for rel in model_obj.get('relationships', []):
                    key = (rel.get('fromTable', ''), rel.get('fromColumn', ''),
                           rel.get('toTable', ''), rel.get('toColumn', ''))
                    if key in seen_rels:
                        r['errors'].append(f'❌ [MDL-144] Duplicate relationship: "{key[0]}[{key[1]}]" → "{key[2]}[{key[3]}]" — remove the duplicate')
                    else:
                        seen_rels.add(key)

                # MDL-145: Hierarchy with only one level (useless)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for h in t.get('hierarchies', []):
                        hname = h.get('name', '?')
                        levels = h.get('levels', [])
                        if len(levels) <= 1:
                            r['info'].append(f'ℹ️ [MDL-145] Hierarchy "{hname}" in "{tname}" has only {len(levels)} level — hierarchies should have 2+ levels')

                # MDL-146: Calculated column that could be a measure (no row context used)
                simple_agg_pattern = _re.compile(r'^(SUM|AVERAGE|MIN|MAX|COUNT|COUNTROWS|DISTINCTCOUNT|DIVIDE)\s*\(', _re.IGNORECASE)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            cexpr = c.get('expression', '')
                            dax = (''.join(cexpr) if isinstance(cexpr, list) else str(cexpr)).strip()
                            if simple_agg_pattern.match(dax):
                                r['info'].append(f'ℹ️ [MDL-146] Calculated column "{cname}" in "{tname}" uses aggregation ({dax[:30]}...) — may be better as a measure for performance')

                # MDL-147: Measure expression references calculated column (performance chain)
                calc_col_refs = set()
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '')
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            calc_col_refs.add(f"'{tname}'[{c.get('name', '')}]")
                            calc_col_refs.add(f"[{c.get('name', '')}]")
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        for ref in calc_col_refs:
                            if ref in dax:
                                r['info'].append(f'ℹ️ [MDL-147] Measure "{mname}" in "{tname}" references calculated column {ref} — consider converting to a measure for better performance')
                                break

                # MDL-148: Fact-to-fact relationship (unusual pattern)
                fact_tables = set()
                dim_tables = set()
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '')
                    has_measures = bool(t.get('measures'))
                    # Tables with measures are often fact tables
                    if has_measures:
                        fact_tables.add(tname)
                    else:
                        dim_tables.add(tname)
                for rel in model_obj.get('relationships', []):
                    fromT = rel.get('fromTable', '')
                    toT = rel.get('toTable', '')
                    if fromT in fact_tables and toT in fact_tables:
                        r['info'].append(f'ℹ️ [MDL-148] Relationship between two fact tables "{fromT}" → "{toT}" — usually fact tables relate to dimensions, not each other')

                # MDL-149: Table with too many measures (organization problem)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    m_count = len(t.get('measures', []))
                    if m_count > 50:
                        r['warnings'].append(f'⚠️ [MDL-149] Table "{tname}" has {m_count} measures — consider organizing into display folders or separate measure tables')
                    elif m_count > 25:
                        r['info'].append(f'ℹ️ [MDL-149] Table "{tname}" has {m_count} measures — consider grouping with display folders')

                # MDL-150: Model with too many tables
                all_tables = [t for t in model_obj.get('tables', []) if not t.get('name', '').startswith('__')]
                if len(all_tables) > 50:
                    r['warnings'].append(f'⚠️ [MDL-150] Model has {len(all_tables)} tables — consider simplifying for better performance')
                elif len(all_tables) > 30:
                    r['info'].append(f'ℹ️ [MDL-150] Model has {len(all_tables)} tables — review model complexity')

                # MDL-151: Column name with special characters needing escaping
                special_char_pattern = _re.compile(r'[^\w\s]', _re.UNICODE)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for c in t.get('columns', []):
                        cname = c.get('name', '')
                        if special_char_pattern.search(cname) and not cname.startswith('__'):
                            r['info'].append(f'ℹ️ [MDL-151] Column "{cname}" in "{tname}" contains special characters — ensure proper escaping in DAX references')

                # MDL-152: Hidden table with visible measures (contradiction)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    if t.get('isHidden'):
                        visible_measures = [m.get('name') for m in t.get('measures', []) if not m.get('isHidden')]
                        if visible_measures:
                            r['info'].append(f'ℹ️ [MDL-152] Hidden table "{tname}" has {len(visible_measures)} visible measures — measures will still appear in field list')

                # MDL-153: Date table without isKey on date column
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    # Heuristic: table with dataCategory or name containing "date/calendar"
                    is_date_table = False
                    for c in t.get('columns', []):
                        if c.get('isKey') and c.get('dataType') in ('dateTime', 'int64'):
                            is_date_table = True
                            break
                    # Check if table has a column used as "Date" in a relationship
                    for rel in model_obj.get('relationships', []):
                        if rel.get('toTable') == tname:
                            to_col = rel.get('toColumn', '')
                            for c in t.get('columns', []):
                                if c.get('name') == to_col and c.get('dataType') == 'dateTime' and not c.get('isKey'):
                                    r['info'].append(f'ℹ️ [MDL-153] Date column "{to_col}" in dimension "{tname}" is not marked as isKey — mark as key for better time intelligence')
                                    break

                # MDL-154: Measure expression too long (complexity smell)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        line_count = len(dax.strip().split('\n'))
                        if line_count > 50:
                            r['info'].append(f'ℹ️ [MDL-154] Measure "{mname}" in "{tname}" has {line_count} lines — consider breaking into helper measures for readability')

                # MDL-155: Duplicate partition names within table
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    part_names = [p.get('name', '') for p in t.get('partitions', [])]
                    seen_parts = set()
                    for pn in part_names:
                        if pn in seen_parts:
                            r['errors'].append(f'❌ [MDL-155] Duplicate partition name "{pn}" in table "{tname}"')
                        seen_parts.add(pn)

                # MDL-156: Table with mixed partition source types
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    source_types = set()
                    for p in t.get('partitions', []):
                        st = p.get('source', {}).get('type', '')
                        if st:
                            source_types.add(st)
                    if len(source_types) > 1:
                        r['warnings'].append(f'⚠️ [MDL-156] Table "{tname}" has mixed partition source types: {source_types} — may cause unexpected behavior')

                # MDL-157: IF(HASONEVALUE, VALUES) pattern → use SELECTEDVALUE
                has_one_val_pattern = _re.compile(r'IF\s*\(\s*HASONEVALUE\s*\(', _re.IGNORECASE)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if has_one_val_pattern.search(dax):
                            r['info'].append(f'ℹ️ [MDL-157] Measure "{mname}" in "{tname}" uses IF(HASONEVALUE,...) pattern — simplify with SELECTEDVALUE()')

                # ═══ OFFICIAL BPA GAPS & COMMUNITY (MDL-158 → MDL-172) ═══

                # MDL-158: DAX expression contains TODO comment (BPA: DAX_TODO)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if 'TODO' in dax.upper():
                            r['info'].append(f'ℹ️ [MDL-158] Measure "{mname}" in "{tname}" contains TODO comment — revisit before production')
                    for c in t.get('columns', []):
                        if c.get('type') == 'calculated':
                            cname = c.get('name', '')
                            cexpr = c.get('expression', '')
                            dax = ''.join(cexpr) if isinstance(cexpr, list) else str(cexpr)
                            if 'TODO' in dax.upper():
                                r['info'].append(f'ℹ️ [MDL-158] Calculated column "{cname}" in "{tname}" contains TODO comment — revisit before production')

                # MDL-159: DAX uses division operator instead of DIVIDE (BPA: DAX_DIVISION_COLUMNS)
                div_pattern = _re.compile(r'(?<!\/)\/(?!\/|\*)', _re.IGNORECASE)  # / not // or /*
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if div_pattern.search(dax):
                            # Exclude lines that are comments 
                            non_comment_lines = [l for l in dax.split('\n') if not l.strip().startswith('//') and not l.strip().startswith('--')]
                            if any('/' in l.split('//')[0] for l in non_comment_lines if '/' in l):
                                r['info'].append(f'ℹ️ [MDL-159] Measure "{mname}" in "{tname}" uses division operator (/) — consider DIVIDE() function for safe division')

                # MDL-160: Culture exists but visible objects have no translation (BPA: TRANSLATE_HIDEABLE_OBJECT_NAMES)
                cultures = model_obj.get('cultures', [])
                if cultures:
                    untranslated_count = 0
                    for t in model_obj.get('tables', []):
                        if not t.get('isHidden'):
                            tname = t.get('name', '')
                            t_translations = t.get('translations', [])
                            if not t_translations:
                                untranslated_count += 1
                    if untranslated_count > 0:
                        r['info'].append(f'ℹ️ [MDL-160] Model has {len(cultures)} culture(s) but {untranslated_count} visible tables have no translations — add translated names for localization')

                # MDL-161: Display folder has no translation when cultures exist (BPA: LAYOUT_LOCALIZE_DF)
                if cultures:
                    for t in model_obj.get('tables', []):
                        for m in t.get('measures', []):
                            df = m.get('displayFolder', '')
                            if df and not m.get('translatedDisplayFolders'):
                                mname = m.get('name', '')
                                tname = t.get('name', '?')
                                r['info'].append(f'ℹ️ [MDL-161] Measure "{mname}" in "{tname}" has displayFolder but no translations — localize for multi-language support')
                                break  # Just one warning per table

                # MDL-162: Object description exists but no translated descriptions (BPA: TRANSLATE_DESCRIPTIONS)
                if cultures:
                    for t in model_obj.get('tables', []):
                        desc = t.get('description', '')
                        if desc and not t.get('translatedDescriptions'):
                            tname = t.get('name', '?')
                            r['info'].append(f'ℹ️ [MDL-162] Table "{tname}" has description but no translated descriptions — translate for multi-language support')

                # MDL-163: DAX uses INTERSECT where TREATAS would be better
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        if 'INTERSECT(' in dax:
                            r['info'].append(f'ℹ️ [MDL-163] Measure "{mname}" in "{tname}" uses INTERSECT — consider TREATAS for virtual relationships (better performance)')

                # MDL-164: Relationship cardinality Many-to-Many without bridge table
                for rel in model_obj.get('relationships', []):
                    card = rel.get('fromCardinality', '')
                    card2 = rel.get('toCardinality', '')
                    if card == 'many' and card2 == 'many':
                        fromT = rel.get('fromTable', '?')
                        toT = rel.get('toTable', '?')
                        # Check if there's a bridge table connecting them
                        r['warnings'].append(f'⚠️ [MDL-164] Many-to-many relationship "{fromT}" ↔ "{toT}" — consider using a bridge table for reliable filter propagation')

                # MDL-165: Unused calculated tables
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    is_calc_table = any(p.get('source', {}).get('type') == 'calculated' for p in t.get('partitions', []))
                    if is_calc_table:
                        # Check if used in any relationship
                        used_in_rel = any(
                            r2.get('fromTable') == tname or r2.get('toTable') == tname
                            for r2 in model_obj.get('relationships', [])
                        )
                        # Check if has measures
                        has_measures = bool(t.get('measures'))
                        if not used_in_rel and not has_measures:
                            r['info'].append(f'ℹ️ [MDL-165] Calculated table "{tname}" is not used in any relationship and has no measures — consider if it is needed')

                # MDL-166: Measure DAX has division by constant zero risk
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = ''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)
                        if _re.search(r'/\s*0\b', dax) and 'DIVIDE(' not in dax.upper():
                            r['warnings'].append(f'⚠️ [MDL-166] Measure "{mname}" in "{tname}" may divide by zero — use DIVIDE() for safe division with fallback')

                # MDL-167: Measure with deeply nested IF (>3 levels)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        if_count = dax.count('IF(')
                        if if_count > 3:
                            r['info'].append(f'ℹ️ [MDL-167] Measure "{mname}" in "{tname}" has {if_count} nested IF statements — consider SWITCH for readability')

                # MDL-168: COUNTROWS vs COUNT misuse
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        # COUNT(column) on non-numeric columns should use COUNTA or COUNTROWS
                        if _re.search(r'COUNT\s*\(\s*\'[^\']+\'\[', dax):
                            r['info'].append(f'ℹ️ [MDL-168] Measure "{mname}" in "{tname}" uses COUNT(column) — ensure column is numeric; use COUNTA for text or COUNTROWS for row counts')

                # MDL-169: M partition expression with Power Query transformations that could be pushed to source
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for p in t.get('partitions', []):
                        src = p.get('source', {})
                        if src.get('type') == 'm':
                            m_expr = src.get('expression', '')
                            m_text = ''.join(m_expr) if isinstance(m_expr, list) else str(m_expr)
                            # Check for heavy PQ transformations
                            heavy_transforms = ['Table.TransformColumns', 'Table.AddColumn', 'Table.ExpandRecordColumn',
                                'Table.SplitColumn', 'Table.ReplaceValue', 'Table.FillDown', 'Table.Pivot', 'Table.Unpivot']
                            found = [h for h in heavy_transforms if h in m_text]
                            if len(found) > 3:
                                r['info'].append(f'ℹ️ [MDL-169] Table "{tname}" has {len(found)} Power Query transformations — consider pushing transformations to the data source or ETL layer for better performance')

                # MDL-170: Unnecessary CONVERT in DAX
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    for m in t.get('measures', []):
                        mname = m.get('name', '')
                        mexpr = m.get('expression', '')
                        dax = (''.join(mexpr) if isinstance(mexpr, list) else str(mexpr)).upper()
                        if 'CONVERT(' in dax:
                            r['info'].append(f'ℹ️ [MDL-170] Measure "{mname}" in "{tname}" uses CONVERT — ensure type conversion is necessary and not implicit')

                # MDL-171: Measure table organization (tables with only measures should be named clearly)
                for t in model_obj.get('tables', []):
                    tname = t.get('name', '?')
                    cols = t.get('columns', [])
                    measures = t.get('measures', [])
                    # Table has measures but only 1-2 system columns (like row number)
                    non_system_cols = [c for c in cols if not c.get('isHidden') and not c.get('name', '').startswith('__')]
                    if len(measures) > 5 and len(non_system_cols) == 0 and not t.get('isHidden'):
                        # This is likely a measure table — check naming
                        if '_measures' not in tname.lower() and 'measure' not in tname.lower() and '_metrics' not in tname.lower():
                            r['info'].append(f'ℹ️ [MDL-171] Table "{tname}" appears to be a measure table ({len(measures)} measures, no visible columns) — consider naming with "Measures" or "_Metrics" suffix')

                # MDL-172: Relationship one-to-one (unusual, usually 1:* or *:1)
                for rel in model_obj.get('relationships', []):
                    fromCard = rel.get('fromCardinality', 'many')
                    toCard = rel.get('toCardinality', 'one')
                    if fromCard == 'one' and toCard == 'one':
                        fromT = rel.get('fromTable', '?')
                        toT = rel.get('toTable', '?')
                        r['info'].append(f'ℹ️ [MDL-172] One-to-one relationship "{fromT}" → "{toT}" — consider merging tables unless there is a specific reason for separation')

            except json.JSONDecodeError as e:
                r['errors'].append(f'❌ [MDL-025] model.bim invalid JSON: {e}')
                _ai_debug(r, 'MDL-025', 'critical', bim_path, 'model.bim', str(e), 'valid JSON',
                    f'Fix JSON syntax error in model.bim. Error: {e}. '
                    f'Common causes: trailing comma, missing quote, unescaped backslash in file paths.')

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 4: Visual Config Deep Validation
    # ═══════════════════════════════════════════════════════════════════
    if report_dir and (report_dir / 'report.json').exists():
        rpt_json_path = report_dir / 'report.json'
        try:
            rdata = json.loads(rpt_json_path.read_text(encoding='utf-8'))

            # ERR-GEN-001: config must be stringified (critical check)
            # If report.json has config as dict instead of string, that's ERR-GEN-001
            for sec in rdata.get('sections', []):
                sec_cfg = sec.get('config')
                if sec_cfg is not None and not isinstance(sec_cfg, str):
                    r['fixable'].append(('GEN-001', 'stringify_section_config', str(rpt_json_path)))
                    r['errors'].append(f'🔥 [GEN-001] Section config is dict, must be stringified JSON! (auto-fixable)')
                elif sec_cfg and isinstance(sec_cfg, str):
                    try:
                        json.loads(sec_cfg)
                    except json.JSONDecodeError:
                        r['errors'].append(f'❌ [GEN-001b] Section config string is invalid JSON')
                        _ai_debug(r, 'GEN-001b', 'error', rpt_json_path, 'sections[].config',
                            str(sec_cfg)[:200], 'valid stringified JSON',
                            'The section config is a string but contains invalid JSON. Parse the string and fix JSON syntax errors.')

                sec_flt = sec.get('filters')
                if sec_flt is not None and not isinstance(sec_flt, str):
                    r['fixable'].append(('GEN-002', 'stringify_section_filters', str(rpt_json_path)))
                    r['errors'].append(f'🔥 [GEN-002] Section filters is array/dict, must be stringified JSON! (auto-fixable)')

                for vc in sec.get('visualContainers', []):
                    vc_cfg = vc.get('config')
                    if vc_cfg is not None and not isinstance(vc_cfg, str):
                        r['fixable'].append(('GEN-001', 'stringify_visual_config', str(rpt_json_path)))
                        r['errors'].append('🔥 [GEN-001] Visual config is dict, must be stringified JSON! (auto-fixable)')
                    vc_flt = vc.get('filters')
                    if vc_flt is not None and not isinstance(vc_flt, str):
                        r['fixable'].append(('GEN-002', 'stringify_visual_filters', str(rpt_json_path)))
                        r['errors'].append('🔥 [GEN-002] Visual filters is array/dict, must be stringified JSON! (auto-fixable)')
                    vc_dt = vc.get('dataTransforms')
                    if vc_dt is not None and not isinstance(vc_dt, str):
                        r['fixable'].append(('GEN-001', 'stringify_visual_dataTransforms', str(rpt_json_path)))
                        r['errors'].append('🔥 [GEN-001] Visual dataTransforms is dict, must be stringified JSON! (auto-fixable)')

            # Report-level checks
            if 'sections' not in rdata:
                r['errors'].append('❌ [VIS-001] report.json missing "sections"')
                _ai_debug(r, 'VIS-001', 'critical', rpt_json_path, 'root', 'missing', '"sections": [...]',
                    'Add "sections" array to report.json. Each section represents a page with visuals.')
            else:
                sections = rdata['sections']
                if not sections:
                    r['errors'].append('❌ [VIS-002] report.json has no pages (empty sections)')
                    _ai_debug(r, 'VIS-002', 'error', rpt_json_path, 'sections', '[]', 'at least 1 page/section',
                        'Add at least one section to the sections array. Each section needs: name, displayName, width, height, visualContainers.')

                all_ids = set()
                all_page_names = set()
                parent_refs = []
                
                active_idx = rdata.get('activeSectionIndex', 0)

                for i, sec in enumerate(sections):
                    page_name = sec.get('displayName', f'Page {i}')
                    
                    # RPT-020: Hidden Active Page
                    if i == active_idx and sec.get('displayOption') == 2:
                        r['warnings'].append(f'⚠️ [RPT-020] "{page_name}" is the default active page but is marked as hidden (displayOption=2)')

                    page_visual_boxes = [] # For VIS-051

                    # Duplicate page names
                    if page_name in all_page_names:
                        r['fixable'].append(('RPT-018', 'fix_duplicate_page', str(rpt_json_path), i, page_name))
                        r['warnings'].append(f'⚠️ [VIS-003] Duplicate page name: "{page_name}" (auto-fixable)')
                    all_page_names.add(page_name)

                    # Page dimensions
                    pw = sec.get('width', 1280)
                    ph = sec.get('height', 720)
                    if pw <= 0 or ph <= 0:
                        r['fixable'].append(('VIS-004', 'fix_page_dims', str(rpt_json_path), i))
                        r['errors'].append(f'❌ [VIS-004] "{page_name}" invalid dimensions: {pw}x{ph} (auto-fixable)')
                        
                    # RPT-022: Oversized Tooltip
                    if sec.get('displayOption') == 3 and (pw > 600 or ph > 600):
                        r['warnings'].append(f'⚠️ [RPT-022] "{page_name}" is a Tooltip page but is unusually large ({pw}x{ph}) — may cover the whole screen')

                    if 'visualContainers' not in sec:
                        r['errors'].append(f'❌ [VIS-005] "{page_name}" missing "visualContainers"')
                        continue

                    vcs = sec.get('visualContainers', [])
                    if not vcs:
                        r['warnings'].append(f'⚠️ [RPT-021] "{page_name}" has no visuals (Ghost Page)')

                    for j, vc in enumerate(vcs):
                        # VIS-038: Visual missing config entirely
                        if 'config' not in vc or not vc.get('config'):
                            r['fixable'].append(('VIS-038', 'fix_missing_config', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-038] "{page_name}" Visual {j}: missing config — visual cannot render (auto-fixable)')
                            continue

                        # VIS-039: Visual with zero size
                        _vw = vc.get('width', 100)
                        _vh = vc.get('height', 100)
                        if (_vw is not None and _vw == 0) or (_vh is not None and _vh == 0):
                            r['fixable'].append(('VIS-039', 'fix_visual_size', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-039] "{page_name}" Visual {j}: width/height is 0 — invisible! (auto-fixable)')

                        # GEN-014: Visual container missing height/width keys
                        if 'width' not in vc or 'height' not in vc:
                            r['fixable'].append(('GEN-014', 'fix_visual_dimensions', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [GEN-014] "{page_name}" Visual {j}: missing width/height — visual size unknown (auto-fixable)')

                        # Parse config
                        try:
                            cfg = json.loads(vc.get('config', '{}'))
                        except json.JSONDecodeError:
                            r['errors'].append(f'❌ [VIS-007] "{page_name}" Visual {j}: invalid config JSON')
                            _ai_debug(r, 'VIS-007', 'error', rpt_json_path, f'sections[{i}].visualContainers[{j}].config',
                                vc.get('config','')[:200], 'valid stringified JSON',
                                f'Fix JSON syntax in visual config string on page "{page_name}", visual {j}.')
                            continue

                        vis_name = cfg.get('name', f'visual_{j}')
                        sv = cfg.get('singleVisual', {})
                        vtype = sv.get('visualType', '?')
                        label = f'"{page_name}" [{vtype}]'

                        # Duplicate visual IDs
                        if vis_name in all_ids:
                            r['fixable'].append(('VIS-008', 'duplicate_id', vis_name, j, i))
                            r['errors'].append(f'❌ [VIS-008] {label}: duplicate ID "{vis_name}" (auto-fixable)')
                        all_ids.add(vis_name)

                        # VIS-049: Orphaned Group Child
                        parent_match = _re.search(r'"parentGroupName"\s*:\s*"([^"]+)"', vc.get('config', ''))
                        if parent_match:
                            parent_refs.append((vis_name, parent_match.group(1), label))

                        if 'visualType' not in sv:
                            r['errors'].append(f'❌ [VIS-009] {label}: missing visualType')
                            _ai_debug(r, 'VIS-009', 'error', rpt_json_path, f'sections[{i}].visualContainers[{j}].config.singleVisual.visualType',
                                'missing', 'e.g., clusteredBarChart, lineChart, card, tableEx',
                                f'Add visualType to singleVisual. Common types: clusteredBarChart, lineChart, card, slicer, tableEx, pieChart.')
                        elif vtype not in VALID_BUILTIN_VISUALS and vtype not in NON_DATA_VISUALS:
                            # VIS-058: Unrecognized visual type → CustomVisualNotFound
                            if vtype in VISUAL_TYPE_ALIASES:
                                safe_type = VISUAL_TYPE_ALIASES[vtype]
                                r['fixable'].append(('VIS-058', 'fix_visual_type', str(report_dir / 'report.json'), vtype, safe_type, str(i), str(j)))
                                r['errors'].append(
                                    f'🔥 [VIS-058] {label}: visualType "{vtype}" causes CustomVisualNotFound! '
                                    f'→ will auto-fix to "{safe_type}" (auto-fixable)')
                            else:
                                r['warnings'].append(
                                    f'⚠️ [VIS-058] {label}: visualType "{vtype}" is not a known built-in type '
                                    f'— may cause CustomVisualNotFound error')

                        # Position bounds check
                        vx = vc.get('x', 0)
                        vy = vc.get('y', 0)
                        vw = vc.get('width', 100)
                        vh = vc.get('height', 100)
                        
                        # VIS-051: Exact Duplicate Box
                        box_tuple = (vx, vy, vw, vh)
                        if box_tuple in page_visual_boxes:
                            r['fixable'].append(('VIS-051', 'fix_exact_duplicate', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-051] {label}: exact duplicate of another visual\'s box (x={vx}, y={vy}, w={vw}, h={vh}) — overlapping completely (auto-fixable)')
                        page_visual_boxes.append(box_tuple)

                        # VIS-048: Visual is completely off-canvas (Invisible)
                        if vx + vw <= 0 or vy + vh <= 0 or (pw > 0 and vx >= pw) or (ph > 0 and vy >= ph):
                            r['fixable'].append(('VIS-048', 'fix_off_canvas', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-048] {label}: completely off-canvas (x={vx}, y={vy}, w={vw}, h={vh}, page={pw}x{ph}) (auto-fixable)')
                        else:
                            if vx < 0 or vy < 0:
                                r['fixable'].append(('VIS-010', 'fix_negative_pos', str(rpt_json_path), i, j))
                                r['warnings'].append(f'⚠️ [VIS-010] {label}: negative position ({vx},{vy}) (auto-fixable)')
                            if vx + vw > pw + 50 or vy + vh > ph + 50:
                                r['fixable'].append(('VIS-011', 'fix_out_of_bounds', str(rpt_json_path), i, j, pw, ph))
                                r['warnings'].append(f'⚠️ [VIS-011] {label}: extends beyond page bounds (auto-fixable)')

                        if vw <= 0 or vh <= 0:
                            r['fixable'].append(('VIS-012', 'fix_zero_size', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-012] {label}: zero/negative size ({vw}x{vh}) (auto-fixable)')

                        # Position should be float
                        for k in ('x', 'y', 'width', 'height'):
                            val = vc.get(k)
                            if val is not None and not isinstance(val, (float, int)):
                                r['warnings'].append(f'⚠️ [VIS-013] {label}: {k}={val} must be numeric')

                        # Skip non-data visuals
                        if vtype in NON_DATA_VISUALS:
                            # Textbox must have objects.general.properties.text
                            if vtype == 'textbox':
                                objs = sv.get('objects', {})
                                if not objs.get('general', []):
                                    r['warnings'].append(f'⚠️ [VIS-056] {label}: textbox has no text content (Empty Textbox)')
                            continue

                        # Data visual checks
                        if 'projections' not in sv:
                            r['fixable'].append(('VIS-015', 'fix_missing_projections', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-015] {label}: missing projections (auto-fixable)')

                        # VIS-036: projections has empty buckets
                        projs = sv.get('projections', {})
                        for bucket_name, bucket_vals in projs.items():
                            if isinstance(bucket_vals, list) and len(bucket_vals) == 0:
                                r['warnings'].append(f'⚠️ [VIS-036] {label}: projections["{bucket_name}"] is empty array — no data will display')
                                
                        # VIS-052: Pie/Donut Missing Category
                        if vtype in ('pieChart', 'donutChart') and not projs.get('Category'):
                            r['warnings'].append(f'⚠️ [VIS-052] {label}: missing Category projection — will only show one slice')
                            
                        # VIS-053: Map Missing Spatial
                        if vtype in ('map', 'filledMap') and not projs.get('Category') and not projs.get('X') and not projs.get('Y'):
                            r['warnings'].append(f'⚠️ [VIS-053] {label}: missing Location/Lat/Lon projection — map will not render points')
                            
                        # VIS-054: Matrix Missing Rows/Cols
                        if vtype == 'matrix' and projs.get('Values') and not projs.get('Rows') and not projs.get('Columns'):
                            r['warnings'].append(f'⚠️ [VIS-054] {label}: missing Rows and Columns — matrix needs dimensions')
                            
                        # VIS-055: Gauge Missing Y
                        if vtype == 'gauge' and not projs.get('Y'):
                            r['warnings'].append(f'⚠️ [VIS-055] {label}: missing Y (Value) projection — gauge will be empty')
                            
                        # VIS-057: Card Overloaded
                        card_vals = projs.get('Y', []) or projs.get('Values', [])
                        if vtype == 'card' and len(card_vals) > 1:
                            r['errors'].append(f'❌ [VIS-057] {label}: too many fields in Values ({len(card_vals)}) — standard card only supports 1')

                        # VIS-037: Aggregation on string column (skip slicers/tables — they use text naturally)
                        if model_tables and vtype not in NON_DATA_VISUALS and vtype not in ('slicer', 'tableEx', 'pivotTable'):
                            for role_name, role_vals in projs.items():
                                for pv in (role_vals if isinstance(role_vals, list) else []):
                                    qref = pv.get('queryRef', '')
                                    if '.' in qref:
                                        _tbl, _col = qref.split('.', 1)
                                        for mt_name, mt_info in model_tables.items():
                                            if mt_name == _tbl:
                                                if _col in mt_info.get('col_types', {}):
                                                    col_type = mt_info['col_types'][_col]
                                                    if col_type == 'string' and role_name in ('Values', 'Y', 'Y2'):
                                                        r['warnings'].append(f'⚠️ [VIS-037] {label}: aggregation on text column "{_col}" — SUM/AVG will fail')

                        pq = sv.get('prototypeQuery', {})
                        if not pq:
                            r['errors'].append(f'❌ [VIS-016] {label}: missing prototypeQuery')
                            _ai_debug(r, 'VIS-016', 'error', rpt_json_path, f'sections[{i}].visualContainers[{j}].config.singleVisual.prototypeQuery',
                                'missing', '{"Version": 2, "From": [...], "Select": [...]}',
                                f'Add prototypeQuery to visual on page "{page_name}". It must have Version=2, From (table aliases), and Select (columns/aggregations).')
                            continue

                        # VIS-034: From.Type must be 0 (entity reference)
                        froms = pq.get('From', [])
                        for frm in froms:
                            from_type = frm.get('Type')
                            if from_type is not None and from_type != 0:
                                r['fixable'].append(('VIS-034', 'fix_from_type', str(rpt_json_path), i, j))
                                r['errors'].append(f'❌ [VIS-034] {label}: From.Type={from_type} must be 0 (auto-fixable)')

                        # VIS-035: prototypeQuery.Version must be "2"
                        pq_ver = pq.get('Version')
                        if pq_ver is None:
                            r['fixable'].append(('VIS-035', 'fix_pq_version', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-035] {label}: prototypeQuery missing Version — must be 2 (auto-fixable)')
                        elif pq_ver != 2:
                            r['fixable'].append(('VIS-035', 'fix_pq_version', str(rpt_json_path), i, j))
                            r['errors'].append(f'❌ [VIS-035] {label}: prototypeQuery.Version={pq_ver} must be 2 (auto-fixable)')

                        # From array validation
                        if not froms:
                            r['errors'].append(f'❌ [VIS-017] {label}: empty From array in prototypeQuery')
                            _ai_debug(r, 'VIS-017', 'error', rpt_json_path, f'{label} prototypeQuery.From',
                                '[]', '[{"Name": "t", "Entity": "TableName", "Type": 0}]',
                                f'Add From entries. Each needs Name (alias), Entity (table name from model.bim), Type=0. '
                                f'Available tables: {list(model_tables.keys()) if model_tables else "check model.bim"}')

                        selects = pq.get('Select', [])
                        if not selects:
                            r['errors'].append(f'❌ [VIS-018] {label}: empty Select array in prototypeQuery')
                            _ai_debug(r, 'VIS-018', 'error', rpt_json_path, f'{label} prototypeQuery.Select',
                                '[]', 'Select entries for each data field',
                                'Add Select entries. Column: {"Column": {"Expression": {"SourceRef": {"Source": "alias"}}, "Property": "ColName"}, "Name": "Table.Col"}. '
                                'Aggregation: {"Aggregation": {"Expression": {...}, "Function": 1}, "Name": "Sum(Table.Col)"}')

                        # From alias/entity checks
                        from_aliases = {}  # alias → entity
                        for frm in froms:
                            alias = frm.get('Name', '')
                            entity = frm.get('Entity', '')
                            if not alias:
                                r['errors'].append(f'❌ [VIS-019] {label}: From item missing Name (alias)')
                            if not entity:
                                r['errors'].append(f'❌ [VIS-020] {label}: From item missing Entity')
                            from_aliases[alias] = entity

                        # queryRef ↔ Select.Name (ERR-GEN-004)
                        proj_refs = set()
                        for role_vals in sv.get('projections', {}).values():
                            for pv in role_vals:
                                proj_refs.add(pv.get('queryRef', ''))
                        sel_names = set()
                        for s in selects:
                            name = s.get('Name', '')
                            if not name:
                                r['errors'].append(f'❌ [VIS-021] {label}: Select item missing Name')
                            sel_names.add(name)

                        mismatches = proj_refs - sel_names
                        if mismatches:
                            r['errors'].append(f'❌ [VIS-022] {label}: queryRef ≠ Select.Name: {mismatches}')
                            _ai_debug(r, 'VIS-022', 'error', rpt_json_path, f'{label} projections vs Select',
                                f'mismatched: {mismatches}', 'matching queryRef and Select.Name values',
                                f'Each projection queryRef must have a matching Select.Name. '
                                f'Mismatched refs: {mismatches}. Add or fix Select entries to match.')

                        orphan_selects = sel_names - proj_refs
                        if orphan_selects and proj_refs:
                            r['warnings'].append(f'⚠️ [VIS-023] {label}: Select not in projections: {orphan_selects}')

                        # SourceRef alias consistency (ERR-GEN-005)
                        alias_set = set(from_aliases.keys())
                        for sel in selects:
                            _check_source_refs(sel, alias_set, r['errors'], page_name, vtype)

                        # Double-wrap detection (ERR-GENQ-001) 🔥
                        for sel in selects:
                            if 'Column' in sel:
                                cv = sel['Column']
                                if isinstance(cv, dict) and 'Column' in cv and 'Expression' not in cv:
                                    r['errors'].append(f'🔥 [GENQ-001] {label}: Double-wrapped Column! Report WILL NOT LOAD!')
                                    _ai_debug(r, 'GENQ-001', 'critical', rpt_json_path, f'{label} Select[].Column',
                                        'Column.Column (double-wrapped)', 'Column.Expression.SourceRef pattern',
                                        'Fix double-wrapped Column structure. Correct format: '
                                        '{"Column": {"Expression": {"SourceRef": {"Source": "alias"}}, "Property": "ColName"}}. '
                                        'Remove the inner Column wrapper.')
                                # VIS-040: Property is dict instead of string → Missing_References
                                if isinstance(cv, dict) and not isinstance(cv.get('Property'), str):
                                    prop_val = cv.get('Property')
                                    r['fixable'].append(('VIS-040', 'fix_dict_property', str(rpt_json_path), i, j))
                                    r['errors'].append(
                                        f'🔥 [VIS-040] {label}: Column Property is dict ({prop_val}) instead of string '
                                        f'→ causes Missing_References! Likely make_table called with dict columns (auto-fixable)')
                            if 'Aggregation' in sel:
                                av = sel['Aggregation']
                                if isinstance(av, dict) and 'Aggregation' in av and 'Expression' not in av:
                                    r['errors'].append(f'🔥 [GENQ-001] {label}: Double-wrapped Aggregation! Report WILL NOT LOAD!')

                        # Aggregation Function value
                        for sel in selects:
                            if 'Aggregation' in sel:
                                agg = sel['Aggregation']
                                func = agg.get('Function')
                                if func is not None and func not in VALID_AGG_FUNCTIONS:
                                    r['errors'].append(f'❌ [VIS-024] {label}: invalid Aggregation Function={func} (valid: 0-6)')

                        # Select Name format (should be "Table.Column" or "CountNonNull(Table.Col)")
                        for sel in selects:
                            name = sel.get('Name', '')
                            if name and '.' not in name and '(' not in name:
                                r['warnings'].append(f'⚠️ [VIS-025] {label}: Select.Name "{name}" missing table prefix (should be "Table.Column")')

                        # NativeReferenceName presence
                        for sel in selects:
                            if 'NativeReferenceName' not in sel and 'Column' in sel:
                                r['warnings'].append(f'⚠️ [VIS-026] {label}: Select missing NativeReferenceName for column')

                        # Cross-reference: Entity exists in model.bim
                        if model_tables:
                            for alias, entity in from_aliases.items():
                                if entity and entity not in model_tables:
                                    r['errors'].append(f'❌ [VIS-027] {label}: Entity "{entity}" not in model.bim tables')
                                    _ai_debug(r, 'VIS-027', 'error', rpt_json_path, f'{label} From[].Entity',
                                        entity, f'one of: {list(model_tables.keys())}',
                                        f'Entity "{entity}" does not exist in model.bim. Available: {list(model_tables.keys())}.')
                                elif entity:
                                    for sel in selects:
                                        prop = _extract_property(sel)
                                        src_alias = _extract_source_alias(sel)
                                        # prop can be dict for complex expressions — skip those
                                        if prop and isinstance(prop, str) and src_alias == alias:
                                            all_names = model_tables[entity]['columns'] | model_tables[entity].get('measures', set())
                                            if prop not in all_names:
                                                r['errors'].append(f'❌ [VIS-028] {label}: Column "{prop}" not in table "{entity}"')
                                                _ai_debug(r, 'VIS-028', 'error', rpt_json_path, f'{label} Select[].Property (table "{entity}")',
                                                    prop, f'one of: {list(all_names)}',
                                                    f'Column/measure "{prop}" not found in table "{entity}". Available: {list(all_names)}.')

                        # dataTransforms JSON check
                        dt_str = vc.get('dataTransforms', '')
                        if dt_str and isinstance(dt_str, str):
                            try:
                                json.loads(dt_str)
                            except json.JSONDecodeError:
                                r['errors'].append(f'❌ [VIS-029] {label}: invalid dataTransforms JSON')

                        # filters JSON check
                        flt_str = vc.get('filters', '')
                        if flt_str and isinstance(flt_str, str):
                            try:
                                json.loads(flt_str)
                            except json.JSONDecodeError:
                                r['errors'].append(f'❌ [VIS-030] {label}: invalid filters JSON')

                        # ERR-GEN-011: drillFilterOtherVisuals
                        if vtype not in NON_DATA_VISUALS and 'drillFilterOtherVisuals' not in sv:
                            r['fixable'].append(('GEN-011', 'fix_drill_filter', str(rpt_json_path), i, j))
                            r['warnings'].append(f'⚠️ [GEN-011] {label}: missing drillFilterOtherVisuals (auto-fixable)')

                        # ERR-GEN-007: z-order check
                        z_val = vc.get('z')
                        if z_val is not None and not isinstance(z_val, (int, float)):
                            r['fixable'].append(('GEN-007', 'fix_z_order', str(rpt_json_path), i, j))
                            r['warnings'].append(f'⚠️ [GEN-007] {label}: z-order must be numeric, got {type(z_val).__name__} (auto-fixable)')

                        # VIS-043: Config parses to empty {} (no singleVisual)
                        if not sv:
                            r['errors'].append(f'❌ [VIS-043] {label}: config parses but has empty singleVisual — visual will be blank')
                            continue

                        # VIS-044: dataTransforms missing projectionActiveItems
                        dt_str_check = vc.get('dataTransforms', '')
                        if dt_str_check and isinstance(dt_str_check, str) and vtype not in NON_DATA_VISUALS:
                            try:
                                dt_obj = json.loads(dt_str_check)
                                if 'projectionActiveItems' not in dt_obj and 'projectionOrdering' not in dt_obj:
                                    r['warnings'].append(f'⚠️ [VIS-044] {label}: dataTransforms missing projectionActiveItems — visual may not show columns correctly')
                            except json.JSONDecodeError:
                                pass

                        # VIS-045: Slicer missing data objects
                        if vtype == 'slicer':
                            slicer_objs = sv.get('objects', {})
                            if not slicer_objs.get('data', []):
                                r['warnings'].append(f'⚠️ [VIS-045] {label}: slicer missing objects.data — dropdown may not appear')

                        # VIS-046: Visual references table that has no data partition
                        if model_tables:
                            for frm in pq.get('From', []):
                                entity = frm.get('Entity', '')
                                if entity in model_tables:
                                    # Check if the table has at least one partition with data source
                                    has_data_partition = model_tables[entity].get('has_partition', True)
                                    if not has_data_partition:
                                        r['warnings'].append(f'⚠️ [VIS-046] {label}: references table "{entity}" which has no data partition — visual will be empty')

                        # Measure reference check in Select
                        for sel in selects:
                            if 'Measure' in sel:
                                m_prop = sel['Measure'].get('Property', '')
                                m_src = sel['Measure'].get('Expression', {}).get('SourceRef', {}).get('Source')
                                if m_src and m_src in from_aliases:
                                    m_entity = from_aliases[m_src]
                                    if m_entity in model_tables and m_prop not in model_tables[m_entity]['measures']:
                                        r['fixable'].append(('VIS-033', 'fix_missing_measure', str(next(project_dir.glob('*.SemanticModel')) / 'model.bim'), m_entity, m_prop))
                                        r['errors'].append(f'❌ [VIS-033] {label}: Measure "{m_prop}" not in table "{m_entity}" (auto-fixable)')

                    # VIS-049: Orphaned Group Child check
                    for child_id, parent_id, lbl in parent_refs:
                        if parent_id not in all_ids:
                            r['errors'].append(f'❌ [VIS-049] {lbl} (ID: {child_id}): grouped under parent "{parent_id}" which does not exist (Orphaned)')

        except json.JSONDecodeError as e:
            r['errors'].append(f'❌ [VIS-031] report.json invalid JSON: {e}')

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 5: Additional Chart-Display Checks (NEW)
    # ═══════════════════════════════════════════════════════════════════

    # --- 5a. definition.pbism check (MDL-034) ---
    if model_dir:
        pbism_path = model_dir / 'definition.pbism'
        if not pbism_path.exists():
            r['fixable'].append(('MDL-034', 'missing_definition_pbism', str(model_dir)))
            r['errors'].append('❌ [MDL-034] Missing definition.pbism in SemanticModel — Power BI Desktop may fail to load model (auto-fixable)')

    # --- 5b. Visual-specific checks in report.json ---
    REQUIRED_PROJECTION_ROLES = {
        'lineChart': ['Category', 'Y'], 'barChart': ['Category', 'Y'],
        'columnChart': ['Category', 'Y'], 'clusteredBarChart': ['Category', 'Y'],
        'clusteredColumnChart': ['Category', 'Y'], 'donutChart': ['Category', 'Y'],
        'pieChart': ['Category', 'Y'], 'funnelChart': ['Category', 'Y'],
        'waterfallChart': ['Category', 'Y'], 'areaChart': ['Category', 'Y'],
        'stackedBarChart': ['Category', 'Y'], 'stackedColumnChart': ['Category', 'Y'],
        'stackedAreaChart': ['Category', 'Y'], 'hundredPercentStackedBarChart': ['Category', 'Y'],
        'hundredPercentStackedColumnChart': ['Category', 'Y'], 'hundredPercentStackedAreaChart': ['Category', 'Y'],
        'ribbonChart': ['Category', 'Y', 'Series'], 'lineClusteredColumnComboChart': ['Category', 'Y', 'Y2'],
        'lineStackedColumnComboChart': ['Category', 'Y', 'Y2'],
        'card': ['Values'], 'multiRowCard': ['Values'],
        'scatterChart': ['X', 'Y'], 'treemap': ['Group', 'Values'],
        'gauge': ['Value'], 'kpi': ['Indicator'],
        'table': ['Values'], 'tableEx': ['Values'], 'matrix': ['Rows', 'Values'],
        'map': ['Location'], 'filledMap': ['Location'],
        'slicer': ['Values'],
    }
    AGG_REQUIRE_NUMERIC = {0, 1, 3, 4}  # Sum, Average, Min, Max need numeric

    if report_dir and (report_dir / 'report.json').exists():
        try:
            rdata = json.loads((report_dir / 'report.json').read_text(encoding='utf-8'))
            sections = rdata.get('sections', [])

            for i, sec in enumerate(sections):
                page_name = sec.get('displayName', f'Page {i}')
                pw = sec.get('width', 1280)
                ph = sec.get('height', 720)

                # 5c. Section name validation (VIS-034)
                sec_name = sec.get('name', '')
                if not sec_name:
                    r['errors'].append(f'❌ [VIS-034] "{page_name}": missing section name (internal ID)')

                # 5d. Ordinal validation (VIS-035)
                ordinal = sec.get('ordinal')
                if ordinal is None:
                    r['warnings'].append(f'⚠️ [VIS-035] "{page_name}": missing ordinal — page ordering may be wrong')

                vcs = sec.get('visualContainers', [])
                positions = []  # for overlap detection

                for j, vc in enumerate(vcs):
                    try:
                        cfg = json.loads(vc.get('config', '{}'))
                    except json.JSONDecodeError:
                        continue

                    sv = cfg.get('singleVisual', {})
                    vtype = sv.get('visualType', '?')
                    label = f'"{page_name}" [{vtype}]'

                    # 5e. Visual too small (VIS-036)
                    vw = vc.get('width', 100)
                    vh = vc.get('height', 100)
                    vx = vc.get('x', 0)
                    vy = vc.get('y', 0)
                    if vtype not in NON_DATA_VISUALS:
                        if isinstance(vw, (int, float)) and vw < 50:
                            r['fixable'].append(('VIS-036', 'fix_visual_too_small', str(report_dir / 'report.json'), i, j, 'width'))
                            r['warnings'].append(f'⚠️ [VIS-036] {label}: width={vw} too small (min ~60) — chart may not render (auto-fixable)')
                        if isinstance(vh, (int, float)) and vh < 30:
                            r['fixable'].append(('VIS-036', 'fix_visual_too_small', str(report_dir / 'report.json'), i, j, 'height'))
                            r['warnings'].append(f'⚠️ [VIS-036] {label}: height={vh} too small (min ~40) — chart may not render (auto-fixable)')

                    # Track positions for overlap detection
                    if isinstance(vx, (int, float)) and isinstance(vy, (int, float)):
                        positions.append((round(vx), round(vy), round(vw), round(vh), j, vtype))

                    # Skip non-data visuals for remaining checks
                    if vtype in NON_DATA_VISUALS:
                        continue

                    projections = sv.get('projections', {})
                    pq = sv.get('prototypeQuery', {})

                    # 5f. Required projection roles (VIS-037)
                    required = REQUIRED_PROJECTION_ROLES.get(vtype, [])
                    for role in required:
                        if role not in projections:
                            r['errors'].append(f'🔥 [VIS-037] {label}: missing required projection role "{role}" — chart WILL BE BLANK!')
                        elif not projections[role]:
                            r['errors'].append(f'🔥 [VIS-037] {label}: projection role "{role}" is empty — chart WILL BE BLANK!')

                    # 5g. prototypeQuery Version (VIS-038)
                    if pq:
                        pq_ver = pq.get('Version')
                        if pq_ver is not None and pq_ver != 2:
                            r['errors'].append(f'❌ [VIS-038] {label}: prototypeQuery Version={pq_ver}, must be 2')

                        # 5h. From Type check (VIS-039)
                        for frm in pq.get('From', []):
                            frm_type = frm.get('Type')
                            if frm_type is not None and frm_type != 0:
                                r['errors'].append(f'❌ [VIS-039] {label}: From Type={frm_type}, must be 0 (Entity)')

                    # 5i. Aggregation on string column (VIS-040)
                    if model_tables and pq:
                        for frm in pq.get('From', []):
                            from_alias = frm.get('Name', '')
                            from_entity = frm.get('Entity', '')
                            if from_entity in model_tables:
                                col_types = model_tables[from_entity].get('col_types', {})
                                for sel in pq.get('Select', []):
                                    if 'Aggregation' in sel:
                                        agg = sel['Aggregation']
                                        func = agg.get('Function', -1)
                                        inner_col = agg.get('Expression', {}).get('Column', {})
                                        inner_alias = inner_col.get('Expression', {}).get('SourceRef', {}).get('Source', '')
                                        prop = inner_col.get('Property', '')
                                        if inner_alias == from_alias and prop in col_types:
                                            if col_types[prop] == 'string' and func in AGG_REQUIRE_NUMERIC:
                                                r['errors'].append(
                                                    f'🔥 [VIS-040] {label}: {AGG_NAMES.get(func, "?")}({from_entity}.{prop}) — '
                                                    f'column is string type! Aggregation WILL FAIL → chart blank!')

                # VIS-047: Too many visuals per page
                data_visual_count = sum(1 for vc2 in vcs if vc2.get('config') and json.loads(vc2.get('config', '{}')).get('singleVisual', {}).get('visualType', '') not in NON_DATA_VISUALS)
                if data_visual_count > 50:
                    r['warnings'].append(f'⚠️ [VIS-047] "{page_name}": {data_visual_count} data visuals on page — performance will degrade (recommended: ≤50)')

                # 5j. Visual overlap detection (VIS-041)
                if len(positions) >= 3:
                    from collections import Counter
                    pos_counter = Counter((p[0], p[1]) for p in positions if p[5] not in NON_DATA_VISUALS)
                    for (px, py), count in pos_counter.items():
                        if count >= 3:
                            r['warnings'].append(f'⚠️ [VIS-041] "{page_name}": {count} visuals stacked at position ({px},{py}) — some may be hidden')

            # 5k. Ordinal continuity check (VIS-042)
            ordinals = [sec.get('ordinal') for sec in sections if sec.get('ordinal') is not None]
            if ordinals:
                expected = list(range(len(ordinals)))
                if sorted(ordinals) != expected:
                    r['fixable'].append(('VIS-042', 'fix_ordinals', str(report_dir / 'report.json')))
                    r['warnings'].append(f'⚠️ [VIS-042] Page ordinals not sequential: {ordinals} — expected {expected} (auto-fixable)')

        except json.JSONDecodeError:
            pass  # Already caught in SECTION 4

    # --- 5l. M expression syntax validation (MDL-035, MDL-046, MDL-047) ---
    if model_dir:
        bim_path = model_dir / 'model.bim'
        if bim_path.exists():
            try:
                mdata = json.loads(bim_path.read_text(encoding='utf-8'))
                for t in mdata.get('model', {}).get('tables', []):
                    tname = t.get('name', '?')
                    for p in t.get('partitions', []):
                        src = p.get('source', {})
                        if src.get('type') == 'm':
                            expr = src.get('expression', [])
                            if isinstance(expr, list) and len(expr) >= 3:
                                # === MDL-035: Missing trailing comma check (auto-fixable) ===
                                in_let_block = False
                                has_comma_issue = False
                                for idx, line in enumerate(expr):
                                    stripped = line.strip()
                                    if stripped.lower() == 'let':
                                        in_let_block = True
                                        continue
                                    if stripped.lower().startswith('in'):
                                        in_let_block = False
                                        continue
                                    if in_let_block and idx < len(expr) - 1:
                                        next_stripped = expr[idx + 1].strip()
                                        if next_stripped.lower().startswith('in'):
                                            continue  # Last step before "in" doesn't need comma
                                        if not stripped.endswith(','):
                                            has_comma_issue = True
                                if has_comma_issue:
                                    r['fixable'].append(('MDL-035', 'fix_m_missing_commas', str(bim_path), tname))
                                    r['errors'].append(
                                        f'🔥 [MDL-035] Table "{tname}": M expression has missing trailing commas '
                                        f'→ causes "Token comma expected" crash in Power BI! (auto-fixable)')

                                # === MDL-046: Duplicate values in "in" clause ===
                                in_block_values = []
                                in_phase = False
                                for line in expr:
                                    stripped = line.strip()
                                    if stripped.lower() == 'in' or stripped.lower().startswith('in '):
                                        in_phase = True
                                        rest = stripped[2:].strip()
                                        if rest:
                                            in_block_values.append(rest)
                                    elif in_phase and stripped:
                                        in_block_values.append(stripped)

                                if len(in_block_values) > 1:
                                    r['fixable'].append(('MDL-046', 'fix_m_duplicate_in', str(bim_path), tname))
                                    r['errors'].append(
                                        f'🔥 [MDL-046] Table "{tname}": M expression has {len(in_block_values)} values '
                                        f'in "in" clause ({", ".join(in_block_values)}) — only 1 allowed! (auto-fixable)')

                                # === MDL-047: "in" references non-existent step ===
                                step_names = set()
                                for line in expr:
                                    stripped = line.strip()
                                    step_match = _re.match(r'(\w+)\s*=\s*', stripped)
                                    if step_match:
                                        step_names.add(step_match.group(1))
                                if in_block_values:
                                    in_ref = in_block_values[0]  # use first value
                                    if in_ref and step_names and in_ref not in step_names:
                                        r['fixable'].append(('MDL-047', 'fix_m_wrong_in_ref', str(bim_path), tname))
                                        r['errors'].append(
                                            f'🔥 [MDL-047] Table "{tname}": "in" references "{in_ref}" '
                                            f'which is not a defined step (valid: {", ".join(sorted(step_names))}) (auto-fixable)')

            except (json.JSONDecodeError, Exception):
                pass

    # ═══ MDL-041: Orphan table detection ═══
    if model_tables and report_dir and (report_dir / 'report.json').exists():
        try:
            rdata = json.loads((report_dir / 'report.json').read_text(encoding='utf-8'))
            visual_entities = set()
            for sec in rdata.get('sections', []):
                for vc in sec.get('visualContainers', []):
                    try:
                        cfg = json.loads(vc.get('config', '{}'))
                        sv = cfg.get('singleVisual', {})
                        pq = sv.get('prototypeQuery', {})
                        for frm in pq.get('From', []):
                            entity = frm.get('Entity', '')
                            if entity:
                                visual_entities.add(entity)
                    except json.JSONDecodeError:
                        pass
            orphan_tables = set(model_tables.keys()) - visual_entities
            for orphan in orphan_tables:
                r['info'].append(f'ℹ️ [MDL-041] Table "{orphan}" is not referenced by any visual — consider removing if unused')
        except Exception:
            pass

    # ═══════════════════════════════════════════════════════════════════
    # SECTION 6: Bookmarks and Actions Validation (BKM-001 to BKM-005)
    # ═══════════════════════════════════════════════════════════════════
    if report_dir and (report_dir / 'report.json').exists():
        try:
            rdata = json.loads((report_dir / 'report.json').read_text(encoding='utf-8'))
            
            all_page_internal_names = set()
            all_visual_ids = set()
            
            for sec in rdata.get('sections', []):
                all_page_internal_names.add(sec.get('name', ''))
                all_page_internal_names.add(sec.get('displayName', ''))
                for vc in sec.get('visualContainers', []):
                    try:
                        c = json.loads(vc.get('config', '{}'))
                        if 'name' in c:
                            all_visual_ids.add(c['name'])
                    except: pass

            rpt_config = {}
            if 'config' in rdata and isinstance(rdata['config'], str):
                try:
                    rpt_config = json.loads(rdata['config'])
                except: pass
            
            bookmarks = rpt_config.get('bookmarks', [])
            if not bookmarks and isinstance(rdata.get('bookmarks'), list):
                bookmarks = rdata.get('bookmarks')
            
            all_bookmark_names = set()
            for bkm in bookmarks:
                bkm_name = bkm.get('name', '')
                disp_name = bkm.get('displayName', '')
                if bkm_name: all_bookmark_names.add(bkm_name)
                if disp_name: all_bookmark_names.add(disp_name)
                
                # BKM-002: Invalid Data
                exp_state = bkm.get('explorationState', {})
                if isinstance(exp_state, str):
                    try:
                        json.loads(exp_state)
                    except json.JSONDecodeError:
                        r['errors'].append(f'❌ [BKM-002] Bookmark "{disp_name or bkm_name}": explorationState is invalid JSON')
                
                # BKM-001: Ghost Bookmark Target (Checks visual target in explorationState)
                exp_str = exp_state if isinstance(exp_state, str) else json.dumps(exp_state)
                # Find visual names in the state
                vis_refs = _re.findall(r'"visualName"\s*:\s*"([^"]+)"', exp_str)
                for v in vis_refs:
                    if v not in all_visual_ids and v != "None":
                        r['warnings'].append(f'⚠️ [BKM-001] Bookmark "{disp_name or bkm_name}" specifies state for non-existent Visual ID "{v}" (Ghost Target)')

            # Action Checks (BKM-003, BKM-004, BKM-005)
            for sec in rdata.get('sections', []):
                for vc in sec.get('visualContainers', []):
                    cfg_str = vc.get('config', '{}')
                    
                    # BKM-005: Invalid Web URL
                    urls = _re.findall(r'"url"\s*:\s*\{"expr"\s*:\s*\{"Literal"\s*:\s*\{"Value"\s*:\s*\'([^\']+)\'', cfg_str.replace('"', '\''))
                    urls += _re.findall(r'"url"\s*:\s*"([^"]+)"', cfg_str) # Catch simple strings too
                    for u in urls:
                        if u and not u.startswith('http://') and not u.startswith('https://'):
                            r['warnings'].append(f'⚠️ [BKM-005] Button/Shape Action: Web URL "{u}" is invalid (must start with http/https)')

                    # BKM-003: Broken Bookmark Action
                    bkm_refs = _re.findall(r'"bookmarkName"\s*:\s*\{"expr"\s*:\s*\{"Literal"\s*:\s*\{"Value"\s*:\s*\'([^\']+)\'', cfg_str.replace('"', '\''))
                    for b in bkm_refs:
                        if b and b not in all_bookmark_names:
                            r['errors'].append(f'❌ [BKM-003] Button Action points to non-existent bookmark "{b}"')

                    # BKM-004: Broken Page Nav Action
                    page_refs = _re.findall(r'"navigationDestination"\s*:\s*\{"expr"\s*:\s*\{"Literal"\s*:\s*\{"Value"\s*:\s*\'([^\']+)\'', cfg_str.replace('"', '\''))
                    for p in page_refs:
                        if p and p not in all_page_internal_names:
                            r['errors'].append(f'❌ [BKM-004] Button Action points to non-existent page "{p}"')

        except Exception as e:
            pass

    # ═══ NEW: Report Quality Checks (RPT-023 → RPT-028) ═══
    rpt_json_path = report_dir / 'report.json' if report_dir else None
    if rpt_json_path and rpt_json_path.exists():
        try:
            rpt_text = rpt_json_path.read_text(encoding='utf-8')
            rpt_data = json.loads(rpt_text)

            # RPT-023: Missing $schema property
            if '$schema' not in rpt_data:
                r['fixable'].append(('RPT-023', 'fix_add_schema', str(rpt_json_path)))
                r['warnings'].append(f'⚠️ [RPT-023] report.json missing "$schema" property — recommended for validation (auto-fixable)')

            # RPT-024: Report has > 20 pages (complexity)
            sections = rpt_data.get('sections', [])
            if len(sections) > 20:
                r['warnings'].append(f'⚠️ [RPT-024] Report has {len(sections)} pages — consider splitting into multiple reports for performance')
                _ai_debug(r, 'RPT-024', 'warning', rpt_json_path, 'sections',
                    str(len(sections)), '< 20 pages per report',
                    f'Report has {len(sections)} pages. Consider splitting into multiple reports or using bookmarks for navigation.')

            # RPT-025: Page has > 30 visuals (performance)
            for sec in sections:
                sec_name = sec.get('displayName', sec.get('name', '?'))
                vis_count = len(sec.get('visualContainers', []))
                if vis_count > 30:
                    r['warnings'].append(f'⚠️ [RPT-025] Page "{sec_name}" has {vis_count} visuals — will load slowly, consider splitting')
                    _ai_debug(r, 'RPT-025', 'warning', rpt_json_path, f'sections["{sec_name}"].visualContainers',
                        str(vis_count), '< 30 visuals per page',
                        f'Page "{sec_name}" has {vis_count} visuals — performance will degrade. Move some to a separate page or use bookmarks.')

            # RPT-028: Report schema version
            schema = rpt_data.get('$schema', '')
            if schema and '1.0.0' not in schema and '1.1.0' not in schema:
                r['warnings'].append(f'⚠️ [RPT-028] Report schema version may be unsupported: {schema}')
                _ai_debug(r, 'RPT-028', 'warning', rpt_json_path, '$schema',
                    schema, 'version 1.0.0 or 1.1.0',
                    f'Report schema "{schema}" may not be recognized. Try 1.0.0 or 1.1.0.')
        except Exception:
            pass

    # RPT-027: BOM encoding check for JSON files
    for json_file in project_dir.rglob('*.json'):
        try:
            raw = json_file.read_bytes()
            if raw[:3] == b'\xef\xbb\xbf':  # UTF-8 BOM
                r['fixable'].append(('RPT-027', 'fix_bom', str(json_file)))
                r['warnings'].append(f'⚠️ [RPT-027] File "{json_file.name}" has BOM encoding — should be UTF-8 without BOM (auto-fixable)')
        except Exception:
            pass

    # RPT-026: localSettings.json validation
    for ls_path in project_dir.rglob('localSettings.json'):
        try:
            ls_data = json.loads(ls_path.read_text(encoding='utf-8'))
            # Check for null values that cause PBI to crash
            for k, v in ls_data.items():
                if v is None:
                    r['warnings'].append(f'⚠️ [RPT-026] localSettings.json has null value for key "{k}" — may prevent PBI Desktop from opening')
                    _ai_debug(r, 'RPT-026', 'warning', ls_path, f'key "{k}"',
                        'null', 'valid string or object',
                        f'Set "{k}" to a valid value or remove it. Null values in localSettings can crash PBI Desktop.')
        except json.JSONDecodeError:
            r['warnings'].append(f'⚠️ [RPT-026] localSettings.json has invalid JSON')
        except Exception:
            pass

    # ═══ NEW: Path Safety (PATH-002 → PATH-004) ═══
    for file_path in project_dir.rglob('*'):
        abs_path = str(file_path.resolve())

        # PATH-002: Total file path exceeds 260 chars
        if len(abs_path) > 260:
            r['warnings'].append(f'⚠️ [PATH-002] File path exceeds 260 chars ({len(abs_path)} chars): ...{abs_path[-60:]}')
            _ai_debug(r, 'PATH-002', 'warning', file_path, 'file path',
                f'{len(abs_path)} chars', '< 260 chars (Windows limit)',
                f'Move project to a shorter root path or shorten file/folder names.')

        # PATH-004: Invalid characters in file/folder names
        name = file_path.name
        invalid_chars = _re.findall(r'[<>:"|?*]', name)
        if invalid_chars:
            r['errors'].append(f'❌ [PATH-004] File/folder name "{name}" contains invalid Windows characters: {invalid_chars}')
            _ai_debug(r, 'PATH-004', 'error', file_path, 'filename',
                name, 'no < > : " | ? * characters',
                f'Rename "{name}" to remove invalid characters: {invalid_chars}')

    # PATH-003: Table names that would create long TMDL paths
    if bim_path and bim_path.exists():
        try:
            bim_data = json.loads(bim_path.read_text(encoding='utf-8'))
            proj_len = len(str(project_dir.resolve()))
            for t in bim_data.get('model', {}).get('tables', []):
                tname = t.get('name', '')
                # TMDL path: project/Model.SemanticModel/definition/tables/TableName/...
                estimated_path = proj_len + 50 + len(tname) * 2
                if estimated_path > 240:
                    r['warnings'].append(f'⚠️ [PATH-003] Table "{tname}" name is very long — may exceed 260 char path limit when saved as TMDL')
                    _ai_debug(r, 'PATH-003', 'warning', bim_path, f'table "{tname}".name',
                        tname, 'shorter table name',
                        f'Table name "{tname}" ({len(tname)} chars) combined with project path may exceed Windows 260 char limit.')
        except Exception:
            pass

    # ═══ NEW: Visual Best Practices (VIS-059 → VIS-064) ═══
    if report_dir and (report_dir / 'report.json').exists():
        try:
            rpt_text = (report_dir / 'report.json').read_text(encoding='utf-8')
            rpt_data = json.loads(rpt_text)
            sections = rpt_data.get('sections', [])

            for sec in sections:
                sec_name = sec.get('displayName', sec.get('name', '?'))
                for vc in sec.get('visualContainers', []):
                    try:
                        cfg = json.loads(vc.get('config', '{}'))
                    except Exception:
                        continue

                    sv = cfg.get('singleVisual', {})
                    vtype = sv.get('visualType', '')

                    # VIS-061: Deprecated visualType
                    deprecated_visuals = {
                        'basicShape': 'shape',
                        'textbox_old': 'textbox',
                        'hundredPercentStackedBarChart': 'clusteredBarChart',
                        'hundredPercentStackedColumnChart': 'clusteredColumnChart',
                        'funnelChart': 'clusteredBarChart',
                    }
                    if vtype in deprecated_visuals:
                        replacement = deprecated_visuals[vtype]
                        r['fixable'].append(('VIS-061', 'fix_deprecated_visual', str(report_dir / 'report.json'), vtype, replacement))
                        r['warnings'].append(f'⚠️ [VIS-061] Page "{sec_name}": visual uses deprecated type "{vtype}" — should be "{replacement}" (auto-fixable)')

                    # VIS-064: dataTransforms refers to non-existent queryRef
                    dt = cfg.get('singleVisual', {}).get('objects', {})
                    if isinstance(dt, dict):
                        for obj_key, obj_val in dt.items():
                            if isinstance(obj_val, list):
                                for item in obj_val:
                                    if isinstance(item, dict):
                                        sel = item.get('selector', {})
                                        if sel and 'metadata' in sel:
                                            ref = sel['metadata']
                                            # Check if queryRef references exist in projections
                                            projs = sv.get('projections', {})
                                            all_proj_refs = set()
                                            for bucket_items in projs.values():
                                                if isinstance(bucket_items, list):
                                                    for pi in bucket_items:
                                                        if isinstance(pi, dict):
                                                            all_proj_refs.add(pi.get('queryRef', ''))
                                            if all_proj_refs and ref not in all_proj_refs:
                                                r['warnings'].append(f'⚠️ [VIS-064] Page "{sec_name}": formatting references non-existent queryRef "{ref}"')

        except Exception:
            pass

    # ═══ Print Results ═══
    _print_results(r)
    return r


def _print_results(r):
    """Pretty print validation results"""
    errs = len(r['errors'])
    warns = len(r['warnings'])
    fixes = len(r['fixable'])
    total = errs + warns

    if total == 0:
        print('✅ PBIP project is valid! Safe to open in Power BI Desktop.')
        print(f'   Checked: structure, definition.pbir, .platform, model.bim, visuals, queries')
    else:
        if errs:
            print(f'\n🔴 {errs} ERROR(s) — must fix before opening:')
            for e in r['errors']:
                print(f'  {e}')
        if warns:
            print(f'\n🟡 {warns} WARNING(s):')
            for w in r['warnings']:
                print(f'  {w}')
        if fixes:
            print(f'\n🔧 {fixes} issue(s) can be auto-fixed with validate_and_fix()')
        print(f'\n📊 Summary: {errs} errors, {warns} warnings, {fixes} auto-fixable')
        ai_count = len(r.get('ai_debug', []))
        if ai_count:
            print(f'🤖 {ai_count} issue(s) have AI debug context — use ai_fix_suggestions(r) for detailed fix instructions')


def ai_fix_suggestions(results):
    """
    Format AI debug context into a structured prompt for AI-assisted fixing.
    
    Usage:
        r = validate_pbip('/path/to/project')
        prompt = ai_fix_suggestions(r)
        # Send prompt to AI for fix suggestions
    
    Returns:
        str: Formatted prompt with all non-auto-fixable issues and fix instructions
    """
    ai_items = results.get('ai_debug', [])
    if not ai_items:
        return "✅ No AI-assisted fixes needed. All issues are either auto-fixable or the project is clean."
    
    # Group by severity
    critical = [d for d in ai_items if d.get('severity') == 'critical']
    errors = [d for d in ai_items if d.get('severity') == 'error']
    warnings = [d for d in ai_items if d.get('severity') == 'warning']
    
    lines = []
    lines.append("=" * 70)
    lines.append("🤖 AI FIX SUGGESTIONS — Non-Auto-Fixable Issues")
    lines.append("=" * 70)
    lines.append(f"Total: {len(ai_items)} issues ({len(critical)} critical, {len(errors)} errors, {len(warnings)} warnings)")
    lines.append("")
    
    def _fmt(items, header):
        if not items:
            return
        lines.append(f"{'─' * 50}")
        lines.append(f"{header}")
        lines.append(f"{'─' * 50}")
        for idx, d in enumerate(items, 1):
            lines.append(f"\n[{idx}] {d['rule_id']} — {d['severity'].upper()}")
            lines.append(f"    📁 File: {d['file']}")
            lines.append(f"    📍 Location: {d['location']}")
            lines.append(f"    ❌ Current: {d['current']}")
            lines.append(f"    ✅ Expected: {d['expected']}")
            lines.append(f"    🔧 Fix: {d['fix_instruction']}")
            if d.get('context_snippet'):
                lines.append(f"    📋 Context: {d['context_snippet']}")
    
    _fmt(critical, "🔴 CRITICAL — Must fix immediately (project won't open)")
    _fmt(errors, "🟠 ERRORS — Must fix (will cause issues)")
    _fmt(warnings, "🟡 WARNINGS — Should fix (may cause unexpected behavior)")
    
    lines.append(f"\n{'=' * 70}")
    lines.append("END OF AI FIX SUGGESTIONS")
    lines.append(f"{'=' * 70}")
    
    return '\n'.join(lines)


def _check_source_refs(obj, valid_aliases, errors, page_name, vtype):
    """Recursively check all SourceRef.Source values match From aliases"""
    if isinstance(obj, dict):
        if 'SourceRef' in obj:
            src = obj['SourceRef'].get('Source', '')
            if src and src not in valid_aliases:
                errors.append(
                    f'❌ [VIS-032] "{page_name}" [{vtype}]: SourceRef.Source="{src}" not in From aliases {valid_aliases}')
        for v in obj.values():
            _check_source_refs(v, valid_aliases, errors, page_name, vtype)
    elif isinstance(obj, list):
        for item in obj:
            _check_source_refs(item, valid_aliases, errors, page_name, vtype)


def _extract_property(sel_item):
    """Extract the Property name from a Select item"""
    if 'Column' in sel_item:
        return sel_item['Column'].get('Property')
    if 'Aggregation' in sel_item:
        agg = sel_item['Aggregation']
        expr = agg.get('Expression', {})
        if 'Column' in expr:
            return expr['Column'].get('Property')
    return None


def _extract_source_alias(sel_item):
    """Extract the SourceRef alias from a Select item"""
    if 'Column' in sel_item:
        return sel_item['Column'].get('Expression', {}).get('SourceRef', {}).get('Source')
    if 'Aggregation' in sel_item:
        agg = sel_item['Aggregation']
        expr = agg.get('Expression', {})
        if 'Column' in expr:
            return expr['Column'].get('Expression', {}).get('SourceRef', {}).get('Source')
    return None


# ═══════════════════════════════════════════════════════════════════════
# AUTO-FIX ENGINE
# ═══════════════════════════════════════════════════════════════════════

def validate_and_fix(project_dir, max_rounds=5):
    """
    Validate → Auto-fix → Re-validate loop.
    Keeps fixing until all auto-fixable issues are resolved or max_rounds reached.
    Returns final validation results.
    """
    project_dir = Path(project_dir)
    print(f'🔄 Starting validate & fix loop (max {max_rounds} rounds)...\n')

    for round_num in range(1, max_rounds + 1):
        print(f'{"="*60}')
        print(f'📋 Round {round_num}/{max_rounds}')
        print(f'{"="*60}')

        result = validate_pbip(project_dir)
        fixable = result.get('fixable', [])
        errors = result.get('errors', [])

        if not errors and not result.get('warnings'):
            print(f'\n🎉 All checks passed in round {round_num}!')
            return result

        if not fixable:
            if errors:
                print(f'\n⛔ {len(errors)} error(s) remain but none are auto-fixable.')
                print('   Manual intervention required.')
            else:
                print(f'\n✅ No errors! Only warnings remain.')
            return result

        # Apply fixes
        print(f'\n🔧 Applying {len(fixable)} fix(es)...')
        fixed_count = 0
        for fix_info in fixable:
            code = fix_info[0]
            fix_type = fix_info[1]
            try:
                if _apply_fix(project_dir, fix_info):
                    fixed_count += 1
                    print(f'  ✅ [{code}] Fixed: {fix_type}')
                else:
                    print(f'  ❌ [{code}] Could not fix: {fix_type}')
            except Exception as e:
                print(f'  ❌ [{code}] Fix failed: {e}')

        print(f'\n  Applied {fixed_count}/{len(fixable)} fixes.')

    print(f'\n⚠️ Max rounds ({max_rounds}) reached.')
    return validate_pbip(project_dir)


# ═══════════════════════════════════════════════════════════════════════
# POST-FIX M INJECTION UTILITIES
# ═══════════════════════════════════════════════════════════════════════
# IMPORTANT: validate_and_fix() rebuilds M expressions (adds ChangedTypes,
# CleanedErrors) and overwrites any custom M steps added via m_expression.
# These utilities inject custom steps AFTER auto-fix completes, so they
# cannot be overwritten.
# ═══════════════════════════════════════════════════════════════════════


def inject_m_steps(bim_path, table_name, extra_steps, final_step_name):
    """
    Inject extra M steps into a table's M expression in model.bim,
    AFTER validate_and_fix() has completed.

    Why needed:
        validate_and_fix() adds ChangedTypes + CleanedErrors steps and
        rebuilds the M let/in block, wiping any custom steps that were
        passed via the 'm_expression' table key. This function injects
        steps after the auto-fix is done, so they persist.

    Args:
        bim_path (str|Path): Path to model.bim file
        table_name (str): Name of the table to modify
        extra_steps (list[str]): M code lines to inject (each is a step)
            Example: ['  Cleaned = Table.TransformColumns(CleanedErrors, ...),',
                      '  Deduped = Table.Distinct(Cleaned, {"ID"})']
        final_step_name (str): New 'in' output reference
            Example: 'Deduped'

    Returns:
        bool: True if injection succeeded, False if table not found

    Example:
        >>> inject_m_steps(
        ...     'Project.SemanticModel/model.bim',
        ...     'Customers',
        ...     [
        ...         m_clean_key('CleanedErrors', 'ID', 'CUST-'),
        ...         '  Deduped = Table.Distinct(Cleaned_ID, {"ID"})',
        ...     ],
        ...     'Deduped'
        ... )
    """
    bim_path = Path(bim_path)
    data = json.loads(bim_path.read_text(encoding='utf-8'))

    for t in data.get('model', {}).get('tables', []):
        if t.get('name') != table_name:
            continue
        for p in t.get('partitions', []):
            src = p.get('source', {})
            if src.get('type') != 'm':
                continue
            expr = src.get('expression', [])
            if isinstance(expr, str):
                expr = expr.split('\n')

            # Find the 'in' keyword and inject before it
            new_lines = []
            found_in = False
            for line in expr:
                stripped = line.strip().lower()
                if stripped == 'in' or stripped.startswith('in '):
                    # Ensure last existing step has trailing comma
                    if new_lines and not new_lines[-1].rstrip().endswith(','):
                        new_lines[-1] = new_lines[-1].rstrip() + ','
                    # Inject custom steps
                    for step in extra_steps:
                        new_lines.append(step)
                    new_lines.append('in')
                    new_lines.append(f'  {final_step_name}')
                    found_in = True
                    break
                else:
                    new_lines.append(line)

            if not found_in:
                # Fallback: append at end
                for step in extra_steps:
                    new_lines.append(step)
                new_lines.append('in')
                new_lines.append(f'  {final_step_name}')

            src['expression'] = new_lines
            bim_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding='utf-8'
            )
            return True

    return False


def m_clean_key(last_step, col, prefix):
    """
    Generate M code to normalize a key column by extracting only digits
    and prepending a standard prefix.

    This bypasses ALL formatting issues:
    - Homoglyphs (Cyrillic 'С' vs Latin 'C')
    - BOM / zero-width characters
    - Hidden spaces / non-breaking spaces
    - Inconsistent formats (C-028 vs CUST-028 vs cust028)

    Args:
        last_step (str): Previous M step name to chain from
        col (str): Column name to clean
        prefix (str): Standard prefix (e.g., 'CUST-', 'TXN-', 'RET-')

    Returns:
        str: M code line (with trailing comma)

    Example:
        >>> m_clean_key('CleanedErrors', 'ID', 'CUST-')
        '  Cleaned_ID = Table.TransformColumns(CleanedErrors, {{"ID", ...}}),' 
    """
    return (
        f'  Cleaned_{col} = Table.TransformColumns({last_step}, '
        f'{{{{"{col}", each "{prefix}" & Text.Select(Text.From(_), '
        f'{{"0".."9"}}), type text}}}}),'
    )


def m_clean_name(last_step, col):
    """
    Generate M code to normalize a text column for case-insensitive
    deduplication. Keeps only letters, digits, spaces; converts to lowercase.

    Use this for product names, category names, etc. where:
    - 'Widget Alpha' and 'WIDGET ALPHA' should be the same
    - 'Widget Alpha™' should become 'widget alpha'
    - Hidden Unicode chars should be stripped

    Args:
        last_step (str): Previous M step name to chain from
        col (str): Column name to clean

    Returns:
        str: M code line (with trailing comma)

    Example:
        >>> m_clean_name('CleanedErrors', 'Product_Name')
        '  Cleaned_Product_Name = Table.TransformColumns(CleanedErrors, {{"Product_Name", ...}}),' 
    """
    return (
        f'  Cleaned_{col} = Table.TransformColumns({last_step}, '
        f'{{{{"{col}", each Text.Lower(Text.Trim(Text.Select(Text.From(_), '
        f'{{"a".."z"}} & {{"A".."Z"}} & {{"0".."9"}} & {{" "}}))), type text}}}}),'
    )


def validate_fix_and_clean(project_dir, project_name, clean_rules=None, max_rounds=5):
    """
    All-in-one: validate_and_fix() → inject custom M cleaning/dedup steps.

    This is the recommended way to handle dirty CSV data that needs
    deduplication on key columns. The auto-fix engine will first add
    ChangedTypes + CleanedErrors, then this function injects your
    custom cleaning/dedup steps on top.

    Args:
        project_dir (str|Path): PBIP project directory
        project_name (str): Project name (e.g., 'MyDashboard')
        clean_rules (list[dict], optional): List of cleaning rules per table.
            Each dict can have:
                - table (str, required): Table name
                - clean_keys (list[tuple]): [(col, prefix), ...] for digit extraction
                - clean_names (list[str]): [col, ...] for name normalization
                - filter_header_col (str): Column to check for embedded headers
                - filter_header_value (str): Value indicating an embedded header row
                - dedup_col (str): Column to deduplicate on
        max_rounds (int): Max auto-fix rounds (default 5)

    Returns:
        dict: Final validation results from validate_and_fix()

    Example:
        >>> validate_fix_and_clean(
        ...     'C:/project', 'MyDashboard',
        ...     clean_rules=[
        ...         {
        ...             'table': 'Customers',
        ...             'clean_keys': [('ID', 'CUST-')],
        ...             'dedup_col': 'ID',
        ...             'filter_header_col': 'ID',
        ...             'filter_header_value': 'CUST-',
        ...         },
        ...         {
        ...             'table': 'Products',
        ...             'clean_names': ['Product_Name'],
        ...             'dedup_col': 'Product_Name',
        ...             'filter_header_col': 'Product_Name',
        ...             'filter_header_value': 'product name',
        ...         },
        ...     ]
        ... )
    """
    project_dir = Path(project_dir)
    results = validate_and_fix(project_dir, max_rounds=max_rounds)

    if not clean_rules:
        return results

    bim_path = project_dir / f'{project_name}.SemanticModel' / 'model.bim'
    if not bim_path.exists():
        print(f'⚠️ model.bim not found at {bim_path}, skipping clean rules')
        return results

    print(f'\n🧹 Injecting {len(clean_rules)} custom data-cleaning rule(s)...')

    for rule in clean_rules:
        table = rule['table']
        steps = []
        last_step = 'CleanedErrors'  # auto-fix always ends with this

        # Step 1: Clean key columns (extract digits + prefix)
        for col, prefix in rule.get('clean_keys', []):
            steps.append(m_clean_key(last_step, col, prefix))
            last_step = f'Cleaned_{col}'

        # Step 2: Clean name columns (lowercase + trim + filter chars)
        for col in rule.get('clean_names', []):
            steps.append(m_clean_name(last_step, col))
            last_step = f'Cleaned_{col}'

        # Step 3: Filter embedded header rows
        filter_col = rule.get('filter_header_col')
        filter_val = rule.get('filter_header_value')
        if filter_col and filter_val:
            steps.append(
                f'  RemovedHeaders = Table.SelectRows({last_step}, '
                f'each [{filter_col}] <> "{filter_val}"),'
            )
            last_step = 'RemovedHeaders'

        # Step 4: Deduplicate
        dedup_col = rule.get('dedup_col')
        final_step = last_step
        if dedup_col:
            # Last step: no trailing comma
            steps.append(
                f'  Deduped = Table.Distinct({last_step}, {{"{dedup_col}"}})'  
            )
            final_step = 'Deduped'

        if steps:
            ok = inject_m_steps(bim_path, table, steps, final_step)
            if ok:
                print(f'  ✅ {table}: injected {len(steps)} cleaning step(s)')
            else:
                print(f'  ⚠️ {table}: table not found in model.bim')

    print('  ✅ All custom M steps injected successfully!')
    return results


def _apply_fix(project_dir, fix_info):
    """Apply a single auto-fix. Returns True if fixed."""
    project_dir = Path(project_dir)
    code = fix_info[0]
    fix_type = fix_info[1]

    if fix_type == 'pbip_missing_artifacts':
        # Fix STRUCT-003: Add artifacts to .pbip
        pbip_path = Path(fix_info[2])
        data = json.loads(pbip_path.read_text(encoding='utf-8'))
        proj_name = project_dir.name
        data['artifacts'] = [
            {"report": {"path": f"{proj_name}.Report"}},
            {"semanticModel": {"path": f"{proj_name}.SemanticModel"}}
        ]
        pbip_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'missing_definition_pbir':
        # Fix RPT-003: Create definition.pbir
        report_dir = Path(fix_info[2])
        model_dir = next(project_dir.glob('*.SemanticModel'), None)
        model_ref = f'../{model_dir.name}' if model_dir else '../Model.SemanticModel'
        pbir = {"version": "4.0", "datasetReference": {"byPath": {"path": model_ref}}}
        (report_dir / 'definition.pbir').write_text(json.dumps(pbir, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'wrong_pbir_version':
        # Fix RPT-004: Set version to 4.0
        pbir_path = Path(fix_info[2])
        data = json.loads(pbir_path.read_text(encoding='utf-8'))
        data['version'] = '4.0'
        pbir_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'wrong_model_ref':
        # Fix RPT-006: Fix model reference path
        pbir_path = Path(fix_info[2])
        model_name = fix_info[3]
        data = json.loads(pbir_path.read_text(encoding='utf-8'))
        data['datasetReference'] = {'byPath': {'path': f'../{model_name}'}}
        pbir_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'missing_platform_report':
        # Fix RPT-008: Create .platform for Report
        report_dir = Path(fix_info[2])
        proj_name = project_dir.name
        platform = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {"type": "Report", "displayName": proj_name},
            "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
        }
        (report_dir / '.platform').write_text(json.dumps(platform, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'missing_platform_model':
        # Fix MDL-002: Create .platform for SemanticModel
        mdl_dir = Path(fix_info[2])
        proj_name = project_dir.name
        platform = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
            "metadata": {"type": "SemanticModel", "displayName": proj_name},
            "config": {"version": "2.0", "logicalId": str(uuid.uuid4())}
        }
        (mdl_dir / '.platform').write_text(json.dumps(platform, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'wrong_ds_version':
        # Fix MDL-009: Set defaultPowerBIDataSourceVersion
        bim_path = Path(fix_info[2])
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        data['model']['defaultPowerBIDataSourceVersion'] = 'powerBI_V3'
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'csv_no_types':
        # Fix GENQ-002: Add TransformColumnTypes to CSV M expression
        # REWRITTEN — old handler had bugs: missing commas, duplicate in-values
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))

        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                cols = t.get('columns', [])
                type_pairs = []
                for c in cols:
                    cname = c.get('name', '')
                    ctype = c.get('dataType', 'string')
                    m_type = M_TYPE_MAP.get(ctype, 'type text')
                    type_pairs.append(f'{{"{cname}", {m_type}}}')

                for p in t.get('partitions', []):
                    src = p.get('source', {})
                    if src.get('type') == 'm':
                        expr = src.get('expression', [])
                        if isinstance(expr, str):
                            expr = expr.split('\n')

                        if 'TransformColumnTypes' not in '\n'.join(expr):
                            # Parse M expression into let-block steps and in-value
                            let_steps = []  # lines between 'let' and 'in'
                            in_value = None
                            phase = 'before'  # before/let/in

                            for line in expr:
                                stripped = line.strip()
                                if stripped.lower() == 'let':
                                    phase = 'let'
                                elif stripped.lower() == 'in' or stripped.lower().startswith('in '):
                                    phase = 'in'
                                    # If 'in' and value on same line like "in  PromotedHeaders"
                                    rest = stripped[2:].strip()
                                    if rest:
                                        in_value = rest
                                elif phase == 'let':
                                    let_steps.append(line)
                                elif phase == 'in' and in_value is None:
                                    in_value = stripped

                            # Find last step name (the one in_value references)
                            last_step = in_value or 'PromotedHeaders'

                            # Build the new ChangedTypes step
                            types_str = ', '.join(type_pairs)
                            new_step = f'  ChangedTypes = Table.TransformColumnTypes({last_step}, {{{types_str}}})'

                            # Rebuild expression with correct commas
                            new_lines = ['let']
                            for i, step in enumerate(let_steps):
                                # Ensure every step (including the last one now) has a trailing comma
                                s = step.rstrip()
                                if not s.endswith(','):
                                    s += ','
                                new_lines.append(s)
                            # Add new step (last step, no comma)
                            new_lines.append(new_step)
                            new_lines.append('in')
                            new_lines.append('  ChangedTypes')

                            src['expression'] = new_lines
                        break

        data_str = json.dumps(data, indent=2, ensure_ascii=False)
        bim_path.write_text(data_str, encoding='utf-8')
        return True

    elif fix_type in ('fix_m_missing_commas', 'fix_m_duplicate_in', 'fix_m_wrong_in_ref'):
        # Fix MDL-035/MDL-046/MDL-047: M expression syntax issues
        # Shared handler — parses let/in structure and rebuilds with correct syntax
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))

        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for p in t.get('partitions', []):
                    src = p.get('source', {})
                    if src.get('type') == 'm':
                        expr = src.get('expression', [])
                        if isinstance(expr, str):
                            expr = expr.split('\n')

                        # Parse M expression into let-block steps and in-value
                        let_steps = []
                        in_values = []
                        phase = 'before'
                        step_names = []
                        for line in expr:
                            stripped = line.strip()
                            if stripped.lower() == 'let':
                                phase = 'let'
                            elif stripped.lower() == 'in' or stripped.lower().startswith('in '):
                                phase = 'in'
                                rest = stripped[2:].strip()
                                if rest:
                                    in_values.append(rest)
                            elif phase == 'let':
                                let_steps.append(line)
                                # Track step names
                                step_match = _re.match(r'\s*(\w+)\s*=\s*', stripped)
                                if step_match:
                                    step_names.append(step_match.group(1))
                            elif phase == 'in' and stripped:
                                in_values.append(stripped)

                        if not let_steps:
                            break

                        # Determine correct in-value (last defined step)
                        correct_in = step_names[-1] if step_names else 'Source'

                        # If in-value references a valid step, keep it; otherwise use last step
                        current_in = in_values[0] if in_values else correct_in
                        if current_in not in step_names:
                            current_in = correct_in

                        # Rebuild with correct commas
                        new_lines = ['let']
                        for i, step in enumerate(let_steps):
                            s = step.rstrip()
                            is_last = (i == len(let_steps) - 1)
                            if is_last:
                                # Last step: no trailing comma
                                if s.endswith(','):
                                    s = s[:-1]
                            else:
                                # Non-last step: must have trailing comma
                                if not s.endswith(','):
                                    s += ','
                            new_lines.append(s)
                        new_lines.append('in')
                        new_lines.append(f'  {current_in}')

                        src['expression'] = new_lines
                        break

        data_str = json.dumps(data, indent=2, ensure_ascii=False)
        bim_path.write_text(data_str, encoding='utf-8')
        return True

    elif fix_type == 'duplicate_id':
        # Fix VIS-008: Regenerate unique visual ID
        vis_name = fix_info[2]
        rpt_path = next((project_dir.glob('*.Report'))) / 'report.json'
        data = json.loads(rpt_path.read_text(encoding='utf-8'))

        seen = set()
        for sec in data.get('sections', []):
            for vc in sec.get('visualContainers', []):
                try:
                    cfg = json.loads(vc.get('config', '{}'))
                    name = cfg.get('name', '')
                    if name in seen:
                        cfg['name'] = uuid.uuid4().hex[:20]
                        vc['config'] = json.dumps(cfg, ensure_ascii=False)
                    seen.add(cfg['name'])
                except json.JSONDecodeError:
                    pass

        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'invalid_uuid_report':
        # Fix RPT-012: Replace invalid logicalId with valid UUID
        plat_path = Path(fix_info[2])
        data = json.loads(plat_path.read_text(encoding='utf-8'))
        data.setdefault('config', {})['logicalId'] = str(uuid.uuid4())
        plat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'invalid_uuid_model':
        # Fix MDL-026: Replace invalid logicalId with valid UUID
        plat_path = Path(fix_info[2])
        data = json.loads(plat_path.read_text(encoding='utf-8'))
        data.setdefault('config', {})['logicalId'] = str(uuid.uuid4())
        plat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'duplicate_logical_ids':
        # Fix MDL-027: Replace Model logicalId so it differs from Report
        plat_path = Path(fix_info[2])
        data = json.loads(plat_path.read_text(encoding='utf-8'))
        data.setdefault('config', {})['logicalId'] = str(uuid.uuid4())
        plat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_encoding':
        # Fix ENC-001: Re-encode file as UTF-8
        file_path = Path(fix_info[2])
        try:
            raw = file_path.read_bytes()
            for enc in ['utf-8-sig', 'latin-1', 'cp1252', 'cp874']:
                try:
                    text = raw.decode(enc)
                    file_path.write_text(text, encoding='utf-8')
                    return True
                except (UnicodeDecodeError, UnicodeEncodeError):
                    continue
        except Exception:
            pass
        return False

    elif fix_type in ('stringify_section_config', 'stringify_visual_config', 'stringify_visual_dataTransforms'):
        # Fix GEN-001: Stringify config/dataTransforms fields
        rpt_path = Path(fix_info[2])
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        for sec in data.get('sections', []):
            if isinstance(sec.get('config'), dict):
                sec['config'] = json.dumps(sec['config'], ensure_ascii=False)
            for vc in sec.get('visualContainers', []):
                if isinstance(vc.get('config'), dict):
                    vc['config'] = json.dumps(vc['config'], ensure_ascii=False)
                if isinstance(vc.get('dataTransforms'), dict):
                    vc['dataTransforms'] = json.dumps(vc['dataTransforms'], ensure_ascii=False)
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type in ('stringify_section_filters', 'stringify_visual_filters'):
        # Fix GEN-002: Stringify filters fields
        rpt_path = Path(fix_info[2])
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        for sec in data.get('sections', []):
            if isinstance(sec.get('filters'), (list, dict)):
                sec['filters'] = json.dumps(sec['filters'], ensure_ascii=False)
            for vc in sec.get('visualContainers', []):
                if isinstance(vc.get('filters'), (list, dict)):
                    vc['filters'] = json.dumps(vc['filters'], ensure_ascii=False)
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_m_expr_format':
        # Fix GEN-009: Convert M expression from string to array
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for p in t.get('partitions', []):
                    src = p.get('source', {})
                    if src.get('type') == 'm':
                        expr = src.get('expression', '')
                        if isinstance(expr, str):
                            src['expression'] = expr.split('\n')
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_col_measure_collision':
        # Fix MDL-028: Rename measures that collide with column names
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        collisions = fix_info[4]  # list of names that collide
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for m in t.get('measures', []):
                    if m.get('name') in collisions:
                        old_name = m['name']
                        m['name'] = f'{old_name} Measure'
                        # Also update DAX expression references in other measures
                        for m2 in t.get('measures', []):
                            if m2.get('expression') and old_name in str(m2['expression']):
                                if isinstance(m2['expression'], list):
                                    m2['expression'] = [line.replace(f'[{old_name}]', f'[{old_name} Measure]') for line in m2['expression']]
                                elif isinstance(m2['expression'], str):
                                    m2['expression'] = m2['expression'].replace(f'[{old_name}]', f'[{old_name} Measure]')
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_duplicate_relationship':
        # Fix MDL-030: Remove duplicate relationship
        bim_path = Path(fix_info[2])
        dup_pair = fix_info[3]  # e.g. "Table1.col1->Table2.col2"
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        rels = data.get('model', {}).get('relationships', [])
        seen = set()
        new_rels = []
        for rel in rels:
            key = f'{rel.get("fromTable","")}.{rel.get("fromColumn","")}->{rel.get("toTable","")}.{rel.get("toColumn","")}'
            if key not in seen:
                new_rels.append(rel)
                seen.add(key)
        data['model']['relationships'] = new_rels
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_z_order':
        # Fix GEN-007: Convert z-order to float
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        z_val = vc.get('z')
        try:
            vc['z'] = float(z_val)
        except (ValueError, TypeError):
            vc['z'] = float((vis_idx + 1) * 1000)
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_drill_filter':
        # Fix GEN-011: Add drillFilterOtherVisuals to singleVisual
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        try:
            cfg = json.loads(vc.get('config', '{}'))
            sv = cfg.get('singleVisual', {})
            sv['drillFilterOtherVisuals'] = True
            cfg['singleVisual'] = sv
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            return False
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_csv_encoding':
        # Fix PQ-008: Add Encoding=65001 to Csv.Document call
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for p in t.get('partitions', []):
                    src = p.get('source', {})
                    if src.get('type') == 'm':
                        expr = src.get('expression', [])
                        if isinstance(expr, list):
                            new_expr = []
                            for line in expr:
                                if 'Csv.Document' in line and 'Encoding' not in line:
                                    # Add Encoding=65001 to options
                                    if '[Delimiter=' in line and ']' in line:
                                        line = line.replace('])', ', Encoding=65001])')
                                    elif 'Csv.Document(' in line and ')' in line:
                                        line = line.rstrip(')')
                                        line = line.rstrip(',')
                                        line += ', [Encoding=65001])'
                                new_expr.append(line)
                            src['expression'] = new_expr
                        elif isinstance(expr, str):
                            if 'Csv.Document' in expr and 'Encoding' not in expr:
                                if '[Delimiter=' in expr:
                                    expr = expr.replace('])', ', Encoding=65001])')
                                src['expression'] = expr
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_missing_measure':
        # Fix VIS-033: Create placeholder measure in model.bim
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        measure_name = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                if 'measures' not in t:
                    t['measures'] = []
                # Check if measure already exists
                existing = {m.get('name') for m in t['measures']}
                if measure_name not in existing:
                    # Create a placeholder measure — user should update the DAX
                    t['measures'].append({
                        'name': measure_name,
                        'expression': f'0 /* TODO: Replace with actual DAX for [{measure_name}] */',
                        'annotations': [{'name': 'AutoGenerated', 'value': 'true'}]
                    })
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_report_models':
        # Fix RPT-013: Add models array to report config
        rpt_path = Path(fix_info[2])
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        cfg_str = data.get('config', '{}')
        cfg = json.loads(cfg_str) if isinstance(cfg_str, str) else cfg_str
        if 'models' not in cfg:
            cfg['models'] = [{'id': 'model', 'ref': 'model'}]
        data['config'] = json.dumps(cfg, ensure_ascii=False) if isinstance(data.get('config'), str) else cfg
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_section_name':
        # Fix RPT-014: Generate hex section name
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        data['sections'][sec_idx]['name'] = uuid.uuid4().hex[:24]
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_section_displayname':
        # Fix RPT-014b: Add displayName
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        data['sections'][sec_idx]['displayName'] = f'Page {sec_idx + 1}'
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_section_dims':
        # Fix RPT-015: Set default page dimensions
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        sec = data['sections'][sec_idx]
        if not sec.get('width') or sec['width'] == 0:
            sec['width'] = 1280
        if not sec.get('height') or sec['height'] == 0:
            sec['height'] = 720
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'add_replace_error_values':
        # Fix MDL-036: Add Table.ReplaceErrorValues to M expression
        bim_path = Path(fix_info[2])
        target_table = fix_info[3]

        data = json.loads(bim_path.read_text(encoding='utf-8'))
        model = data.get('model', {})
        for t in model.get('tables', []):
            if t.get('name') != target_table:
                continue
            for p in t.get('partitions', []):
                src = p.get('source', {})
                expr = src.get('expression', [])
                if isinstance(expr, list):
                    expr_text = '\n'.join(expr)
                else:
                    expr_text = str(expr)

                if 'ReplaceErrorValues' in expr_text:
                    continue  # already has it

                # Find columns from ChangedTypes step
                col_names = []
                import re as _fix_re
                for match in _fix_re.finditer(r'\{"([^"]+)"\s*,\s*[^}]+\}', expr_text):
                    c_name = match.group(1)
                    if c_name not in col_names:
                        col_names.append(c_name)

                if not col_names:
                    continue

                # Build the new step (NO trailing comma — this is the last step before 'in')
                last_step = 'ChangedTypes'
                replace_pairs = ', '.join(f'{{"{ c }", null}}' for c in col_names)
                replace_step = f'  CleanedErrors = Table.ReplaceErrorValues({last_step}, {{{replace_pairs}}})'

                # Rebuild expression: insert CleanedErrors before 'in', fix commas
                lines = expr_text.split('\n')
                result_lines = []
                for line in lines:
                    stripped = line.strip()
                    if stripped == 'in':
                        # Ensure the previous step (ChangedTypes) has trailing comma
                        if result_lines and not result_lines[-1].rstrip().endswith(','):
                            result_lines[-1] = result_lines[-1].rstrip() + ','
                        # Add CleanedErrors WITHOUT comma (last step before 'in')
                        result_lines.append(replace_step)
                        # Add 'in' keyword
                        result_lines.append('in')
                        # Add the in-value reference
                        result_lines.append('  CleanedErrors')
                        # Skip the original 'in' line and the next non-empty line (old in-value)
                        continue
                    # Skip the old in-value (the line after 'in')
                    if result_lines and result_lines[-1].strip() == 'in':
                        continue  # skip old in-value, already replaced with CleanedErrors
                    result_lines.append(line)

                src['expression'] = result_lines

        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_visual_type':
        # Fix VIS-058: Replace unrecognized visualType with safe built-in type
        rpt_path = Path(fix_info[2])
        old_type = fix_info[3]
        new_type = fix_info[4]
        sec_idx = int(fix_info[5])
        vis_idx = int(fix_info[6])

        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        sections = data.get('sections', [])
        if sec_idx < len(sections):
            vcs = sections[sec_idx].get('visualContainers', [])
            if vis_idx < len(vcs):
                vc = vcs[vis_idx]
                cfg_str = vc.get('config', '{}')
                cfg = json.loads(cfg_str)
                sv = cfg.get('singleVisual', {})
                if sv.get('visualType') == old_type:
                    sv['visualType'] = new_type
                    vc['config'] = json.dumps(cfg, ensure_ascii=False)

        data_str = json.dumps(data, indent=2, ensure_ascii=False)
        rpt_path.write_text(data_str, encoding='utf-8')
        return True

    elif fix_type == 'fix_from_type':
        # Fix VIS-034: Set From.Type to 0
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        try:
            cfg = json.loads(vc.get('config', '{}'))
            pq = cfg.get('singleVisual', {}).get('prototypeQuery', {})
            for frm in pq.get('From', []):
                frm['Type'] = 0
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            return False
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_pq_version':
        # Fix VIS-035: Set prototypeQuery.Version to 2
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        try:
            cfg = json.loads(vc.get('config', '{}'))
            sv = cfg.get('singleVisual', {})
            if 'prototypeQuery' in sv:
                sv['prototypeQuery']['Version'] = 2
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            return False
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_missing_config':
        # Fix VIS-038: Create minimal config for visual
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        minimal_cfg = {
            'name': uuid.uuid4().hex[:20],
            'layouts': [{'id': 0, 'position': {'x': vc.get('x', 0), 'y': vc.get('y', 0), 'width': vc.get('width', 300), 'height': vc.get('height', 300)}}],
            'singleVisual': {'visualType': 'card', 'projections': {}}
        }
        vc['config'] = json.dumps(minimal_cfg, ensure_ascii=False)
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_visual_size':
        # Fix VIS-039: Set default visual size
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        if not vc.get('width') or vc['width'] == 0:
            vc['width'] = 300
        if not vc.get('height') or vc['height'] == 0:
            vc['height'] = 300
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_visual_dimensions':
        # Fix GEN-014: Add missing width/height
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        if 'width' not in vc:
            vc['width'] = 300
        if 'height' not in vc:
            vc['height'] = 300
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'missing_definition_pbism':
        # Fix MDL-034: Create definition.pbism file
        mdl_dir = Path(fix_info[2])
        pbism = {"version": "4.0", "settings": {}}
        (mdl_dir / 'definition.pbism').write_text(
            json.dumps(pbism, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_visual_too_small':
        # Fix VIS-036: Resize visual to minimum dimensions
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        dimension = fix_info[5]  # 'width' or 'height'
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        if dimension == 'width':
            vc['width'] = max(vc.get('width', 0), 60.0)
        elif dimension == 'height':
            vc['height'] = max(vc.get('height', 0), 40.0)
        # Also update config layouts position
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                if dimension == 'width':
                    pos['width'] = max(pos.get('width', 0), 60)
                elif dimension == 'height':
                    pos['height'] = max(pos.get('height', 0), 40)
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_ordinals':
        # Fix VIS-042: Reset ordinals to sequential 0,1,2,...
        rpt_path = Path(fix_info[2])
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        for idx, sec in enumerate(data.get('sections', [])):
            sec['ordinal'] = idx
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'platform_itemconfig_conflict':
        # Fix STRUCT-007: Remove item.config.json when .platform exists (mutually exclusive)
        item_cfg_path = Path(fix_info[2])
        if item_cfg_path.exists():
            item_cfg_path.unlink()
            return True
        return False

    elif fix_type == 'missing_item_config_model':
        # Fix MDL-037: Create item.config.json in SemanticModel (only when .platform absent)
        mdl_dir = Path(fix_info[2])
        if (mdl_dir / '.platform').exists():
            return False  # .platform exists → skip, they're mutually exclusive
        item_cfg = {"type": "SemanticModel", "displayName": project_dir.name}
        (mdl_dir / 'item.config.json').write_text(json.dumps(item_cfg, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'missing_item_config_report':
        # Fix MDL-038: Create item.config.json in Report (only when .platform absent)
        rpt_dir = Path(fix_info[2])
        if (rpt_dir / '.platform').exists():
            return False  # .platform exists → skip, they're mutually exclusive
        item_cfg = {"type": "Report", "displayName": project_dir.name}
        (rpt_dir / 'item.config.json').write_text(json.dumps(item_cfg, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    # ═══════════════════════════════════════════════════════════════════
    # NEW AUTO-FIX HANDLERS (Batch 1: MDL, Batch 2: VIS, Batch 3: RPT)
    # ═══════════════════════════════════════════════════════════════════

    elif fix_type == 'fix_compat_level':
        # Fix MDL-007: Set compatibilityLevel to 1567
        bim_path = Path(fix_info[2])
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        data['compatibilityLevel'] = 1567
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_duplicate_table':
        # Fix MDL-011: Rename duplicate table by appending _2
        bim_path = Path(fix_info[2])
        dup_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        count = 0
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == dup_name:
                count += 1
                if count > 1:
                    t['name'] = f'{dup_name}_{count}'
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_invalid_datatype':
        # Fix MDL-012: Map invalid dataType to closest valid one
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        col_name = fix_info[4]
        invalid_type = fix_info[5]
        TYPE_MAP = {
            'text': 'string', 'str': 'string', 'varchar': 'string', 'nvarchar': 'string', 'char': 'string',
            'integer': 'int64', 'int': 'int64', 'bigint': 'int64', 'smallint': 'int64', 'tinyint': 'int64',
            'float': 'double', 'real': 'double', 'numeric': 'double', 'number': 'double',
            'bool': 'boolean', 'bit': 'boolean',
            'date': 'dateTime', 'datetime2': 'dateTime', 'timestamp': 'dateTime',
            'money': 'decimal', 'currency': 'decimal',
        }
        new_type = TYPE_MAP.get(invalid_type.lower(), 'string')
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for c in t.get('columns', []):
                    if c.get('name') == col_name:
                        c['dataType'] = new_type
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_missing_source_col':
        # Fix MDL-013: Set sourceColumn = column name
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        col_name = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for c in t.get('columns', []):
                    if c.get('name') == col_name and not c.get('sourceColumn'):
                        c['sourceColumn'] = col_name
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_dax_parens':
        # Fix MDL-015: Auto-close/open unbalanced parentheses in DAX measure
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        measure_name = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for m in t.get('measures', []):
                    if m.get('name') == measure_name:
                        expr = m.get('expression', '')
                        dax = ''.join(expr) if isinstance(expr, list) else expr
                        opens = dax.count('(')
                        closes = dax.count(')')
                        if opens > closes:
                            dax += ')' * (opens - closes)
                        elif closes > opens:
                            dax = '(' * (closes - opens) + dax
                        m['expression'] = dax
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_empty_table':
        # Fix MDL-016: Remove table with no columns and no measures
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        tables = data.get('model', {}).get('tables', [])
        data['model']['tables'] = [t for t in tables if t.get('name') != table_name]
        # Also remove relationships referencing this table
        rels = data.get('model', {}).get('relationships', [])
        data['model']['relationships'] = [r2 for r2 in rels if r2.get('fromTable') != table_name and r2.get('toTable') != table_name]
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_m_missing_in':
        # Fix MDL-019: Add missing 'in' + last step name to M expression
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for p in t.get('partitions', []):
                    src = p.get('source', {})
                    if src.get('type') == 'm':
                        expr = src.get('expression', [])
                        if isinstance(expr, str):
                            expr = expr.split('\n')
                        # Find last step name
                        step_names = []
                        for line in expr:
                            step_match = _re.match(r'\s*(\w+)\s*=\s*', line.strip())
                            if step_match:
                                step_names.append(step_match.group(1))
                        last_step = step_names[-1] if step_names else 'Source'
                        # Ensure last step has no trailing comma
                        if expr and expr[-1].rstrip().endswith(','):
                            expr[-1] = expr[-1].rstrip()[:-1]
                        expr.append('in')
                        expr.append(f'  {last_step}')
                        src['expression'] = expr
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_self_join':
        # Fix MDL-029: Remove self-join relationship
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        rels = data.get('model', {}).get('relationships', [])
        data['model']['relationships'] = [r2 for r2 in rels if not (r2.get('fromTable') == table_name and r2.get('toTable') == table_name)]
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_inactive_rel':
        # Fix MDL-031: Remove inactive relationship
        bim_path = Path(fix_info[2])
        from_t = fix_info[3]
        from_c = fix_info[4]
        to_t = fix_info[5]
        to_c = fix_info[6]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        rels = data.get('model', {}).get('relationships', [])
        data['model']['relationships'] = [
            r2 for r2 in rels
            if not (r2.get('fromTable') == from_t and r2.get('fromColumn') == from_c
                    and r2.get('toTable') == to_t and r2.get('toColumn') == to_c
                    and r2.get('isActive') is False)
        ]
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_partition_type':
        # Fix MDL-033: Set partition type to 'm'
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for p in t.get('partitions', []):
                    if p.get('source', {}).get('type') not in ('m', 'calculated', 'none'):
                        p['source']['type'] = 'm'
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_dax_table_ref':
        # Fix MDL-039: Comment out measure that references non-existent table
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        measure_name = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for m in t.get('measures', []):
                    if m.get('name') == measure_name:
                        expr = m.get('expression', '')
                        dax = ''.join(expr) if isinstance(expr, list) else expr
                        m['expression'] = f'0 /* AUTO-DISABLED: {dax} */'
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_multi_active_rel':
        # Fix MDL-044: Set duplicate active relationships to inactive (keep only first)
        bim_path = Path(fix_info[2])
        table_a = fix_info[3]
        table_b = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        seen_first = False
        for rel in data.get('model', {}).get('relationships', []):
            pair = tuple(sorted([rel.get('fromTable', ''), rel.get('toTable', '')]))
            target = tuple(sorted([table_a, table_b]))
            if pair == target and rel.get('isActive', True):
                if seen_first:
                    rel['isActive'] = False
                else:
                    seen_first = True
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_self_ref_measure':
        # Fix MDL-045: Comment out self-referencing measure
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        measure_name = fix_info[4]
        data = json.loads(bim_path.read_text(encoding='utf-8'))
        for t in data.get('model', {}).get('tables', []):
            if t.get('name') == table_name:
                for m in t.get('measures', []):
                    if m.get('name') == measure_name:
                        expr = m.get('expression', '')
                        dax = ''.join(expr) if isinstance(expr, list) else expr
                        m['expression'] = f'0 /* AUTO-DISABLED (self-ref): {dax} */'
                        break
        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_name_whitespace':
        # Fix MDL-049: Trim whitespace from table/column/measure names
        bim_path = Path(fix_info[2])
        entity_type = fix_info[3]  # 'table', 'column', or 'measure'
        data = json.loads(bim_path.read_text(encoding='utf-8'))

        if entity_type == 'table':
            old_name = fix_info[4]
            for t in data.get('model', {}).get('tables', []):
                if t.get('name') == old_name:
                    t['name'] = old_name.strip()
                    # Also update sourceColumn if it matches
                    for c in t.get('columns', []):
                        if c.get('sourceColumn') == old_name:
                            c['sourceColumn'] = old_name.strip()
        elif entity_type == 'column':
            table_name = fix_info[4]
            old_name = fix_info[5]
            for t in data.get('model', {}).get('tables', []):
                if t.get('name') == table_name:
                    for c in t.get('columns', []):
                        if c.get('name') == old_name:
                            c['name'] = old_name.strip()
                            if c.get('sourceColumn') == old_name:
                                c['sourceColumn'] = old_name.strip()
                            break
        elif entity_type == 'measure':
            table_name = fix_info[4]
            old_name = fix_info[5]
            for t in data.get('model', {}).get('tables', []):
                if t.get('name') == table_name:
                    for m in t.get('measures', []):
                        if m.get('name') == old_name:
                            m['name'] = old_name.strip()
                            break

        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_calc_no_expr':
        # Fix MDL-054: Remove calculated table/column without expression
        bim_path = Path(fix_info[2])
        table_name = fix_info[3]
        entity_type = fix_info[4]  # 'table' or 'column'
        data = json.loads(bim_path.read_text(encoding='utf-8'))

        if entity_type == 'table':
            tables = data.get('model', {}).get('tables', [])
            data['model']['tables'] = [t for t in tables if not (
                t.get('name') == table_name and
                any(p.get('source', {}).get('type') == 'calculated' and not p.get('source', {}).get('expression')
                    for p in t.get('partitions', []))
            )]
        elif entity_type == 'column':
            col_name = fix_info[5]
            for t in data.get('model', {}).get('tables', []):
                if t.get('name') == table_name:
                    t['columns'] = [c for c in t.get('columns', [])
                                    if not (c.get('name') == col_name and c.get('type') == 'calculated' and not c.get('expression'))]
                    break

        bim_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    # ── VIS Fixes ──

    elif fix_type == 'fix_page_dims':
        # Fix VIS-004: Set page dimensions to 1280x720
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        sec = data['sections'][sec_idx]
        if not sec.get('width') or sec['width'] <= 0:
            sec['width'] = 1280
        if not sec.get('height') or sec['height'] <= 0:
            sec['height'] = 720
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_negative_pos':
        # Fix VIS-010: Set negative position to 0
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        if vc.get('x', 0) < 0:
            vc['x'] = 0.0
        if vc.get('y', 0) < 0:
            vc['y'] = 0.0
        # Also update config layouts
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                if pos.get('x', 0) < 0:
                    pos['x'] = 0
                if pos.get('y', 0) < 0:
                    pos['y'] = 0
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_out_of_bounds':
        # Fix VIS-011: Clamp visual to page bounds
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        pw = fix_info[5]
        ph = fix_info[6]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        vw = vc.get('width', 300)
        vh = vc.get('height', 200)
        if vc.get('x', 0) + vw > pw:
            vc['x'] = max(0, pw - vw)
        if vc.get('y', 0) + vh > ph:
            vc['y'] = max(0, ph - vh)
        # Update config layouts
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                pos['x'] = vc['x']
                pos['y'] = vc['y']
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_zero_size':
        # Fix VIS-012: Set zero/negative size to 300x200
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        if vc.get('width', 0) <= 0:
            vc['width'] = 300
        if vc.get('height', 0) <= 0:
            vc['height'] = 200
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                if pos.get('width', 0) <= 0:
                    pos['width'] = 300
                if pos.get('height', 0) <= 0:
                    pos['height'] = 200
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_missing_projections':
        # Fix VIS-015: Add empty projections to visual
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        try:
            cfg = json.loads(vc.get('config', '{}'))
            sv = cfg.get('singleVisual', {})
            if 'projections' not in sv:
                sv['projections'] = {}
            cfg['singleVisual'] = sv
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            return False
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_off_canvas':
        # Fix VIS-048: Move off-canvas visual to 0,0
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        vc['x'] = 0.0
        vc['y'] = 0.0
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                pos['x'] = 0
                pos['y'] = 0
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_exact_duplicate':
        # Fix VIS-051: Offset duplicate visual by +20px
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        vis_idx = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        vc = data['sections'][sec_idx]['visualContainers'][vis_idx]
        vc['x'] = vc.get('x', 0) + 20
        vc['y'] = vc.get('y', 0) + 20
        try:
            cfg = json.loads(vc.get('config', '{}'))
            for layout in cfg.get('layouts', []):
                pos = layout.get('position', {})
                pos['x'] = pos.get('x', 0) + 20
                pos['y'] = pos.get('y', 0) + 20
            vc['config'] = json.dumps(cfg, ensure_ascii=False)
        except json.JSONDecodeError:
            pass
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    # ── RPT Fixes ──

    elif fix_type == 'fix_platform_type':
        # Fix RPT-009: Set .platform type to correct value
        plat_path = Path(fix_info[2])
        correct_type = fix_info[3]  # 'Report' or 'SemanticModel'
        data = json.loads(plat_path.read_text(encoding='utf-8'))
        data.setdefault('metadata', {})['type'] = correct_type
        plat_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_report_filters':
        # Fix RPT-016: Reset invalid report-level filters to empty array
        rpt_path = Path(fix_info[2])
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        data['filters'] = '[]'
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    elif fix_type == 'fix_duplicate_page':
        # Fix RPT-018: Rename duplicate page by appending " (2)"
        rpt_path = Path(fix_info[2])
        sec_idx = fix_info[3]
        old_name = fix_info[4]
        data = json.loads(rpt_path.read_text(encoding='utf-8'))
        data['sections'][sec_idx]['displayName'] = f'{old_name} (2)'
        rpt_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return True

    return False


# ═══════════════════════════════════════════════════════════════════════
# ADAPTIVE DESIGN ENGINE — Dynamic layout/style generation (no presets)
# ═══════════════════════════════════════════════════════════════════════
import random as _random, math as _math, colorsys as _colorsys

# ─── Stage 1: Data Profiler ───

def _profile_data(df):
    """Analyze DataFrame → return data signature for visual planning."""
    date_cols, cat_cols, num_cols, id_cols = [], [], [], []
    cardinality = {}
    try:
        import pandas as pd
    except ImportError:
        return {'date_cols': [], 'cat_cols': [], 'num_cols': [], 'id_cols': [],
                'signature': 'unknown', 'total_rows': 0, 'cardinality': {}}

    for col in df.columns:
        dtype = df[col].dtype
        nunique = df[col].nunique()
        cardinality[col] = nunique
        if 'date' in col.lower() or 'time' in col.lower():
            date_cols.append(col)
        elif dtype in ('int64', 'float64'):
            if nunique == len(df) or '_id' in col.lower() or col.lower().endswith('id'):
                id_cols.append(col)
            else:
                num_cols.append(col)
        elif dtype == 'object':
            try:
                pd.to_datetime(df[col], errors='raise', infer_datetime_format=True)
                date_cols.append(col)
            except Exception:
                if nunique > len(df) * 0.8:
                    id_cols.append(col)
                else:
                    cat_cols.append(col)
        else:
            cat_cols.append(col)

    # Determine data signature
    if date_cols and num_cols:
        sig = 'time_series'
    elif len(cat_cols) >= 2 and num_cols:
        sig = 'multi_category'
    elif cat_cols and len(num_cols) >= 3:
        sig = 'multi_metric'
    elif cat_cols and num_cols:
        sig = 'category_metric'
    elif num_cols:
        sig = 'numeric_only'
    else:
        sig = 'categorical_only'

    # Compute correlations between numeric cols
    correlations = []
    if len(num_cols) >= 2:
        try:
            corr = df[num_cols].corr()
            for i, c1 in enumerate(num_cols):
                for c2 in num_cols[i+1:]:
                    correlations.append((c1, c2, abs(corr.loc[c1, c2])))
        except Exception:
            pass

    return {
        'date_cols': date_cols, 'cat_cols': cat_cols,
        'num_cols': num_cols, 'id_cols': id_cols,
        'signature': sig, 'total_rows': len(df),
        'cardinality': cardinality, 'correlations': correlations
    }


# ─── Stage 2: Visual Planner ───

# Visual pools by data pattern
_VISUAL_POOLS = {
    'kpi':        ['card', 'card_states', 'kpi', 'multi_row_card'],
    'trend':      ['line_chart', 'area_chart', 'stacked_area', 'combo_chart',
                   'line_clustered_combo'],
    'compare':    ['bar_chart', 'column_chart', 'clustered_column',
                   'stacked_bar', 'stacked_column'],
    'proportion': ['donut', 'pie_chart', 'treemap', 'hundred_pct_bar',
                   'hundred_pct_column'],
    'relation':   ['scatter', 'combo_chart'],
    'detail':     ['table', 'matrix'],
    'geo':        ['map', 'filled_map'],
    'filter':     ['slicer'],
}

# Map visual plan types to make_* functions
_VISUAL_BUILDERS = {
    'card': 'make_card', 'card_states': 'make_card_with_states',
    'kpi': 'make_kpi', 'multi_row_card': 'make_multi_row_card',
    'line_chart': 'make_line_chart', 'area_chart': 'make_area_chart',
    'stacked_area': 'make_stacked_area', 'combo_chart': 'make_combo_chart',
    'line_clustered_combo': 'make_line_clustered_combo',
    'bar_chart': 'make_bar_chart', 'column_chart': 'make_column_chart',
    'clustered_column': 'make_clustered_column',
    'stacked_bar': 'make_stacked_bar', 'stacked_column': 'make_stacked_column',
    'donut': 'make_donut', 'pie_chart': 'make_pie_chart',
    'treemap': 'make_treemap', 'hundred_pct_bar': 'make_hundred_pct_bar',
    'hundred_pct_column': 'make_hundred_pct_column',
    'scatter': 'make_scatter', 'table': 'make_table', 'matrix': 'make_matrix',
    'map': 'make_map', 'filled_map': 'make_filled_map', 'slicer': 'make_slicer',
}

def _plan_visuals(profile, rng):
    """Randomly select appropriate visual types from pools based on data profile."""
    plan = []
    date_cols = profile['date_cols']
    cat_cols = profile['cat_cols']
    num_cols = profile['num_cols']
    sig = profile['signature']

    # 1) KPI cards — 2-4 random numeric cols
    n_cards = min(rng.randint(2, 4), len(num_cols))
    card_nums = rng.sample(num_cols, n_cards) if num_cols else []
    for nc in card_nums:
        func = 1 if any(k in nc.lower() for k in ('avg','rate','score','pct','ratio')) else 0
        vtype = rng.choice(_VISUAL_POOLS['kpi'])
        plan.append({'role': 'kpi', 'vtype': vtype, 'col': nc, 'func': func})

    # 2) Trend chart (if time-series)
    if date_cols and num_cols:
        vtype = rng.choice(_VISUAL_POOLS['trend'])
        val_col = rng.choice(num_cols)
        extra = {}
        if vtype in ('combo_chart', 'line_clustered_combo') and len(num_cols) >= 2:
            cols2 = rng.sample(num_cols, 2)
            extra = {'val_col2': cols2[1]}
            val_col = cols2[0]
        if vtype == 'stacked_area' and cat_cols:
            extra['series_col'] = rng.choice(cat_cols)
        plan.append({'role': 'trend', 'vtype': vtype, 'cat_col': date_cols[0],
                     'val_col': val_col, **extra})

    # 3) Comparison chart (if categories)
    if cat_cols and num_cols:
        vtype = rng.choice(_VISUAL_POOLS['compare'])
        val_col = rng.choice(num_cols)
        extra = {}
        if vtype in ('stacked_bar', 'stacked_column') and len(cat_cols) >= 2:
            extra['series_col'] = cat_cols[1]
        plan.append({'role': 'compare', 'vtype': vtype, 'cat_col': cat_cols[0],
                     'val_col': val_col, **extra})

    # 4) Proportion chart
    if cat_cols and num_cols:
        vtype = rng.choice(_VISUAL_POOLS['proportion'])
        extra = {}
        if 'hundred_pct' in vtype and len(cat_cols) >= 2:
            extra['series_col'] = cat_cols[1]
        elif 'hundred_pct' in vtype:
            vtype = rng.choice(['donut', 'pie_chart', 'treemap'])
        plan.append({'role': 'proportion', 'vtype': vtype, 'cat_col': cat_cols[0],
                     'val_col': rng.choice(num_cols), **extra})

    # 5) Scatter (if correlated numerics)
    corrs = profile.get('correlations', [])
    if corrs and rng.random() > 0.3:
        best = max(corrs, key=lambda x: x[2])
        plan.append({'role': 'relation', 'vtype': 'scatter',
                     'x_col': best[0], 'y_col': best[1],
                     'detail_col': cat_cols[0] if cat_cols else None})

    # 6) Detail table
    tcols = (cat_cols[:2] + num_cols[:3])[:5]
    if tcols:
        plan.append({'role': 'detail', 'vtype': 'table', 'columns': tcols})

    # 7) Slicer (50% chance if categories exist)
    if cat_cols and rng.random() > 0.5:
        plan.append({'role': 'filter', 'vtype': 'slicer', 'col': rng.choice(cat_cols)})

    return plan


# ─── Stage 3: Layout Generator ───

_LAYOUT_STRATEGIES = ['grid', 'hero', 'dashboard', 'magazine', 'rows']

def _generate_layout(visual_plan, rng, page_w=1280, page_h=720):
    """Generate random layout positions within constraints. Returns list of rects."""
    strategy = rng.choice(_LAYOUT_STRATEGIES)
    n = len(visual_plan)
    if n == 0:
        return []

    margin = rng.randint(12, 28)
    gap = rng.randint(8, 20)
    usable_w = page_w - 2 * margin
    usable_h = page_h - 2 * margin
    rects = []

    if strategy == 'dashboard':
        # KPI cards top row, charts below
        kpis = [i for i, v in enumerate(visual_plan) if v['role'] == 'kpi']
        others = [i for i, v in enumerate(visual_plan) if v['role'] != 'kpi']
        # KPI row
        if kpis:
            kpi_h = rng.randint(80, 110)
            kw = (usable_w - gap * (len(kpis) - 1)) // max(len(kpis), 1)
            for j, idx in enumerate(kpis):
                rects.append((idx, margin + j * (kw + gap), margin, kw, kpi_h))
            chart_y = margin + kpi_h + gap
        else:
            chart_y = margin
        # Remaining visuals in grid
        remain_h = page_h - chart_y - margin
        if others:
            cols = min(rng.choice([2, 3]), len(others))
            rows_n = _math.ceil(len(others) / cols)
            cw = (usable_w - gap * (cols - 1)) // cols
            ch = (remain_h - gap * (rows_n - 1)) // max(rows_n, 1)
            ch = max(ch, 150)
            for j, idx in enumerate(others):
                r, c = divmod(j, cols)
                rects.append((idx, margin + c * (cw + gap), chart_y + r * (ch + gap), cw, ch))

    elif strategy == 'hero':
        # First non-KPI visual takes ~60% width, rest on the side + below
        kpis = [i for i, v in enumerate(visual_plan) if v['role'] == 'kpi']
        others = [i for i, v in enumerate(visual_plan) if v['role'] != 'kpi']
        # KPI row
        y_cursor = margin
        if kpis:
            kpi_h = rng.randint(75, 100)
            kw = (usable_w - gap * (len(kpis) - 1)) // max(len(kpis), 1)
            for j, idx in enumerate(kpis):
                rects.append((idx, margin + j * (kw + gap), y_cursor, kw, kpi_h))
            y_cursor += kpi_h + gap
        remain_h = page_h - y_cursor - margin
        if others:
            hero_w = int(usable_w * rng.uniform(0.55, 0.65))
            hero_h = min(int(remain_h * 0.7), remain_h)
            rects.append((others[0], margin, y_cursor, hero_w, hero_h))
            side_x = margin + hero_w + gap
            side_w = usable_w - hero_w - gap
            side_items = others[1:]
            if side_items:
                sh = (hero_h - gap * (len(side_items) - 1)) // max(len(side_items), 1)
                sh = max(sh, 120)
                for j, idx in enumerate(side_items):
                    rects.append((idx, side_x, y_cursor + j * (sh + gap), side_w, sh))

    elif strategy == 'magazine':
        # Asymmetric: mix of large and small tiles
        kpis = [i for i, v in enumerate(visual_plan) if v['role'] == 'kpi']
        others = [i for i, v in enumerate(visual_plan) if v['role'] != 'kpi']
        y_cursor = margin
        if kpis:
            kpi_h = rng.randint(70, 100)
            kw = (usable_w - gap * (len(kpis) - 1)) // max(len(kpis), 1)
            for j, idx in enumerate(kpis):
                rects.append((idx, margin + j * (kw + gap), y_cursor, kw, kpi_h))
            y_cursor += kpi_h + gap
        remain_h = page_h - y_cursor - margin
        # Alternate between full-width and half-width
        i = 0
        for idx in others:
            if i % 3 == 0:  # full width
                h = rng.randint(180, min(280, remain_h))
                rects.append((idx, margin, y_cursor, usable_w, h))
                y_cursor += h + gap
            else:  # half width
                hw = (usable_w - gap) // 2
                x = margin if (i % 2 == 1) else margin + hw + gap
                h = rng.randint(160, min(250, remain_h))
                rects.append((idx, x, y_cursor, hw, h))
                if i % 2 == 0:
                    y_cursor += h + gap
            i += 1

    elif strategy == 'rows':
        # Each visual gets full width row
        kpis = [i for i, v in enumerate(visual_plan) if v['role'] == 'kpi']
        others = [i for i, v in enumerate(visual_plan) if v['role'] != 'kpi']
        y_cursor = margin
        if kpis:
            kpi_h = rng.randint(70, 95)
            kw = (usable_w - gap * (len(kpis) - 1)) // max(len(kpis), 1)
            for j, idx in enumerate(kpis):
                rects.append((idx, margin + j * (kw + gap), y_cursor, kw, kpi_h))
            y_cursor += kpi_h + gap
        remain_h = page_h - y_cursor - margin
        if others:
            rh = (remain_h - gap * (len(others) - 1)) // max(len(others), 1)
            rh = max(rh, 140)
            for idx in others:
                rects.append((idx, margin, y_cursor, usable_w, rh))
                y_cursor += rh + gap

    else:  # grid (default)
        cols = min(rng.choice([2, 3]), n)
        rows_n = _math.ceil(n / cols)
        cw = (usable_w - gap * (cols - 1)) // cols
        ch = (usable_h - gap * (rows_n - 1)) // max(rows_n, 1)
        ch = max(ch, 120)
        for j in range(n):
            r, c = divmod(j, cols)
            rects.append((j, margin + c * (cw + gap), margin + r * (ch + gap), cw, ch))

    # Sort by visual index and return as list of dicts
    rects.sort(key=lambda r: r[0])
    return [{'idx': r[0], 'x': r[1], 'y': r[2], 'w': r[3], 'h': r[4]} for r in rects]


def _check_no_overlap(rects):
    """Check that no two rects overlap. Returns True if no overlaps."""
    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            a, b = rects[i], rects[j]
            if not (a['x'] + a['w'] <= b['x'] or b['x'] + b['w'] <= a['x'] or
                    a['y'] + a['h'] <= b['y'] or b['y'] + b['h'] <= a['y']):
                return False
    return True


# ─── Stage 4: Style Generator ───

def _hsl_to_hex(h, s, l):
    """Convert HSL (h:0-360, s:0-1, l:0-1) to hex color."""
    r, g, b = _colorsys.hls_to_rgb(h / 360.0, l, s)
    return f'#{int(r*255):02X}{int(g*255):02X}{int(b*255):02X}'

def _hex_to_rgb(hex_color):
    """Convert hex to RGB tuple (0-255)."""
    h = hex_color.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def _relative_luminance(hex_color):
    """Calculate relative luminance for contrast ratio."""
    r, g, b = _hex_to_rgb(hex_color)
    def _lin(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)

def _contrast_ratio(c1, c2):
    """WCAG contrast ratio between two hex colors."""
    l1 = _relative_luminance(c1)
    l2 = _relative_luminance(c2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def _generate_style(rng):
    """Generate a random but harmonious style. No presets — pure color theory."""
    base_hue = rng.randint(0, 359)
    is_dark = rng.random() > 0.45  # ~55% chance dark mode

    if is_dark:
        bg_color = _hsl_to_hex(base_hue, rng.uniform(0.05, 0.15), rng.uniform(0.08, 0.15))
        fg_color = _hsl_to_hex(base_hue, rng.uniform(0.05, 0.1), rng.uniform(0.85, 0.95))
        # Dark mode: cards slightly lighter than page, page slightly darker
        card_bg = _hsl_to_hex(base_hue, rng.uniform(0.05, 0.12), rng.uniform(0.13, 0.20))
        page_bg = _hsl_to_hex(base_hue, rng.uniform(0.05, 0.10), rng.uniform(0.06, 0.10))
        card_border_color = _hsl_to_hex(base_hue, rng.uniform(0.05, 0.10), rng.uniform(0.20, 0.28))
    else:
        bg_color = _hsl_to_hex(base_hue, rng.uniform(0.0, 0.08), rng.uniform(0.95, 0.99))
        fg_color = _hsl_to_hex(base_hue, rng.uniform(0.1, 0.2), rng.uniform(0.12, 0.25))
        # Light mode: cards pure white, page off-white/light gray
        card_bg = '#FFFFFF'
        page_bg = _hsl_to_hex(base_hue, rng.uniform(0.02, 0.06), rng.uniform(0.93, 0.96))
        card_border_color = _hsl_to_hex(base_hue, rng.uniform(0.02, 0.06), rng.uniform(0.88, 0.92))

    # Generate accent colors using color harmony
    harmony = rng.choice(['complementary', 'analogous', 'triadic', 'split'])
    accents = []
    n_accents = rng.randint(4, 6)

    if harmony == 'complementary':
        hues = [base_hue, (base_hue + 180) % 360]
    elif harmony == 'analogous':
        spread = rng.randint(25, 40)
        hues = [base_hue, (base_hue + spread) % 360, (base_hue - spread) % 360]
    elif harmony == 'triadic':
        hues = [base_hue, (base_hue + 120) % 360, (base_hue + 240) % 360]
    else:  # split-complementary
        hues = [base_hue, (base_hue + 150) % 360, (base_hue + 210) % 360]

    for i in range(n_accents):
        h = hues[i % len(hues)] + rng.randint(-10, 10)
        s = rng.uniform(0.55, 0.85)
        l = rng.uniform(0.45, 0.65) if is_dark else rng.uniform(0.35, 0.55)
        color = _hsl_to_hex(h % 360, s, l)
        # Ensure readable against background
        if _contrast_ratio(color, bg_color) < 3.0:
            l = 0.7 if is_dark else 0.3
            color = _hsl_to_hex(h % 360, s, l)
        accents.append(color)

    # Ensure fg has good contrast
    if _contrast_ratio(fg_color, bg_color) < 4.5:
        fg_color = '#FFFFFF' if is_dark else '#1A1A2E'

    # Beautification: weighted toward modern look (no 0px radius, prefer subtle shadow)
    border_radius = rng.choice([6, 8, 8, 10, 10, 12, 12, 14])
    shadow = rng.choices(['none', 'subtle', 'medium'], weights=[10, 55, 35])[0]
    header_size = rng.randint(20, 26)
    body_size = rng.randint(11, 13)
    # Card transparency (0=opaque, 100=fully transparent)
    card_transparency = rng.randint(0, 8) if is_dark else 0
    # Title font: modern sans-serif
    title_font = rng.choice(['Segoe UI Semibold', 'DIN', 'Segoe UI', 'Segoe UI Semibold'])

    return {
        'bg_color': bg_color, 'fg_color': fg_color,
        'accent_colors': accents, 'is_dark': is_dark,
        'border_radius': border_radius, 'shadow': shadow,
        'header_size': header_size, 'body_size': body_size,
        'harmony': harmony, 'base_hue': base_hue,
        'card_bg': card_bg, 'page_bg': page_bg,
        'card_border_color': card_border_color,
        'card_transparency': card_transparency,
        'title_font': title_font
    }


def _make_vc_style(style):
    """
    Generate vcObjects for visual containers from style settings.
    Adds: background, border with rounded corners, drop shadow, and title styling.
    These translate directly to Power BI visual container formatting.
    """
    vc = {}

    # ── Background ──
    card_bg = style.get('card_bg', '#FFFFFF')
    transparency = style.get('card_transparency', 0)
    vc['background'] = [{'properties': {
        'show': {'expr': {'Literal': {'Value': 'true'}}},
        'color': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{card_bg}'"}}}}},
        'transparency': {'expr': {'Literal': {'Value': f'{transparency}D'}}}
    }}]

    # ── Border with rounded corners ──
    radius = style.get('border_radius', 10)
    border_color = style.get('card_border_color', '#E0E0E0')
    if radius > 0:
        vc['border'] = [{'properties': {
            'show': {'expr': {'Literal': {'Value': 'true'}}},
            'color': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{border_color}'"}}}}},
            'radius': {'expr': {'Literal': {'Value': f'{radius}D'}}}
        }}]

    # ── Drop Shadow ──
    shadow_type = style.get('shadow', 'subtle')
    if shadow_type in ('subtle', 'medium'):
        # preset: 1=slight outer, 2=outer, 3=center, 4=inner
        shadow_preset = '1' if shadow_type == 'subtle' else '2'
        shadow_color = '#000000' if not style.get('is_dark') else '#000000'
        vc['dropShadow'] = [{'properties': {
            'show': {'expr': {'Literal': {'Value': 'true'}}},
            'preset': {'expr': {'Literal': {'Value': f"'{shadow_preset}'"}}},
            'color': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{shadow_color}'"}}}}},
            'position': {'expr': {'Literal': {'Value': "'Outer'"}}}
        }}]

    # ── Title styling ──
    fg = style.get('fg_color', '#333333')
    title_font = style.get('title_font', 'Segoe UI Semibold')
    title_size = style.get('header_size', 22)
    vc['title'] = [{'properties': {
        'show': {'expr': {'Literal': {'Value': 'true'}}},
        'fontColor': {'solid': {'color': {'expr': {'Literal': {'Value': f"'{fg}'"}}}}},
        'fontSize': {'expr': {'Literal': {'Value': f"'{title_size}'"}}},
        'fontFamily': {'expr': {'Literal': {'Value': f"'{title_font}'"}}},
        'alignment': {'expr': {'Literal': {'Value': "'left'"}}}
    }}]

    return vc


# ─── Stage 5: Fitness Scorer ───

def _score_layout(layout, style, page_w=1280, page_h=720):
    """Score a layout+style candidate 0-100 based on design principles."""
    if not layout:
        return {'total': 0}

    scores = {}

    # 1. Alignment (20%) — how many visuals share x or y coordinates
    xs = [r['x'] for r in layout]
    ys = [r['y'] for r in layout]
    x_groups = len(set(xs))
    y_groups = len(set(ys))
    n = len(layout)
    alignment = max(0, 100 - (x_groups + y_groups - 2) * 10)
    scores['alignment'] = min(alignment, 100)

    # 2. Balance (20%) — distribution across quadrants
    cx, cy = page_w / 2, page_h / 2
    q_areas = [0, 0, 0, 0]  # TL, TR, BL, BR
    for r in layout:
        rc_x = r['x'] + r['w'] / 2
        rc_y = r['y'] + r['h'] / 2
        qi = (0 if rc_x < cx else 1) + (0 if rc_y < cy else 2)
        q_areas[qi] += r['w'] * r['h']
    total_area = sum(q_areas)
    if total_area > 0:
        ideal = total_area / 4
        deviation = sum(abs(q - ideal) for q in q_areas) / total_area
        scores['balance'] = max(0, int(100 - deviation * 150))
    else:
        scores['balance'] = 50

    # 3. Proximity (15%) — consistent spacing
    gaps_h, gaps_v = [], []
    sorted_x = sorted(layout, key=lambda r: (r['y'], r['x']))
    for i in range(len(sorted_x) - 1):
        a, b = sorted_x[i], sorted_x[i + 1]
        if abs(a['y'] - b['y']) < 20:  # same row
            gap = b['x'] - (a['x'] + a['w'])
            if gap > 0:
                gaps_h.append(gap)
        else:
            gap = b['y'] - (a['y'] + a['h'])
            if gap > 0:
                gaps_v.append(gap)
    all_gaps = gaps_h + gaps_v
    if len(all_gaps) >= 2:
        avg_gap = sum(all_gaps) / len(all_gaps)
        variance = sum((g - avg_gap) ** 2 for g in all_gaps) / len(all_gaps)
        cv = (variance ** 0.5) / max(avg_gap, 1)
        scores['proximity'] = max(0, int(100 - cv * 100))
    else:
        scores['proximity'] = 70

    # 4. Contrast (15%) — fg/bg contrast ratio
    cr = _contrast_ratio(style['fg_color'], style['bg_color'])
    scores['contrast'] = min(100, int((cr / 7.0) * 100))

    # 5. Hierarchy (15%) — size variation (KPIs should be smaller than charts)
    areas = [r['w'] * r['h'] for r in layout]
    if len(areas) >= 2:
        area_range = max(areas) / max(min(areas), 1)
        scores['hierarchy'] = min(100, int(area_range * 20))
    else:
        scores['hierarchy'] = 50

    # 6. Whitespace (15%) — total used vs available
    total_used = sum(r['w'] * r['h'] for r in layout)
    total_avail = page_w * page_h
    fill_ratio = total_used / total_avail
    # Ideal: 50-75% fill
    if 0.45 <= fill_ratio <= 0.78:
        scores['whitespace'] = 90 + int((1 - abs(fill_ratio - 0.62) / 0.16) * 10)
    elif fill_ratio < 0.45:
        scores['whitespace'] = max(30, int(fill_ratio / 0.45 * 80))
    else:
        scores['whitespace'] = max(30, int((1 - fill_ratio) / 0.22 * 80))

    # Weighted total
    weights = {'alignment': 0.20, 'balance': 0.20, 'proximity': 0.15,
               'contrast': 0.15, 'hierarchy': 0.15, 'whitespace': 0.15}
    scores['total'] = int(sum(scores[k] * weights[k] for k in weights))
    return scores


# ─── Adaptive Builder: assemble visuals from plan + layout ───

def _inject_vc_style(visual_container, style):
    """
    Inject vcObjects styling into a visual container.
    Decodes the config JSON → merges vcObjects → re-encodes.
    """
    if not style:
        return visual_container
    try:
        cfg = json.loads(visual_container.get('config', '{}'))
        vc_style = _make_vc_style(style)
        sv = cfg.get('singleVisual', {})
        existing_vc = sv.get('vcObjects', {})
        # Merge: style vcObjects + existing (existing wins on conflicts)
        merged = {**vc_style, **existing_vc}
        sv['vcObjects'] = merged
        cfg['singleVisual'] = sv
        visual_container['config'] = json.dumps(cfg, separators=(',', ':'))
    except (json.JSONDecodeError, TypeError, KeyError):
        pass  # Don't break if config is malformed
    return visual_container


def _build_visual(plan_item, x, y, w, h, z, table_name, style):
    """Build a visual container from a plan item using the make_* functions, with vcObjects styling."""
    vtype = plan_item['vtype']
    role = plan_item['role']
    vis = None

    if role == 'kpi':
        col = plan_item['col']
        func = plan_item.get('func', 0)
        title = f'{AGG_NAMES.get(func, "Sum")} of {col}'
        if vtype == 'card_states':
            vis = make_card_with_states(x, y, w, h, table_name, col, func, title=title, z=z)
        elif vtype == 'multi_row_card':
            vis = make_multi_row_card(x, y, w, h, table_name, [col], title=title, z=z)
        elif vtype == 'kpi':
            vis = make_kpi(x, y, w, h, table_name, col, ind_func=func, title=title, z=z)
        else:
            vis = make_card(x, y, w, h, table_name, col, func, title=title, z=z)

    elif role == 'trend':
        cat = plan_item['cat_col']
        val = plan_item['val_col']
        title = f'{val} over {cat}'
        if vtype == 'area_chart':
            vis = make_area_chart(x, y, w, h, table_name, cat, val, title=title, z=z)
        elif vtype == 'stacked_area' and 'series_col' in plan_item:
            vis = make_stacked_area(x, y, w, h, table_name, cat, plan_item['series_col'], val, title=title, z=z)
        elif vtype in ('combo_chart',) and 'val_col2' in plan_item:
            vis = make_combo_chart(x, y, w, h, table_name, cat, val, plan_item['val_col2'], title=title, z=z)
        elif vtype == 'line_clustered_combo' and 'val_col2' in plan_item:
            vis = make_line_clustered_combo(x, y, w, h, table_name, cat, val, plan_item['val_col2'], title=title, z=z)
        else:
            vis = make_line_chart(x, y, w, h, table_name, cat, val, title=title, z=z)

    elif role == 'compare':
        cat = plan_item['cat_col']
        val = plan_item['val_col']
        title = f'{val} by {cat}'
        series = plan_item.get('series_col')
        if vtype == 'stacked_bar' and series:
            vis = make_stacked_bar(x, y, w, h, table_name, cat, series, val, title=title, z=z)
        elif vtype == 'stacked_column' and series:
            vis = make_stacked_column(x, y, w, h, table_name, cat, series, val, title=title, z=z)
        elif vtype == 'clustered_column':
            vis = make_clustered_column(x, y, w, h, table_name, cat, val, title=title, z=z)
        elif vtype == 'column_chart':
            vis = make_column_chart(x, y, w, h, table_name, cat, val, title=title, z=z)
        else:
            vis = make_bar_chart(x, y, w, h, table_name, cat, val, title=title, z=z)

    elif role == 'proportion':
        cat = plan_item['cat_col']
        val = plan_item['val_col']
        title = f'{val} Distribution'
        series = plan_item.get('series_col')
        if vtype == 'hundred_pct_bar' and series:
            vis = make_hundred_pct_bar(x, y, w, h, table_name, cat, series, val, title=title, z=z)
        elif vtype == 'hundred_pct_column' and series:
            vis = make_hundred_pct_column(x, y, w, h, table_name, cat, series, val, title=title, z=z)
        elif vtype == 'treemap':
            vis = make_treemap(x, y, w, h, table_name, cat, val, title=title, z=z)
        elif vtype == 'pie_chart':
            vis = make_pie_chart(x, y, w, h, table_name, cat, val, title=title, z=z)
        else:
            vis = make_donut(x, y, w, h, table_name, cat, val, title=title, z=z)

    elif role == 'relation':
        vis = make_scatter(x, y, w, h, table_name, plan_item['x_col'], plan_item['y_col'],
                           detail_col=plan_item.get('detail_col'), title='Correlation', z=z)

    elif role == 'detail':
        vis = make_table(x, y, w, h, table_name, plan_item['columns'], title='Details', z=z)

    elif role == 'filter':
        vis = make_slicer(x, y, w, h, table_name, plan_item['col'], z=z)

    elif role == 'date_filter':
        date_style = plan_item.get('date_style', 'between')
        vis = make_date_slicer(x, y, w, h, table_name, plan_item['col'],
                               title=plan_item.get('title'), z=z, style=date_style)

    # Fallback
    if vis is None:
        vis = make_card(x, y, w, h, table_name, plan_item.get('col', ''), z=z)

    # ✨ Inject vcObjects styling (border radius, shadow, background, title)
    return _inject_vc_style(vis, style)


# ─── AI Page Planner — semantic column analysis ───

# Semantic keyword → theme mapping
_THEME_KEYWORDS = {
    'financial':   ['sales', 'revenue', 'profit', 'cost', 'price', 'amount', 'budget',
                    'income', 'expense', 'margin', 'discount', 'tax', 'fee', 'payment'],
    'geographic':  ['country', 'region', 'state', 'city', 'location', 'address', 'zip',
                    'postal', 'territory', 'area', 'district', 'province', 'geo', 'lat', 'lon'],
    'temporal':    ['date', 'time', 'month', 'year', 'quarter', 'week', 'day', 'hour',
                    'period', 'created', 'updated', 'timestamp'],
    'product':     ['product', 'item', 'sku', 'category', 'brand', 'model', 'type',
                    'variant', 'catalog', 'inventory', 'stock'],
    'customer':    ['customer', 'client', 'user', 'name', 'email', 'phone', 'age',
                    'gender', 'segment', 'tier', 'member', 'account'],
    'performance': ['score', 'rating', 'kpi', 'target', 'goal', 'growth', 'rate',
                    'conversion', 'retention', 'churn', 'satisfaction', 'nps'],
    'operations':  ['status', 'order', 'shipment', 'delivery', 'fulfillment', 'channel',
                    'source', 'medium', 'campaign', 'platform', 'method'],
}

# Theme → page name + visual emphasis
_THEME_PAGE_CONFIG = {
    'financial':   {'name': 'Financial Overview',   'emphasis': ['kpi', 'trend', 'compare']},
    'geographic':  {'name': 'Geographic Analysis',  'emphasis': ['compare', 'proportion']},
    'temporal':    {'name': 'Trend Analysis',       'emphasis': ['trend', 'compare']},
    'product':     {'name': 'Product Analysis',     'emphasis': ['compare', 'proportion', 'detail']},
    'customer':    {'name': 'Customer Insights',    'emphasis': ['proportion', 'compare', 'kpi']},
    'performance': {'name': 'Performance Dashboard','emphasis': ['kpi', 'trend', 'compare']},
    'operations':  {'name': 'Operations Overview',  'emphasis': ['compare', 'proportion', 'detail']},
}

def _analyze_column_themes(profile):
    """AI-like semantic analysis: map columns to themes by name keywords."""
    all_cols = profile['date_cols'] + profile['cat_cols'] + profile['num_cols']
    col_themes = {}  # col → theme
    theme_cols = {}  # theme → [cols]

    for col in all_cols:
        col_lower = col.lower().replace('_', ' ').replace('-', ' ')
        best_theme, best_score = None, 0
        for theme, keywords in _THEME_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in col_lower)
            if score > best_score:
                best_score = score
                best_theme = theme
        if best_theme and best_score > 0:
            col_themes[col] = best_theme
            theme_cols.setdefault(best_theme, []).append(col)

    # Unassigned columns go to 'general'
    for col in all_cols:
        if col not in col_themes:
            col_themes[col] = 'general'
            theme_cols.setdefault('general', []).append(col)

    return col_themes, theme_cols


def _plan_pages(profile, rng):
    """
    AI-powered page planner: analyze data semantics → decide pages + topics.
    Returns list of page specs: [{'name': str, 'plan': [visual_plan_items]}]
    """
    col_themes, theme_cols = _analyze_column_themes(profile)
    date_cols = profile['date_cols']
    cat_cols = profile['cat_cols']
    num_cols = profile['num_cols']

    # Determine which themes are significant (≥2 columns)
    sig_themes = [t for t, cols in theme_cols.items()
                  if len(cols) >= 2 and t != 'general']

    pages = []

    # ─── Page 1: Executive Overview (always) ───
    overview_plan = []
    # KPIs from top numeric cols
    n_cards = min(rng.randint(2, 4), len(num_cols))
    for nc in (rng.sample(num_cols, n_cards) if num_cols else []):
        func = 1 if any(k in nc.lower() for k in ('avg','rate','score','pct','ratio')) else 0
        vtype = rng.choice(_VISUAL_POOLS['kpi'])
        overview_plan.append({'role': 'kpi', 'vtype': vtype, 'col': nc, 'func': func})

    # Main trend or comparison
    if date_cols and num_cols:
        vtype = rng.choice(['line_chart', 'area_chart'])
        overview_plan.append({'role': 'trend', 'vtype': vtype,
                             'cat_col': date_cols[0], 'val_col': rng.choice(num_cols)})
    if cat_cols and num_cols:
        vtype = rng.choice(['bar_chart', 'column_chart', 'donut'])
        role = 'proportion' if vtype == 'donut' else 'compare'
        overview_plan.append({'role': role, 'vtype': vtype,
                             'cat_col': cat_cols[0], 'val_col': rng.choice(num_cols)})
    pages.append({'name': 'Executive Overview', 'plan': overview_plan})

    # ─── Themed Pages (from semantic analysis) ───
    for theme in sig_themes:
        cols = theme_cols[theme]
        cfg = _THEME_PAGE_CONFIG.get(theme, {'name': theme.title(), 'emphasis': ['compare']})
        page_plan = []

        # Find numeric + categorical cols for this theme
        t_nums = [c for c in cols if c in num_cols]
        t_cats = [c for c in cols if c in cat_cols]
        t_dates = [c for c in cols if c in date_cols]

        # Borrow from global pools if theme has too few
        if not t_nums:
            t_nums = num_cols[:2]
        if not t_cats and cat_cols:
            t_cats = cat_cols[:1]

        # KPIs for this theme
        if t_nums and 'kpi' in cfg['emphasis']:
            for nc in t_nums[:rng.randint(1, 3)]:
                func = 1 if any(k in nc.lower() for k in ('avg','rate','score','pct')) else 0
                page_plan.append({'role': 'kpi', 'vtype': rng.choice(_VISUAL_POOLS['kpi']),
                                  'col': nc, 'func': func})

        # Trend for this theme
        if (t_dates or date_cols) and t_nums and 'trend' in cfg['emphasis']:
            d_col = t_dates[0] if t_dates else date_cols[0]
            vtype = rng.choice(_VISUAL_POOLS['trend'][:3])  # line, area, stacked_area
            extra = {}
            if vtype == 'stacked_area' and t_cats:
                extra['series_col'] = t_cats[0]
            page_plan.append({'role': 'trend', 'vtype': vtype,
                             'cat_col': d_col, 'val_col': rng.choice(t_nums), **extra})

        # Comparison for this theme
        if t_cats and t_nums and 'compare' in cfg['emphasis']:
            vtype = rng.choice(_VISUAL_POOLS['compare'])
            extra = {}
            if vtype in ('stacked_bar', 'stacked_column') and len(t_cats) >= 2:
                extra['series_col'] = t_cats[1]
            page_plan.append({'role': 'compare', 'vtype': vtype,
                             'cat_col': t_cats[0], 'val_col': rng.choice(t_nums), **extra})

        # Proportion for this theme
        if t_cats and t_nums and 'proportion' in cfg['emphasis']:
            vtype = rng.choice(['donut', 'pie_chart', 'treemap'])
            page_plan.append({'role': 'proportion', 'vtype': vtype,
                             'cat_col': t_cats[0], 'val_col': rng.choice(t_nums)})

        # Detail table
        if 'detail' in cfg['emphasis']:
            tcols = (t_cats[:2] + t_nums[:3])[:5]
            if tcols:
                page_plan.append({'role': 'detail', 'vtype': 'table', 'columns': tcols})

        if page_plan:
            pages.append({'name': cfg['name'], 'plan': page_plan})

    # ─── Detail Page (if enough data and ≤3 pages so far) ───
    if len(pages) <= 3:
        detail_plan = []
        # Scatter if correlations exist
        corrs = profile.get('correlations', [])
        if corrs:
            best = max(corrs, key=lambda x: x[2])
            detail_plan.append({'role': 'relation', 'vtype': 'scatter',
                               'x_col': best[0], 'y_col': best[1],
                               'detail_col': cat_cols[0] if cat_cols else None})
        # Full detail table
        all_cols = (cat_cols[:3] + num_cols[:4])[:6]
        if all_cols:
            detail_plan.append({'role': 'detail', 'vtype': 'table', 'columns': all_cols})
        # Category slicer
        if cat_cols:
            detail_plan.append({'role': 'filter', 'vtype': 'slicer',
                               'col': rng.choice(cat_cols)})
        if detail_plan:
            pages.append({'name': 'Data Explorer', 'plan': detail_plan})

    # ─── Auto Date Slicer: inject into EVERY page when date columns exist ───
    if date_cols:
        primary_date = date_cols[0]
        date_styles = ['between', 'relative', 'before', 'after']
        for page in pages:
            # Don't add if page already has a date filter
            has_date_filter = any(item.get('role') == 'date_filter' for item in page['plan'])
            if not has_date_filter:
                chosen_style = rng.choice(date_styles[:2])  # prefer 'between' or 'relative'
                page['plan'].append({
                    'role': 'date_filter',
                    'vtype': 'date_slicer',
                    'col': primary_date,
                    'date_style': chosen_style,
                    'title': f'📅 {primary_date}'
                })

    # Cap at 5 pages max
    return pages[:5]


# ─── Full Project Generator (Fix #2 — CSV → PBIP) ───

def auto_generate_dashboard(csv_path, project_name=None, output_dir=None,
                            candidates=5, seed=None, verbose=False):
    """
    Full auto: CSV → complete PBIP dashboard project.
    Uses Adaptive Design Engine — randomly generates multiple layout/style
    candidates, scores them, and picks the best one. No fixed presets.

    Args:
        csv_path: Path to CSV file
        project_name: Optional project name (default: CSV filename)
        output_dir: Optional output directory
        candidates: Number of design candidates to generate and score (default: 5)
        seed: Random seed for reproducibility (default: None = random every time)
        verbose: Print scoring details for all candidates
    """
    try:
        import pandas as pd
    except ImportError:
        print('❌ pandas required: pip install pandas')
        return None

    csv_path = Path(csv_path).resolve()
    if not csv_path.exists():
        print(f'❌ File not found: {csv_path}')
        return None

    try:
        df = pd.read_csv(csv_path, nrows=500)
    except Exception as e:
        print(f'❌ Cannot read CSV: {e}')
        return None

    project_name = project_name or csv_path.stem
    output_dir = Path(output_dir or csv_path.parent / project_name)
    table_name = csv_path.stem.replace(' ','_').replace('-','_')

    # Stage 1: Profile data
    profile = _profile_data(df)
    col_themes, theme_cols = _analyze_column_themes(profile)
    detected_themes = [t for t in theme_cols if t != 'general' and len(theme_cols[t]) >= 2]
    print(f'📊 Data Profile: {profile["signature"]} | '
          f'{len(profile["date_cols"])} date, {len(profile["cat_cols"])} cat, '
          f'{len(profile["num_cols"])} num, {len(profile["id_cols"])} ID cols')
    if detected_themes:
        print(f'🧠 Detected themes: {", ".join(detected_themes)}')

    # Stage 2-5: Generate N candidates per page → pick best per page
    master_rng = _random.Random(seed)

    # AI Page Planning
    page_specs = _plan_pages(profile, _random.Random(master_rng.randint(0, 2**31)))
    print(f'📄 Pages planned: {len(page_specs)} → {", ".join(p["name"] for p in page_specs)}')

    # Generate shared style (one palette for all pages)
    style_rng = _random.Random(master_rng.randint(0, 2**31))
    best_style = None
    best_style_score = -1
    for _ in range(candidates):
        s = _generate_style(style_rng)
        cr = _contrast_ratio(s['fg_color'], s['bg_color'])
        sc = min(100, int(cr / 7.0 * 100))
        if sc > best_style_score:
            best_style_score = sc
            best_style = s
    style = best_style

    mode_icon = '🌙 Dark' if style['is_dark'] else '☀️ Light'
    print(f'🎨 Style: {mode_icon} | {style["harmony"]} harmony | '
          f'bg={style["bg_color"]} fg={style["fg_color"]}')

    # Generate layout per page, pick best candidate
    all_pages = []
    for pi, pspec in enumerate(page_specs):
        plan = pspec['plan']
        best_score = -1
        best_layout = None

        for ci in range(candidates):
            c_seed = master_rng.randint(0, 2**31)
            rng = _random.Random(c_seed)
            layout = _generate_layout(plan, rng)
            score = _score_layout(layout, style)
            if not _check_no_overlap(layout):
                score['total'] = max(0, score['total'] - 30)

            if verbose:
                print(f'  Page "{pspec["name"]}" #{ci+1}: score={score["total"]} '
                      f'visuals={len(plan)}')

            if score['total'] > best_score:
                best_score = score['total']
                best_layout = layout

        # Build visuals for this page
        visuals = []
        z = 0
        if best_layout:
            for i, plan_item in enumerate(plan):
                rect = next((r for r in best_layout if r['idx'] == i), None)
                if rect:
                    vis = _build_visual(plan_item, rect['x'], rect['y'],
                                       rect['w'], rect['h'], z, table_name, style)
                    visuals.append(vis)
                    z += 1000

        all_pages.append({'name': pspec['name'], 'visuals': visuals})
        print(f'  ✅ Page {pi+1}: "{pspec["name"]}" — {len(visuals)} visuals, score={best_score}')

    # Apply theme from style
    theme = make_custom_theme(
        name='Adaptive', bg_color=style['bg_color'], fg_color=style['fg_color'],
        accent_colors=style['accent_colors']
    )

    report = make_report_json(all_pages, page_bg=style.get('page_bg'))

    # Inject theme into report config
    try:
        rpt_cfg = json.loads(report.get('config', '{}'))
        rpt_cfg['theme'] = theme
        report['config'] = json.dumps(rpt_cfg, ensure_ascii=False)
    except (json.JSONDecodeError, TypeError):
        pass

    # Generate model.bim columns
    date_cols = profile['date_cols']
    col_defs = []
    for col in df.columns:
        dtype = df[col].dtype
        if dtype == 'int64':
            pbi_type = 'int64'
        elif dtype == 'float64':
            pbi_type = 'double'
        elif col in date_cols:
            pbi_type = 'dateTime'
        else:
            pbi_type = 'string'
        col_defs.append({'name': col, 'type': pbi_type})

    # Measures
    num_cols = profile['num_cols']
    measures = []
    for nc in num_cols[:4]:
        measures.append({'name': f'Total {nc}', 'expression': f"SUM('{table_name}'[{nc}])", 'format': '#,##0'})
    if len(num_cols) >= 1:
        measures.append({'name': f'Avg {num_cols[0]}', 'expression': f"AVERAGE('{table_name}'[{num_cols[0]}])", 'format': '#,##0.00'})

    model = make_model_bim(project_name, [{
        'name': table_name, 'csv_path': str(csv_path),
        'columns': col_defs, 'measures': measures
    }])

    # Write files
    _write_pbip_project(output_dir, project_name, report, model)
    validate_pbip(output_dir)
    total_vis = sum(len(p['visuals']) for p in all_pages)
    print(f'\n🎉 Dashboard created: {output_dir}')
    print(f'   📄 Pages: {len(all_pages)} | Visuals: {total_vis}')
    for p in all_pages:
        print(f'      → {p["name"]} ({len(p["visuals"])} visuals)')
    print(f'   🎨 Colors: bg={style["bg_color"]} fg={style["fg_color"]} accents={style["accent_colors"][:3]}...')
    return output_dir



def _write_pbip_project(output_dir, project_name, report, model):
    """Write all PBIP project files to disk (Fix #16 — error handling)"""
    output_dir = Path(output_dir)
    report_dir = output_dir / f'{project_name}.Report'
    model_dir = output_dir / f'{project_name}.SemanticModel'

    try:
        report_dir.mkdir(parents=True, exist_ok=True)
        model_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f'❌ Cannot create directories: {e}')
        return

    def _write_json(path, data):
        try:
            Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        except Exception as e:
            print(f'❌ Cannot write {path}: {e}')

    # .pbip
    _write_json(output_dir / f'{project_name}.pbip', {
        'version': '1.0',
        'artifacts': [{'report': {'path': f'{project_name}.Report'}}],
        'settings': {'enableAutoRecovery': True}
    })

    # Report files
    _write_json(report_dir / 'report.json', report)
    _write_json(report_dir / 'definition.pbir', {
        'version': '4.0',
        'datasetReference': {'byPath': {'path': f'../{project_name}.SemanticModel'}}
    })
    _write_json(report_dir / '.platform', {
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json',
        'metadata': {'type': 'Report', 'displayName': project_name},
        'config': {'version': '2.0', 'logicalId': str(uuid.uuid4())}
    })

    # Model files
    _write_json(model_dir / 'model.bim', model)
    _write_json(model_dir / 'definition.pbism', {'version': '4.2', 'settings': {}})
    _write_json(model_dir / '.platform', {
        '$schema': 'https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json',
        'metadata': {'type': 'SemanticModel', 'displayName': project_name},
        'config': {'version': '2.0', 'logicalId': str(uuid.uuid4())}
    })

# ─── Checker Capabilities (merged from powerbi-checker) ───

def check(project_dir, fix=False, strict=False, html=None, output_json=False):
    """
    Unified validation entry point. Use this from other scripts.

    Args:
        project_dir: Path to PBIP project directory
        fix: If True, auto-fix errors
        strict: If True, treat warnings as errors
        html: If set, path to save HTML report
        output_json: If True, return JSON string

    Returns:
        dict with validation results
    """
    if fix:
        result = run_check_and_fix(project_dir, strict=strict)
    else:
        result = run_check(project_dir, strict=strict)

    if html:
        generate_html_report([result], html)

    if output_json:
        return format_json([result])

    return result


def run_check(project_dir, strict=False):
    """Run validation on a single PBIP project with metadata."""
    from datetime import datetime
    result = validate_pbip(str(project_dir))
    if strict:
        result['errors'].extend(result['warnings'])
        result['warnings'] = []
    result['passed'] = len(result['errors']) == 0
    result['project'] = str(project_dir)
    result['timestamp'] = datetime.now().isoformat()
    return result


def run_check_and_fix(project_dir, strict=False):
    """Run validation + auto-fix loop with metadata."""
    from datetime import datetime
    result = validate_and_fix(str(project_dir))
    if strict:
        result['errors'].extend(result['warnings'])
        result['warnings'] = []
    result['passed'] = len(result['errors']) == 0
    result['project'] = str(project_dir)
    result['timestamp'] = datetime.now().isoformat()
    return result


def run_batch(project_dirs, strict=False, fix=False):
    """Run checks on multiple PBIP projects. Returns list of results."""
    results = []
    from datetime import datetime
    for pdir in project_dirs:
        pdir = Path(pdir)
        if not pdir.exists():
            results.append({
                'project': str(pdir),
                'errors': [f'❌ Project directory not found: {pdir}'],
                'warnings': [], 'info': [], 'fixable': [],
                'passed': False,
                'timestamp': datetime.now().isoformat()
            })
            continue
        if fix:
            r = run_check_and_fix(pdir, strict=strict)
        else:
            r = run_check(pdir, strict=strict)
        results.append(r)
    return results


def format_summary(result):
    """One-line summary string."""
    e = len(result.get('errors', []))
    w = len(result.get('warnings', []))
    f = len(result.get('fixable', []))
    i = len(result.get('info', []))
    status = '✅ PASSED' if result.get('passed') else '❌ FAILED'
    name = Path(result.get('project', '?')).name
    return f'{status} | {name} | {e} errors, {w} warnings, {f} fixable, {i} info'


def format_json(results):
    """JSON output for CI/CD integration."""
    if not isinstance(results, list):
        results = [results]
    output = []
    for r in results:
        output.append({
            'project': r.get('project'),
            'passed': r.get('passed'),
            'errors': r.get('errors', []),
            'warnings': r.get('warnings', []),
            'info': r.get('info', []),
            'fixable_count': len(r.get('fixable', [])),
            'timestamp': r.get('timestamp')
        })
    return json.dumps(output, indent=2, ensure_ascii=False)


def _html_escape(text):
    """Simple HTML escape."""
    return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def generate_html_report(results, output_path):
    """Generate a styled HTML validation report."""
    from datetime import datetime
    if not isinstance(results, list):
        results = [results]

    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en"><head><meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>Power BI PBIP Validation Report</title>',
        '<style>',
        '  * { margin: 0; padding: 0; box-sizing: border-box; }',
        '  body { font-family: "Segoe UI", system-ui, sans-serif; background: #0d1117; color: #c9d1d9; padding: 2rem; }',
        '  .container { max-width: 1000px; margin: 0 auto; }',
        '  h1 { color: #58a6ff; margin-bottom: 0.5rem; font-size: 1.8rem; }',
        '  .subtitle { color: #8b949e; margin-bottom: 2rem; }',
        '  .summary-bar { display: flex; gap: 1rem; margin-bottom: 2rem; flex-wrap: wrap; }',
        '  .stat { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 1rem 1.5rem; min-width: 120px; text-align: center; }',
        '  .stat .value { font-size: 2rem; font-weight: bold; }',
        '  .stat .label { color: #8b949e; font-size: 0.85rem; margin-top: 0.25rem; }',
        '  .stat.errors .value { color: #f85149; }',
        '  .stat.warnings .value { color: #d29922; }',
        '  .stat.info .value { color: #58a6ff; }',
        '  .stat.passed .value { color: #3fb950; }',
        '  .stat.failed .value { color: #f85149; }',
        '  .project { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }',
        '  .project h2 { color: #c9d1d9; font-size: 1.2rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }',
        '  .badge { display: inline-block; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600; }',
        '  .badge.pass { background: #23352a; color: #3fb950; }',
        '  .badge.fail { background: #3d1f20; color: #f85149; }',
        '  .items { list-style: none; }',
        '  .items li { padding: 0.5rem 0.75rem; border-bottom: 1px solid #21262d; font-family: "Cascadia Code", "Fira Code", monospace; font-size: 0.85rem; line-height: 1.5; }',
        '  .items li:last-child { border-bottom: none; }',
        '  .items li.error { color: #f85149; }',
        '  .items li.warning { color: #d29922; }',
        '  .items li.info { color: #58a6ff; }',
        '  .section-title { color: #8b949e; font-size: 0.9rem; font-weight: 600; margin: 1rem 0 0.5rem; text-transform: uppercase; letter-spacing: 0.05em; }',
        '  .footer { text-align: center; color: #484f58; margin-top: 2rem; font-size: 0.8rem; }',
        '</style></head><body>',
        '<div class="container">',
        '<h1>🛡️ Power BI Validation Report</h1>',
        f'<p class="subtitle">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>',
    ]

    total_e = sum(len(r.get('errors', [])) for r in results)
    total_w = sum(len(r.get('warnings', [])) for r in results)
    total_i = sum(len(r.get('info', [])) for r in results)
    total_pass = sum(1 for r in results if r.get('passed'))
    total_fail = len(results) - total_pass

    html_parts.append('<div class="summary-bar">')
    html_parts.append(f'<div class="stat errors"><div class="value">{total_e}</div><div class="label">Errors</div></div>')
    html_parts.append(f'<div class="stat warnings"><div class="value">{total_w}</div><div class="label">Warnings</div></div>')
    html_parts.append(f'<div class="stat info"><div class="value">{total_i}</div><div class="label">Info</div></div>')
    if total_pass > 0:
        html_parts.append(f'<div class="stat passed"><div class="value">{total_pass}</div><div class="label">Passed</div></div>')
    if total_fail > 0:
        html_parts.append(f'<div class="stat failed"><div class="value">{total_fail}</div><div class="label">Failed</div></div>')
    html_parts.append('</div>')

    for r in results:
        name = Path(r.get('project', '?')).name
        passed = r.get('passed', False)
        badge = '<span class="badge pass">✓ PASSED</span>' if passed else '<span class="badge fail">✗ FAILED</span>'
        html_parts.append('<div class="project">')
        html_parts.append(f'<h2>{badge} {name}</h2>')
        errors = r.get('errors', [])
        warnings = r.get('warnings', [])
        infos = r.get('info', [])
        if errors:
            html_parts.append(f'<p class="section-title">Errors ({len(errors)})</p>')
            html_parts.append('<ul class="items">')
            for e in errors:
                html_parts.append(f'<li class="error">{_html_escape(e)}</li>')
            html_parts.append('</ul>')
        if warnings:
            html_parts.append(f'<p class="section-title">Warnings ({len(warnings)})</p>')
            html_parts.append('<ul class="items">')
            for w in warnings:
                html_parts.append(f'<li class="warning">{_html_escape(w)}</li>')
            html_parts.append('</ul>')
        if infos:
            html_parts.append(f'<p class="section-title">Info ({len(infos)})</p>')
            html_parts.append('<ul class="items">')
            for i in infos:
                html_parts.append(f'<li class="info">{_html_escape(i)}</li>')
            html_parts.append('</ul>')
        if not errors and not warnings and not infos:
            html_parts.append('<p style="color:#3fb950;padding:1rem;">✅ No issues found!</p>')
        html_parts.append('</div>')

    html_parts.append('<p class="footer">Power BI PBIP Generator + Checker — Antigravity</p>')
    html_parts.append('</div></body></html>')

    Path(output_path).write_text('\n'.join(html_parts), encoding='utf-8')
    print(f'📄 HTML report saved: {output_path}')
    return output_path


# ─── CLI ───
if __name__ == '__main__':
    import argparse, time as _time

    parser = argparse.ArgumentParser(
        description='🔧 Power BI PBIP Generator + Checker',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate.py data.csv                              # Generate dashboard
  python generate.py data.csv MyDash --verbose --seed 42   # With options
  python generate.py --validate ./MyDashboard              # Validate project
  python generate.py --validate ./MyDash --fix             # Validate + auto-fix
  python generate.py --validate ./MyDash --html report.html # HTML report
  python generate.py --validate ./MyDash --strict          # Strict mode
  python generate.py --validate ./P1 ./P2 --batch          # Batch check
  python generate.py --validate ./MyDash --json            # JSON output
        """
    )
    parser.add_argument('inputs', nargs='*', help='CSV path or project dir(s)')
    parser.add_argument('--validate', action='store_true', help='Run validation mode')
    parser.add_argument('--fix', action='store_true', help='Auto-fix errors')
    parser.add_argument('--strict', action='store_true', help='Treat warnings as errors')
    parser.add_argument('--html', type=str, metavar='FILE', help='Generate HTML report')
    parser.add_argument('--json', action='store_true', dest='json_output', help='JSON output')
    parser.add_argument('--summary', action='store_true', help='Summary only')
    parser.add_argument('--batch', action='store_true', help='Batch mode')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress output')
    parser.add_argument('--verbose', action='store_true', help='Show scoring details')
    parser.add_argument('--seed', type=int, default=None, help='Random seed')

    args = parser.parse_args()

    if not args.inputs:
        parser.print_help()
        sys.exit(1)

    if args.validate:
        # ─── Checker mode ───
        start = _time.time()
        if args.batch or len(args.inputs) > 1:
            results = run_batch(args.inputs, strict=args.strict, fix=args.fix)
        else:
            proj = args.inputs[0]
            if not Path(proj).exists():
                print(f'❌ Project not found: {proj}')
                sys.exit(1)
            if args.fix:
                results = [run_check_and_fix(proj, strict=args.strict)]
            else:
                results = [run_check(proj, strict=args.strict)]

        elapsed = _time.time() - start

        if args.json_output:
            print(format_json(results))
        elif args.summary:
            for r in results:
                print(format_summary(r))
        elif not args.quiet:
            print(f'\n⏱️ Completed in {elapsed:.1f}s')
            if len(results) > 1:
                print(f'\n📊 Batch Summary:')
                for r in results:
                    print(f'  {format_summary(r)}')

        if args.html:
            generate_html_report(results, args.html)

        any_failed = any(not r.get('passed') for r in results)
        sys.exit(1 if any_failed else 0)
    else:
        # ─── Generator mode ───
        auto_generate_dashboard(args.inputs[0],
                                args.inputs[1] if len(args.inputs) > 1 else None,
                                args.inputs[2] if len(args.inputs) > 2 else None,
                                verbose=args.verbose, seed=args.seed)
