#!/usr/bin/env python3
"""Automated tests for generate.py — verifies JSON output structure for all visual generators."""
import json
import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))
import generate as g

PASS = 0
FAIL = 0

def check(name, result, checks):
    """Run checks on a visual container result."""
    global PASS, FAIL
    errors = []
    
    # 1. Must be a dict
    if not isinstance(result, dict):
        errors.append(f'Expected dict, got {type(result).__name__}')
    
    # 2. Must have 'config' key (serialized JSON)
    config_str = result.get('config', '')
    if not config_str:
        errors.append('Missing config key')
    
    # 3. config must be valid JSON
    try:
        cfg = json.loads(config_str) if isinstance(config_str, str) else config_str
    except json.JSONDecodeError as e:
        errors.append(f'Invalid JSON in config: {e}')
        cfg = {}
    
    # 4. Must have 'name' (visual ID)
    if 'name' not in cfg:
        errors.append('Missing name in config')
    
    # 5. Check visualType
    sv = cfg.get('singleVisual', {})
    vtype = sv.get('visualType', '')
    if 'visual_type' in checks:
        if vtype != checks['visual_type']:
            errors.append(f'Expected visualType={checks["visual_type"]}, got {vtype}')
    
    # 6. Check projections exist (if expected)
    if checks.get('has_projections', True):
        proj = sv.get('projections', {})
        if not proj and vtype not in ('textbox', 'shape', 'image', 'qnaVisual', 'annotatedTimeline'):
            errors.append(f'Missing projections for {vtype}')
    
    # 7. Check prototypeQuery exists (if expected)
    if checks.get('has_query', True):
        pq = sv.get('prototypeQuery', {})
        if not pq and vtype not in ('textbox', 'shape', 'image', 'qnaVisual', 'annotatedTimeline'):
            errors.append(f'Missing prototypeQuery for {vtype}')
    
    # 8. Must have layouts with position
    layouts = cfg.get('layouts', [])
    if not layouts:
        errors.append('Missing layouts')
    elif 'position' not in layouts[0]:
        errors.append('Missing position in layout')
    
    # 9. Check position values
    if layouts:
        pos = layouts[0].get('position', {})
        for dim in ['x', 'y', 'width', 'height']:
            if dim not in pos:
                errors.append(f'Missing {dim} in position')
    
    if errors:
        FAIL += 1
        print(f'  ❌ {name}: {"; ".join(errors)}')
    else:
        PASS += 1
        print(f'  ✅ {name}')


def test_all_visuals():
    """Test all visual generator functions."""
    print('\n🧪 Testing Visual Generators\n')
    T = 'Sales'  # test table name
    
    # --- Basic charts ---
    check('make_card', g.make_card(0,0,100,50, T, 'Amount'),
          {'visual_type': 'card'})
    
    check('make_line_chart', g.make_line_chart(0,0,400,300, T, 'Date', 'Amount'),
          {'visual_type': 'lineChart'})
    
    check('make_bar_chart', g.make_bar_chart(0,0,400,300, T, 'Category', 'Amount'),
          {'visual_type': 'clusteredBarChart'})
    
    check('make_column_chart', g.make_column_chart(0,0,400,300, T, 'Category', 'Amount'),
          {'visual_type': 'clusteredColumnChart'})
    
    check('make_combo_chart', g.make_combo_chart(0,0,400,300, T, 'Date', 'Amount', 'Quantity'),
          {'visual_type': 'lineStackedColumnComboChart'})
    
    check('make_donut', g.make_donut(0,0,300,300, T, 'Category', 'Amount'),
          {'visual_type': 'donutChart'})
    
    check('make_treemap', g.make_treemap(0,0,300,300, T, 'Category', 'Amount'),
          {'visual_type': 'treemap'})
    
    check('make_gauge', g.make_gauge(0,0,200,200, T, 'Score', target_val=80),
          {'visual_type': 'gauge'})
    
    check('make_table', g.make_table(0,0,600,400, T, ['Date','Product','Amount']),
          {'visual_type': 'tableEx'})
    
    check('make_scatter', g.make_scatter(0,0,400,300, T, 'Price', 'Quantity', detail_col='Category'),
          {'visual_type': 'scatterChart'})
    
    check('make_funnel', g.make_funnel(0,0,300,300, T, 'Stage', 'Count'),
          {'visual_type': 'funnelChart'})
    
    check('make_waterfall', g.make_waterfall(0,0,400,300, T, 'Category', 'Amount'),
          {'visual_type': 'waterfallChart'})
    
    check('make_slicer', g.make_slicer(0,0,200,50, T, 'Region'),
          {'visual_type': 'slicer'})
    
    check('make_area_chart', g.make_area_chart(0,0,400,300, T, 'Date', 'Amount'),
          {'visual_type': 'areaChart'})
    
    check('make_matrix', g.make_matrix(0,0,600,400, T, ['Region'], 'Quarter', 'Amount'),
          {'visual_type': 'pivotTable'})
    
    # --- New visuals (round 1) ---
    check('make_kpi', g.make_kpi(0,0,200,100, T, 'Revenue', 'Target', 'Date'),
          {'visual_type': 'kpi'})
    
    check('make_pie_chart', g.make_pie_chart(0,0,300,300, T, 'Category', 'Amount'),
          {'visual_type': 'pieChart'})
    
    check('make_ribbon_chart', g.make_ribbon_chart(0,0,400,300, T, 'Date', 'Category', 'Amount'),
          {'visual_type': 'ribbonChart'})
    
    check('make_multi_row_card', g.make_multi_row_card(0,0,400,200, T, ['Revenue', 'Cost', 'Profit']),
          {'visual_type': 'multiRowCard'})
    
    check('make_stacked_area', g.make_stacked_area(0,0,400,300, T, 'Date', 'Category', 'Amount'),
          {'visual_type': 'stackedAreaChart'})
    
    check('make_hundred_pct_bar', g.make_hundred_pct_bar(0,0,400,300, T, 'Category', 'Region', 'Amount'),
          {'visual_type': 'hundredPercentStackedBarChart'})
    
    check('make_textbox', g.make_textbox(0,0,300,50, 'Hello World', 16),
          {'visual_type': 'textbox', 'has_projections': False, 'has_query': False})
    
    check('make_shape', g.make_shape(0,0,200,100, 'rectangle', '#FF0000'),
          {'visual_type': 'shape', 'has_projections': False, 'has_query': False})
    
    check('make_image', g.make_image(0,0,200,150, 'https://example.com/logo.png'),
          {'visual_type': 'image', 'has_projections': False, 'has_query': False})
    
    check('make_map', g.make_map(0,0,400,300, T, 'City', 'Amount'),
          {'visual_type': 'map'})
    
    check('make_filled_map', g.make_filled_map(0,0,400,300, T, 'Country', 'Sales'),
          {'visual_type': 'filledMap'})
    
    # --- New visuals (round 2) ---
    check('make_decomposition_tree', g.make_decomposition_tree(0,0,600,400, T, 'Revenue', ['Region','Product','Channel']),
          {'visual_type': 'decompositionTreeVisual'})
    
    check('make_key_influencers', g.make_key_influencers(0,0,600,400, T, 'Churn', ['Age','Plan','Usage']),
          {'visual_type': 'keyDriversVisual'})
    
    check('make_qna', g.make_qna(0,0,400,200, 'What is total sales?'),
          {'visual_type': 'qnaVisual', 'has_projections': False, 'has_query': False})
    
    check('make_shape_map', g.make_shape_map(0,0,400,300, T, 'State', 'Population'),
          {'visual_type': 'shapeMap'})
    
    check('make_azure_map', g.make_azure_map(0,0,400,300, T, 'City', 'Revenue'),
          {'visual_type': 'azureMap'})
    
    check('make_stacked_bar', g.make_stacked_bar(0,0,400,300, T, 'Product', 'Region', 'Sales'),
          {'visual_type': 'stackedBarChart'})
    
    check('make_stacked_column', g.make_stacked_column(0,0,400,300, T, 'Month', 'Category', 'Revenue'),
          {'visual_type': 'stackedColumnChart'})
    
    check('make_hundred_pct_column', g.make_hundred_pct_column(0,0,400,300, T, 'Month', 'Type', 'Amount'),
          {'visual_type': 'hundredPercentStackedColumnChart'})
    
    check('make_hundred_pct_area', g.make_hundred_pct_area(0,0,400,300, T, 'Date', 'Channel', 'Revenue'),
          {'visual_type': 'hundredPercentStackedAreaChart'})
    
    check('make_clustered_column', g.make_clustered_column(0,0,400,300, T, 'Product', 'Sales'),
          {'visual_type': 'clusteredColumnChart'})
    
    check('make_line_clustered_combo', g.make_line_clustered_combo(0,0,400,300, T, 'Date', 'Revenue', 'Margin'),
          {'visual_type': 'lineClusteredColumnComboChart'})
    
    check('make_line_stacked_combo', g.make_line_stacked_combo(0,0,400,300, T, 'Date', 'Revenue', 'Margin', 'Region'),
          {'visual_type': 'lineStackedColumnComboChart'})
    
    check('make_smart_narrative', g.make_smart_narrative(0,0,400,200),
          {'visual_type': 'annotatedTimeline', 'has_projections': False, 'has_query': False})
    
    check('make_paginated_table', g.make_paginated_table(0,0,600,400, T, ['ID','Name','Amount']),
          {'visual_type': 'tableEx'})
    
    check('make_card_with_states', g.make_card_with_states(0,0,150,80, T, 'Score', target=80),
          {'visual_type': 'card'})
    
    check('make_r_script', g.make_r_script(0,0,400,300, T, ['X','Y'], 'plot(dataset$X, dataset$Y)'),
          {'visual_type': 'scriptVisual'})
    
    check('make_python_script', g.make_python_script(0,0,400,300, T, ['X','Y'], 'import matplotlib'),
          {'visual_type': 'scriptVisual'})


def test_utilities():
    """Test utility functions."""
    print('\n🔧 Testing Utilities\n')
    global PASS, FAIL
    
    # Test model builder
    try:
        model = g.make_model_bim('TestProject', [
            {'name': 'Sales', 'columns': [
                {'name': 'Amount', 'dataType': 'double', 'sourceColumn': 'Amount'},
                {'name': 'Date', 'dataType': 'dateTime', 'sourceColumn': 'Date'},
            ], 'measures': [
                {'name': 'Total', 'expression': 'SUM(Sales[Amount])'}
            ], 'partition_m': 'let Source = #table({"Amount","Date"},{}) in Source'}
        ], relationships=[{'from_table': 'Sales', 'from_col': 'Date', 'to_table': 'Calendar', 'to_col': 'Date'}])
        if model.get('compatibilityLevel') and model.get('model', {}).get('tables'):
             PASS += 1
             print('  ✅ make_model_bim')
        else:
             FAIL += 1
             print('  ❌ make_model_bim: invalid structure')
    except Exception as e:
        FAIL += 1
        print(f'  ❌ make_model_bim: {e}')
    
    # Test report builder
    try:
        visuals = [g.make_card(0,0,100,50, 'Sales', 'Amount')]
        report = g.make_report_json([{'name': 'Overview', 'visuals': visuals}])
        sections = report.get('sections', [])
        if sections and 'visualContainers' in sections[0]:
            PASS += 1
            print('  ✅ make_report_json')
        else:
            FAIL += 1
            print('  ❌ make_report_json: missing sections/visualContainers')
    except Exception as e:
        FAIL += 1
        print(f'  ❌ make_report_json: {e}')
    
    # Test theme builder
    try:
        theme = g.make_custom_theme('TestTheme', '#1B2A4A', '#E8344E')
        if theme.get('name') == 'TestTheme' and 'dataColors' in theme:
            PASS += 1
            print('  ✅ make_custom_theme')
        else:
            FAIL += 1
            print('  ❌ make_custom_theme: invalid structure')
    except Exception as e:
        FAIL += 1
        print(f'  ❌ make_custom_theme: {e}')
    
    # Test add_bookmark
    try:
        bm = g.make_bookmark('BM1', 'Page1', {'Visual1': True})
        if bm.get('name') == 'BM1' and 'explorationState' in bm:
            PASS += 1
            print('  ✅ make_bookmark')
        else:
            FAIL += 1
            print('  ❌ make_bookmark: invalid structure')
    except Exception as e:
        FAIL += 1
        print(f'  ❌ make_bookmark: {e}')
    
    # Test filter functions
    try:
        vc = g.make_card(0,0,100,50, 'Sales', 'Amount')
        g.add_topn_filter(vc, 'Sales', 'Amount', 0, 10)
        filters = json.loads(vc.get('filters', '[]'))
        if filters and filters[0].get('type') == 'TopN':
            PASS += 1
            print('  ✅ add_topn_filter')
        else:
            FAIL += 1
            print('  ❌ add_topn_filter: invalid filter')
    except Exception as e:
        FAIL += 1
        print(f'  ❌ add_topn_filter: {e}')


def test_json_serialization():
    """Test that all outputs are JSON-serializable."""
    print('\n📋 Testing JSON Serialization\n')
    global PASS, FAIL
    T = 'Test'
    
    all_visuals = [
        ('card', g.make_card(0,0,100,50,T,'A')),
        ('line', g.make_line_chart(0,0,400,300,T,'X','Y')),
        ('kpi', g.make_kpi(0,0,200,100,T,'V','T','D')),
        ('textbox', g.make_textbox(0,0,200,50,'Hi')),
        ('shape', g.make_shape(0,0,100,100)),
        ('image', g.make_image(0,0,100,100)),
        ('qna', g.make_qna(0,0,300,200)),
        ('decomp', g.make_decomposition_tree(0,0,600,400,T,'V',['A','B'])),
    ]
    
    for name, visual in all_visuals:
        try:
            json.dumps(visual)
            PASS += 1
            print(f'  ✅ {name} serializable')
        except (TypeError, ValueError) as e:
            FAIL += 1
            print(f'  ❌ {name} not serializable: {e}')


def test_data_cleaning():
    """Test the data cleaning engine functions."""
    print('\n🧹 Testing Data Cleaning Engine\n')
    global PASS, FAIL
    import tempfile, csv, os

    # ── Helper: write a temp CSV and return path ──
    def _make_csv(headers, rows, encoding='utf-8'):
        f = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False,
                                         newline='', encoding=encoding)
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)
        f.close()
        return f.name

    def _read_csv(path):
        """Read CSV file and return list of rows (including header)."""
        import csv
        with open(path, 'r', encoding='utf-8') as f:
            return list(csv.reader(f))

    # ── 1. Null Standardization ──
    try:
        path = _make_csv(['A', 'B'], [['hello', 'N/A'], ['world', 'null'], ['test', '-']])
        _, report = g.clean_csv(path, config={'standardize_nulls': True, 'remove_duplicates': False, 'remove_empty_rows': False})
        if report['nulls_standardized'] >= 3:
            PASS += 1; print('  ✅ null standardization')
        else:
            FAIL += 1; print(f'  ❌ null standardization: expected ≥3, got {report["nulls_standardized"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ null standardization: {e}')

    # ── 2. Text Cleaning (BOM, whitespace, control chars) ──
    try:
        path = _make_csv(['\ufeffName', 'Value'],
                         [[' hello\u200b ', '  extra   spaces  '], ['\ttab\there', 'ok']])
        _, report = g.clean_csv(path, config={'remove_duplicates': False, 'remove_empty_rows': False})
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if report['text_cells_cleaned'] > 0 and '\ufeff' not in content and '\u200b' not in content:
            PASS += 1; print('  ✅ text cleaning (BOM, whitespace, control chars)')
        else:
            FAIL += 1; print(f'  ❌ text cleaning: cleaned={report["text_cells_cleaned"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ text cleaning: {e}')

    # ── 3. Numeric Cleaning (currency, thousands, parens, pct) ──
    try:
        path = _make_csv(['Amount'], [['$1,000.50'], ['(200)'], ['€3.500,25'], ['50%']])
        _, report = g.clean_csv(path, config={'remove_duplicates': False, 'remove_empty_rows': False})
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        vals = [r[0] for r in rows[1:]]
        ok = ('$' not in vals[0] and ',' not in vals[0]  # currency + thousands removed
              and vals[1].startswith('-'))                # parens → negative
        if ok and report['numbers_cleaned'] > 0:
            PASS += 1; print('  ✅ numeric cleaning (currency, thousands, parens)')
        else:
            FAIL += 1; print(f'  ❌ numeric cleaning: vals={vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ numeric cleaning: {e}')

    # ── 4. Date Parsing ──
    try:
        path = _make_csv(['DateCol'], [['2024-01-15'], ['15/06/2024'], ['Jan 20, 2024']])
        _, report = g.clean_csv(path, config={
            'fix_dates': True, 'date_columns': ['DateCol'],
            'remove_duplicates': False, 'remove_empty_rows': False
        })
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        vals = [r[0] for r in rows[1:]]
        if all(v.startswith('20') and '-' in v for v in vals):
            PASS += 1; print('  ✅ date parsing (ISO output)')
        else:
            FAIL += 1; print(f'  ❌ date parsing: vals={vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ date parsing: {e}')

    # ── 5. Boolean Standardization ──
    try:
        path = _make_csv(['Active'], [['yes'], ['No'], ['Y'], ['FALSE'], ['1']])
        _, report = g.clean_csv(path, config={
            'standardize_booleans': True,
            'remove_duplicates': False, 'remove_empty_rows': False
        })
        if report['booleans_standardized'] >= 4:
            PASS += 1; print('  ✅ boolean standardization')
        else:
            FAIL += 1; print(f'  ❌ boolean standardization: got {report["booleans_standardized"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ boolean standardization: {e}')

    # ── 6. Duplicate Removal ──
    try:
        path = _make_csv(['X', 'Y'], [['a', '1'], ['b', '2'], ['a', '1'], ['c', '3'], ['b', '2']])
        _, report = g.clean_csv(path, config={'remove_duplicates': True, 'remove_empty_rows': False})
        if report['duplicates_removed'] == 2 and report['output_rows'] == 3:
            PASS += 1; print('  ✅ duplicate removal')
        else:
            FAIL += 1; print(f'  ❌ duplicate removal: removed={report["duplicates_removed"]}, rows={report["output_rows"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ duplicate removal: {e}')

    # ── 7. Empty Row Removal ──
    try:
        path = _make_csv(['A', 'B'], [['x', 'y'], ['', ''], ['z', 'w'], ['  ', '   ']])
        _, report = g.clean_csv(path, config={'remove_empty_rows': True, 'remove_duplicates': False})
        if report['output_rows'] == 2:
            PASS += 1; print('  ✅ empty row removal')
        else:
            FAIL += 1; print(f'  ❌ empty row removal: output_rows={report["output_rows"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ empty row removal: {e}')

    # ── 8. Outlier Detection (IQR) ──
    try:
        path = _make_csv(['Score'], [[str(x)] for x in [10, 12, 11, 13, 12, 11, 10, 100, 9, 12]])
        _, report = g.clean_csv(path, config={
            'remove_outliers': True, 'outlier_method': 'iqr', 'outlier_action': 'remove',
            'remove_duplicates': False, 'remove_empty_rows': False
        })
        if report['outliers_handled'] >= 1 and report['output_rows'] < 10:
            PASS += 1; print('  ✅ outlier detection (IQR)')
        else:
            FAIL += 1; print(f'  ❌ outlier detection: handled={report["outliers_handled"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ outlier detection: {e}')

    # ── 9. Forward Fill ──
    try:
        path = _make_csv(['Cat', 'Val'], [['A', '1'], ['', '2'], ['', '3'], ['B', '4'], ['', '5']])
        _, report = g.clean_csv(path, config={
            'null_fill_strategy': 'forward', 'null_fill_columns': ['Cat'],
            'remove_duplicates': False, 'remove_empty_rows': False, 'standardize_nulls': False
        })
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        cats = [r[0] for r in rows[1:]]
        if cats == ['A', 'A', 'A', 'B', 'B']:
            PASS += 1; print('  ✅ forward fill')
        else:
            FAIL += 1; print(f'  ❌ forward fill: cats={cats}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ forward fill: {e}')

    # ── 10. Column Removal (high-null) ──
    try:
        path = _make_csv(['A', 'B', 'C'], [['1', '', ''], ['2', '', ''], ['3', '', 'x']])
        _, report = g.clean_csv(path, config={
            'remove_columns_pct': 0.6, 'remove_duplicates': False, 'remove_empty_rows': False
        })
        if 'B' in report['columns_removed'] and report['output_cols'] < 3:
            PASS += 1; print('  ✅ high-null column removal')
        else:
            FAIL += 1; print(f'  ❌ column removal: removed={report["columns_removed"]}, out_cols={report["output_cols"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ column removal: {e}')

    # ── 11. Validation Warnings ──
    try:
        path = _make_csv(['email', 'phone'], [['bad@', '12345'], ['ok@example.com', '+1-555-1234567']])
        _, report = g.clean_csv(path, config={
            'validate_emails': True, 'validate_phones': True,
            'remove_duplicates': False, 'remove_empty_rows': False
        })
        if len(report['validation_warnings']) > 0:
            PASS += 1; print('  ✅ validation warnings (email/phone)')
        else:
            FAIL += 1; print(f'  ❌ validation warnings: got {report["validation_warnings"]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ validation warnings: {e}')

    # ── 12. Column Type Detection ──
    try:
        path = _make_csv(['Num', 'Text', 'Bool'],
                         [['100', 'hello', 'yes'], ['200', 'world', 'no'], ['300', 'foo', 'y']])
        _, report = g.clean_csv(path, config={'remove_duplicates': False, 'remove_empty_rows': False})
        types = report['column_types']
        if types.get('Num') == 'numeric':
            PASS += 1; print('  ✅ column type detection')
        else:
            FAIL += 1; print(f'  ❌ column type detection: types={types}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ column type detection: {e}')

    # ── 13. M Cleaning Steps Generation ──
    try:
        cols = [{'name': 'Name', 'type': 'string'}, {'name': 'Amount', 'type': 'number'}]
        steps, last = g.build_m_cleaning_steps(cols, config={
            'remove_duplicates': True, 'remove_empty_rows': True,
            'trim_text': True, 'clean_text': True, 'error_handling': True,
        })
        if (len(steps) >= 3
            and any('Table.Distinct' in s for s in steps)
            and any('Table.TransformColumns' in s for s in steps)
            and any('ErrorsHandled' in s for s in steps)):
            PASS += 1; print('  ✅ M cleaning steps generation')
        else:
            FAIL += 1; print(f'  ❌ M cleaning steps: {len(steps)} steps, last={last}')
    except Exception as e:
        FAIL += 1; print(f'  ❌ M cleaning steps: {e}')

    # ── 14. Case Standardization ──
    try:
        path = _make_csv(['Name'], [['john doe'], ['JANE DOE'], ['Bob Smith']])
        _, report = g.clean_csv(path, config={
            'case_mode': 'upper', 'remove_duplicates': False, 'remove_empty_rows': False
        })
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        vals = [r[0] for r in rows[1:]]
        if all(v == v.upper() for v in vals):
            PASS += 1; print('  ✅ case standardization (upper)')
        else:
            FAIL += 1; print(f'  ❌ case standardization: vals={vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ case standardization: {e}')

    # ── 15. Clean Report Structure ──
    try:
        path = _make_csv(['X'], [['1'], ['2']])
        _, report = g.clean_csv(path, config={'remove_duplicates': False, 'remove_empty_rows': False})
        required_keys = ['input_rows', 'output_rows', 'input_cols', 'output_cols',
                         'nulls_standardized', 'duplicates_removed', 'column_types']
        if all(k in report for k in required_keys):
            PASS += 1; print('  ✅ cleaning report structure')
        else:
            missing = [k for k in required_keys if k not in report]
            FAIL += 1; print(f'  ❌ cleaning report: missing keys {missing}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  ❌ cleaning report: {e}')

    # ══════════════════════════════════════════
    # Phase 2 Tests
    # ══════════════════════════════════════════

    # ── 16. Diacritics removal ──
    try:
        path = _make_csv(['Name'], [['caf\u00e9'], ['na\u00efve'], ['r\u00e9sum\u00e9']])
        _, report = g.clean_csv(path, config={'remove_diacritics': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if vals == ['cafe', 'naive', 'resume']:
            PASS += 1; print('  \u2705 diacritics removal')
        else:
            FAIL += 1; print(f'  \u274c diacritics: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c diacritics: {e}')

    # ── 17. Emoji removal ──
    try:
        path = _make_csv(['Text'], [['Hello \U0001f600 World'], ['Good \u2764\ufe0f']])
        _, report = g.clean_csv(path, config={'remove_emoji': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        v0 = rows[1][0].strip()
        if 'Hello' in v0 and 'World' in v0 and '\U0001f600' not in v0:
            PASS += 1; print('  \u2705 emoji removal')
        else:
            FAIL += 1; print(f'  \u274c emoji: got {v0!r}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c emoji: {e}')

    # ── 18. PII masking ──
    try:
        path = _make_csv(['Data'], [['My SSN is 123-45-6789']])
        _, report = g.clean_csv(path, config={'mask_pii': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        v = rows[1][0]
        if '123-45-6789' not in v and '***' in v:
            PASS += 1; print('  \u2705 PII masking')
        else:
            FAIL += 1; print(f'  \u274c PII: got {v!r}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c PII: {e}')

    # ── 19. Email privacy masking ──
    try:
        path = _make_csv(['Email'], [['john.doe@example.com']])
        _, report = g.clean_csv(path, config={'mask_emails_privacy': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        v = rows[1][0]
        if v.startswith('j') and '@example.com' in v and '*' in v:
            PASS += 1; print('  \u2705 email privacy masking')
        else:
            FAIL += 1; print(f'  \u274c email mask: got {v!r}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c email mask: {e}')

    # ── 20. Full-width -> half-width ──
    try:
        path = _make_csv(['Text'], [['\uff21\uff22\uff23\uff11\uff12\uff13']])
        _, report = g.clean_csv(path, config={'fix_fullwidth': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        v = rows[1][0].strip()
        if v == 'ABC123':
            PASS += 1; print('  \u2705 full-width conversion')
        else:
            FAIL += 1; print(f'  \u274c fullwidth: got {v!r}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fullwidth: {e}')

    # ── 21. Fraction conversion ──
    try:
        path = _make_csv(['Amount'], [['\u00bd'], ['\u00be'], ['1/4']])
        _, report = g.clean_csv(path, config={'fix_fractions': True, 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0].strip() for r in rows[1:]]
        if vals[0] == '0.5' and vals[1] == '0.75' and vals[2] == '0.25':
            PASS += 1; print('  \u2705 fraction conversion')
        else:
            FAIL += 1; print(f'  \u274c fractions: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fractions: {e}')

    # ── 22. String padding ──
    try:
        path = _make_csv(['zip'], [['123'], ['4567'], ['89']])
        _, report = g.clean_csv(path, config={'pad_columns': {'zip': (5, '0', 'left')}, 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if vals == ['00123', '04567', '00089']:
            PASS += 1; print('  \u2705 string padding')
        else:
            FAIL += 1; print(f'  \u274c padding: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c padding: {e}')

    # ── 23. Rounding ──
    try:
        path = _make_csv(['Value'], [['3.14159'], ['2.71828']])
        _, report = g.clean_csv(path, config={'round_decimals': 2, 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if vals == ['3.14', '2.72']:
            PASS += 1; print('  \u2705 rounding')
        else:
            FAIL += 1; print(f'  \u274c rounding: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c rounding: {e}')

    # ── 24. Clamping ──
    try:
        path = _make_csv(['Score'], [['150'], ['50'], ['-10']])
        _, report = g.clean_csv(path, config={'clamp_ranges': {'Score': (0, 100)}, 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if float(vals[0]) == 100 and float(vals[1]) == 50 and float(vals[2]) == 0:
            PASS += 1; print('  \u2705 clamping')
        else:
            FAIL += 1; print(f'  \u274c clamping: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c clamping: {e}')

    # ── 25. Phone normalization ──
    try:
        path = _make_csv(['Phone'], [['(555) 123-4567'], ['555.987.6543']])
        _, report = g.clean_csv(path, config={'normalize_phones': True, 'phone_country_code': '+1', 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if all(v.startswith('+1') for v in vals):
            PASS += 1; print('  \u2705 phone normalization')
        else:
            FAIL += 1; print(f'  \u274c phone: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c phone: {e}')

    # ── 26. Postal code formatting ──
    try:
        path = _make_csv(['zip'], [['123'], ['1234'], ['90210']])
        _, report = g.clean_csv(path, config={'format_postal_codes': 'US', 'remove_duplicates': False})
        rows = _read_csv(path)
        vals = [r[0] for r in rows[1:]]
        if vals[0] == '00123' and vals[1] == '01234' and vals[2] == '90210':
            PASS += 1; print('  \u2705 postal code formatting')
        else:
            FAIL += 1; print(f'  \u274c postal: got {vals}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c postal: {e}')

    # ── 27. Fuzzy deduplication ──
    try:
        path = _make_csv(['Name', 'Value'], [['John Smith', '100'], ['Jon Smith', '100'], ['Jane Doe', '200']])
        _, report = g.clean_csv(path, config={'fuzzy_dedup': True, 'fuzzy_dedup_threshold': 0.8, 'remove_duplicates': False})
        rows = _read_csv(path)
        if len(rows) == 3:  # header + 2 unique (John & Jon are fuzzy dupes)
            PASS += 1; print('  \u2705 fuzzy deduplication')
        else:
            FAIL += 1; print(f'  \u274c fuzzy dedup: expected 3 rows, got {len(rows)}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fuzzy dedup: {e}')

    # ═══════════════════════════════════════════════════
    # PHASE 3 TESTS: Messy Data Handling
    # ═══════════════════════════════════════════════════

    # ── 28. Fix column count ──
    try:
        path = _make_csv(['Name', 'Age', 'City'], [
            ['Alice', '30', 'NYC', 'extra'],  # too many columns
            ['Bob', '25'],                     # too few columns
        ])
        _, report = g.clean_csv(path, config={'fix_column_count': True})
        rows = _read_csv(path)
        # CSV reader normalizes row length at read time; verify output has correct column count
        if all(len(r) == 3 for r in rows[1:]):
            PASS += 1; print('  \u2705 fix column count')
        else:
            FAIL += 1; print(f'  \u274c fix column count: rows have inconsistent columns')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fix column count: {e}')

    # ── 29. Fix quoted strings ──
    try:
        path = _make_csv(['Name', 'Value'], [
            ['"Alice"', '"100"'],
            ["'Bob'", "'200'"],
        ])
        _, report = g.clean_csv(path, config={'fix_quoted_strings': True})
        rows = _read_csv(path)
        if report.get('quotes_fixed', 0) >= 2:
            PASS += 1; print('  \u2705 fix quoted strings')
        else:
            FAIL += 1; print(f'  \u274c fix quoted strings: {report.get("quotes_fixed")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fix quoted strings: {e}')

    # ── 30. Split multi-value cells ──
    try:
        path = _make_csv(['Name', 'Tags'], [
            ['Alice', 'red;blue;green'],
            ['Bob', 'yellow'],
        ])
        _, report = g.clean_csv(path, config={'split_multi_value': {'Tags': ';'}})
        rows = _read_csv(path)
        if len(rows) == 5:  # header + 3 (Alice split) + 1 (Bob)
            PASS += 1; print('  \u2705 split multi-value')
        else:
            FAIL += 1; print(f'  \u274c split multi-value: expected 5 rows, got {len(rows)}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c split multi-value: {e}')

    # ── 31. Column splitting ──
    try:
        path = _make_csv(['Full Name', 'Age'], [
            ['John Smith', '30'],
            ['Jane Doe', '25'],
        ])
        _, report = g.clean_csv(path, config={'split_columns': {'Full Name': (' ', ['First', 'Last'])}})
        rows = _read_csv(path)
        if len(rows[0]) >= 4 and report.get('columns_split', 0) >= 1:  # Original 2 + 2 new
            PASS += 1; print('  \u2705 column splitting')
        else:
            FAIL += 1; print(f'  \u274c column splitting: cols={len(rows[0])}, split={report.get("columns_split")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c column splitting: {e}')

    # ── 32. Extract numbers ──
    try:
        path = _make_csv(['Product', 'Weight'], [
            ['Apple', 'weighs 2.5 kg'],
            ['Banana', 'about 150 grams'],
        ])
        _, report = g.clean_csv(path, config={'extract_numbers': ['Weight']})
        rows = _read_csv(path)
        if rows[1][1] == '2.5' and rows[2][1] == '150':
            PASS += 1; print('  \u2705 extract numbers')
        else:
            FAIL += 1; print(f'  \u274c extract numbers: got {rows[1][1]}, {rows[2][1]}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c extract numbers: {e}')

    # ── 33. Compress repeated chars ──
    try:
        path = _make_csv(['Text'], [
            ['helloooo'],
            ['yesssss'],
        ])
        _, report = g.clean_csv(path, config={'compress_repeated_chars': True})
        rows = _read_csv(path)
        if report.get('chars_compressed', 0) >= 2:
            PASS += 1; print('  \u2705 compress repeated chars')
        else:
            FAIL += 1; print(f'  \u274c compress repeated chars: {report.get("chars_compressed")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c compress repeated chars: {e}')

    # ── 34. Strip honorifics ──
    try:
        path = _make_csv(['Customer Name', 'Age'], [
            ['Mr. John Smith', '30'],
            ['Dr. Jane Doe', '40'],
        ])
        _, report = g.clean_csv(path, config={'strip_honorifics': True})
        rows = _read_csv(path)
        if report.get('honorifics_stripped', 0) >= 2:
            PASS += 1; print('  \u2705 strip honorifics')
        else:
            FAIL += 1; print(f'  \u274c strip honorifics: {report.get("honorifics_stripped")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c strip honorifics: {e}')

    # ── 35. Expand abbreviations ──
    try:
        path = _make_csv(['Address'], [
            ['123 Main St.'],
            ['456 Oak Ave.'],
        ])
        _, report = g.clean_csv(path, config={'expand_abbreviations': True})
        rows = _read_csv(path)
        if report.get('abbreviations_expanded', 0) >= 2:
            PASS += 1; print('  \u2705 expand abbreviations')
        else:
            FAIL += 1; print(f'  \u274c expand abbreviations: {report.get("abbreviations_expanded")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c expand abbreviations: {e}')

    # ── 36. Fix mixed case ──
    try:
        path = _make_csv(['Name'], [
            ['jOhN sMiTh'],
            ['jAnE dOe'],
        ])
        _, report = g.clean_csv(path, config={'fix_mixed_case': True})
        rows = _read_csv(path)
        if report.get('mixed_case_fixed', 0) >= 2:
            PASS += 1; print('  \u2705 fix mixed case')
        else:
            FAIL += 1; print(f'  \u274c fix mixed case: {report.get("mixed_case_fixed")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c fix mixed case: {e}')

    # ── 37. Standardize gender ──
    try:
        path = _make_csv(['Name', 'Gender'], [
            ['Alice', 'Female'],
            ['Bob', 'male'],
            ['Carol', 'F'],
        ])
        _, report = g.clean_csv(path, config={'standardize_gender': True})
        rows = _read_csv(path)
        if report.get('genders_standardized', 0) >= 2:  # Female→F, male→M
            PASS += 1; print('  \u2705 standardize gender')
        else:
            FAIL += 1; print(f'  \u274c standardize gender: {report.get("genders_standardized")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c standardize gender: {e}')

    # ── 38. Unit conversion ──
    try:
        path = _make_csv(['Product', 'Weight'], [
            ['Apple', '1'],
            ['Banana', '2.5'],
        ])
        _, report = g.clean_csv(path, config={'convert_units': {'Weight': ('kg', 'lbs')}})
        rows = _read_csv(path)
        if report.get('units_converted', 0) >= 2:
            PASS += 1; print('  \u2705 unit conversion')
        else:
            FAIL += 1; print(f'  \u274c unit conversion: {report.get("units_converted")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c unit conversion: {e}')

    # ── 39. Normalize spelling ──
    try:
        path = _make_csv(['Description'], [
            ['The colour is beautiful'],
            ['My favourite organisation'],
        ])
        _, report = g.clean_csv(path, config={'normalize_spelling': True})
        rows = _read_csv(path)
        if report.get('spellings_normalized', 0) >= 2:
            PASS += 1; print('  \u2705 normalize spelling')
        else:
            FAIL += 1; print(f'  \u274c normalize spelling: {report.get("spellings_normalized")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c normalize spelling: {e}')

    # ── 40. Parse durations ──
    try:
        path = _make_csv(['Task', 'Duration'], [
            ['Meeting', '2h30m'],
            ['Lunch', '1:30'],
            ['Call', '90 minutes'],
        ])
        _, report = g.clean_csv(path, config={'parse_durations': ['Duration']})
        rows = _read_csv(path)
        if report.get('durations_parsed', 0) >= 3:
            PASS += 1; print('  \u2705 parse durations')
        else:
            FAIL += 1; print(f'  \u274c parse durations: {report.get("durations_parsed")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c parse durations: {e}')

    # ── 41. Consolidate categories ──
    try:
        path = _make_csv(['City'], [
            ['NYC'],
            ['New York City'],
            ['N.Y.C.'],
        ])
        _, report = g.clean_csv(path, config={'consolidate_categories': {'City': {'NYC': 'New York', 'New York City': 'New York', 'N.Y.C.': 'New York'}}})
        rows = _read_csv(path)
        if report.get('categories_consolidated', 0) >= 3:
            PASS += 1; print('  \u2705 consolidate categories')
        else:
            FAIL += 1; print(f'  \u274c consolidate categories: {report.get("categories_consolidated")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c consolidate categories: {e}')

    # ── 42. Smart dedup (merge) ──
    try:
        path = _make_csv(['Name', 'Email', 'Phone'], [
            ['John', 'john@test.com', ''],
            ['John', '', '555-1234'],
        ])
        _, report = g.clean_csv(path, config={'smart_dedup': True, 'smart_dedup_columns': ['Name'], 'remove_duplicates': False})
        rows = _read_csv(path)
        if len(rows) == 2 and report.get('smart_dupes_merged', 0) >= 1:  # header + 1 merged
            PASS += 1; print('  \u2705 smart dedup merge')
        else:
            FAIL += 1; print(f'  \u274c smart dedup: rows={len(rows)}, merged={report.get("smart_dupes_merged")}')
        os.unlink(path)
    except Exception as e:
        FAIL += 1; print(f'  \u274c smart dedup: {e}')


if __name__ == '__main__':
    print('='*60)
    print('  Power BI generate.py — Automated Test Suite')
    print('='*60)
    
    test_all_visuals()
    test_utilities()
    test_json_serialization()
    test_data_cleaning()
    
    print(f'\n{"="*60}')
    total = PASS + FAIL
    print(f'  Results: {PASS}/{total} passed, {FAIL} failed')
    print(f'{"="*60}\n')
    
    sys.exit(1 if FAIL > 0 else 0)
