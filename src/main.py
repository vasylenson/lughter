#!/usr/bin/python3

from argparse import ArgumentParser, Namespace
from pathlib import Path
from pandas import DataFrame, ExcelWriter, read_csv

from config import COOLING, HEATING, T_PRI_RET_LOWER, T_PRI_RET_UPPER, T_PRI_SUP_LOWER, T_PRI_SUP_UPPER, T_SEC_RET_LOWER, T_SEC_RET_UPPER, T_SEC_SUP_LOWER, T_SEC_SUP_UPPER

DEBUG_MODE = True

USE_COLS = {
    'Datum',
    'Tijd',
    '6/Anal1 - 1: Impuls',
    # '6/Anal2',
    # '6/Anal3 - 3: Storing',
    '6/Anal4 - 4: koelbedrijf',
    # '6/Anal5 - 5: T.warmtep.aanv',
    # '6/Anal6 - 6: T.warmtep.ret',
    # '6/Anal7',
    '6/Anal8 - 11: T.sec.sup',
    '6/Anal9 - 12: T.sec.ret.',
    '6/Anal10 - 1: T.pri.sup',
    '6/Anal11 - 2: T.pri.ret',
    # '6/Anal12 - 4: P.well.pump',
    '6/Anal13 - 18: Status.well.pump',
    '6/Anal14 - 19: Alarm.well.pump',
    '6/Anal15 - 20: Status.heat.pump',
    '6/Anal16 - 21: Alarm.heat.pump',
    # '6/Anal17 - 3: p.prim.top.WHEx',
    '6/Anal18 - 13: Flow.heat.pump',
    # '6/Anal19 - 7: Impulsteller Tellerstand va',
    # '6/Anal20 - 7: RV.buiten',
    # '6/Anal21 - 8: T.buiten',
    # '6/Anal22 - 9: Dauwpunt.buiten',
    # '6/Anal23 - 10: SV.buiten',
    # '6/Anal24 - 7: Impulsteller Totale tellers',
    '6/Anal25 - 9: Sample & Hold Uitkomst',
    # '6/Anal26 - 5: Warmtemeting 1 Vermogen',
    # '6/Anal27 - 5: Warmtemeting 1 Tellerstand ',
    # '6/Anal28 - 5: Warmtemeting 1 Tellerstand ',
    # '6/Anal29 - 5: Warmtemeting 1 Tellerstand ',
    # '6/Anal30 - 5: Warmtemeting 1 Tellerstand ',
    # '6/Anal31 - 6: Warmtemeting 2 Vermogen',
    # '6/Anal32 - 6: Warmtemeting 2 Tellerstand ',
    # '6/Anal33 - 6: Warmtemeting 2 Tellerstand ',
    # '6/Anal34 - 6: Warmtemeting 2 Tellerstand ',
    # '6/Anal35 - 6: Warmtemeting 2 Tellerstand ',
    # '6/Anal36 - 6: Warmtemeting 2 kWh totaal',
    '6/Anal37 - 10: F.sec.hr Uitkomst',
    # '6/Anal38 - 11: F.pri.hr Uitkomst',
    # '6/Anal39 - 14: F.pri.hr 2 Uitkomst',
    # '6/Dig1 - 1: Vrijgave Verwarming 1',
    # '6/Dig2 - 2: vrijgave verwarming Ext. 1',
    # '6/Dig3 - 3: Vrijgave Koeling 1',
    # '6/Dig4 - 4: vrijgave koeling Ext. 1',
    # '6/Dig5 - 5: Vrijgave Verwarming 2',
    # '6/Dig6 - 6: vrijgave verwarming Ext. 2',
    # '6/Dig7 - 7: Vrijgave Koeling 2',
    # '6/Dig8 - 8: vrijgave koeling Ext. 2',
    # '6/Dig9 - 9: Vrijgave Verwarming 3',
    # '6/Dig10 - 10: vrijgave verwarming Ext. 3',
    # '6/Dig11 - 11: Vrijgave Koeling 3',
    # '6/Dig12 - 12: vrijgave koeling Ext. 3',
    # '6/Dig13 - 13: Vrijgave Verwarming 4',
    # '6/Dig14 - 14: vrijgave verwarming Ext. 4',
    # '6/Dig15 - 15: Vrijgave Koeling 4',
    # '6/Dig16 - 16: vrijgave koeling Ext. 4',
    # '6/Dig17 - 17: Vrijgave Verwarming 5',
    # '6/Dig18 - 18: vrijgave verwarming Ext. 5',
    # '6/Dig19 - 19: Vrijgave Koeling 5',
    # '6/Dig20 - 20: vrijgave koeling Ext. 5',
    # '6/Dig21 - 21: Vrijgave Verwarming 6',
    # '6/Dig22 - 22: vrijgave verwarming Ext. 6',
    # '6/Dig23 - 23: Vrijgave Koeling 6',
    # '6/Dig24 - 24: vrijgave koeling Ext. 6',
    # '6/Dig25 - 25: Vrijgave Verwarming 7',
    # '6/Dig26',
    # '6/Dig27 - 27: Vrijgave Koeling 7',
    # '6/Dig28',
    # '6/Dig29 - 29: Vrijgave Verwarming 8',
    # '6/Dig30 - 30: vrijgave verwarming Ext. 8',
    # '6/Dig31 - 31: Vrijgave Koeling 8',
    # '6/Dig32 - 32: vrijgave koeling Ext. 8',
    # '6/Dig33 - 33: Vrijgave Verwarming 9',
    # '6/Dig34',
    # '6/Dig35 - 35: Vrijgave Koeling 9',
    # '6/Dig36',
    # '6/Dig37 - 37: Vrijgave Verwarming 10',
    # '6/Dig38 - 38: vrijgave verwarming Ext. 10',
    # '6/Dig39 - 39: Vrijgave Koeling 10',
    # '6/Dig40 - 40: vrijgave koeling Ext. 10',
    # '6/Dig41 - 4: koelbedrijf'
}

CSV_OPTIONS = {
    'sep': ';',
    'decimal': ',',
}


def debug(*values, **kwargs):
    if DEBUG_MODE:
        print(*values, **kwargs)


def parse_args() -> Namespace:
    parser = ArgumentParser('Process CSV logs')

    parser.add_argument('source_csv_path',
                        help='Path to the CSV file with the logs', type=str)
    parser.add_argument('-o', '--out_path',
                        help='Path to compiled result', type=str)

    return parser.parse_args()


def prepare_table(t: DataFrame) -> DataFrame:

    def delta_and_percent(before, after):
        delta = before - after
        return f'{str.format("{:,}", delta)} ({delta / before // 0.0001 / 100}%)'

    debug(f'Starting with {str.format("{:,}", len(t.index))} rows')

    # take one every 5 minutes
    t = t.iloc[::5, :]

    INITIAL_SIZE = len(t.index)
    debug(f'Filtering {str.format("{:,}", INITIAL_SIZE)} rows')

    t_sec_sup = t['6/Anal8 - 11: T.sec.sup']
    t_sec_ret = t['6/Anal9 - 12: T.sec.ret.']
    t_pri_sup = t['6/Anal10 - 1: T.pri.sup']
    t_pri_ret = t['6/Anal11 - 2: T.pri.ret']

    # pre-filter dat
    t = t[
        # status = AAN and alarm = UIT checks
        (t['6/Anal13 - 18: Status.well.pump'] == 0) &
        (t['6/Anal14 - 19: Alarm.well.pump'] == 1) &
        (t['6/Anal15 - 20: Status.heat.pump'] == 0) &
        (t['6/Anal16 - 21: Alarm.heat.pump'] == 1) &

        # Temperature ranges checks (secondary cycle)
        (t_sec_sup >= T_SEC_SUP_LOWER) &
        (t_sec_sup < T_SEC_SUP_UPPER) &
        (t_sec_ret >= T_SEC_RET_LOWER) &
        (t_sec_ret < T_SEC_RET_UPPER) &

        # Temperature ranges checks (primary cycle)
        (t_pri_sup >= T_PRI_SUP_LOWER) &
        (t_pri_sup < T_PRI_SUP_UPPER) &
        (t_pri_ret >= T_PRI_RET_LOWER) &
        (t_pri_ret < T_PRI_RET_UPPER)
    ]

    PRIMARY_FILTERED_SIZE = len(t.index)
    debug('Discarded', delta_and_percent(INITIAL_SIZE, PRIMARY_FILTERED_SIZE),
          'rows based on status and temperature levels')

    # pre-compute temperature differences
    t = t.assign(
        ΔT_pri=(t_pri_ret - t_pri_sup),
        ΔT_sec=(t_sec_ret - t_sec_sup)
    )

    FINAL_SIZE = len(t.index)
    debug(
        f'Discarded {delta_and_percent(PRIMARY_FILTERED_SIZE, FINAL_SIZE)} \
more rows because of invalid temperature differences\n\
Total discarded rows while filtering: \
{delta_and_percent(INITIAL_SIZE, FINAL_SIZE)}\n'
    )

    return t


def generate_flow_report(t: DataFrame) -> DataFrame:

   # back-calculate primary cycle flow
    filtered = t[(t.ΔT_pri != 0) & (t.ΔT_sec * t.ΔT_pri >= 0)]
    flow_pri_m3_5_min = filtered['6/Anal25 - 9: Sample & Hold Uitkomst'] * \
        0.9425e-3 * filtered.ΔT_sec / filtered.ΔT_pri

    flow_pri_m3_h = flow_pri_m3_5_min * 12
    mode = t['6/Anal4 - 4: koelbedrijf']
    in_cooling = flow_pri_m3_5_min[mode == COOLING].sum()
    in_heating = flow_pri_m3_5_min[mode == HEATING].sum()

    # TODO: just summing up the 5min mark, aggregation logic may need replacement ^

    E_vb = t[mode == HEATING].ΔT_pri.sum() * in_heating * 1000 * 3.8 * 3e-5
    E_kb = -t[mode == COOLING].ΔT_pri.sum() * in_heating * 1000 * 3.8 * 3e-5

    return (DataFrame({
        'Total water per month (m^3)': [flow_pri_m3_5_min.sum()],
        'Total water per month (m^3) in cooling': [in_cooling],
        'Total water per month (m^3) in heating': [in_heating],
        'Total water per month (m^3) in heat exchange': [in_cooling + in_heating],
        'Max. flow per hour (m^3)': [flow_pri_m3_h.max()],
        'Ground water??': [0]  # TODO:  out what it meant

    }),
        DataFrame({
            'E_kb': [E_kb],
            'E_vb': [E_vb],
            'Productivity': [0]  # TODO
        }))


def generate_temp_report(t: DataFrame) -> DataFrame:

    t_pri_sup = t['6/Anal10 - 1: T.pri.sup']
    t_pri_ret = t['6/Anal11 - 2: T.pri.ret']
    mode = t['6/Anal4 - 4: koelbedrijf']

    return DataFrame({
        'Max. T primary sup': [t_pri_sup.max()],
        'Max. T primary dis': [t_pri_ret.max()],
        'Cooling - avg. T primary sup': [t_pri_sup[mode == COOLING].mean()],
        'Cooling - avg. T primary dis': [t_pri_ret[mode == COOLING].mean()],
        'Heating - avg. T primary sup': [t_pri_sup[mode == HEATING].mean()],
        'Heating - avg. T primary dis': [t_pri_ret[mode == HEATING].mean()]
    })


def generate_energy_report(t: DataFrame) -> DataFrame:
    # TODO extract this logic (currently within generate_flow_report())

    mode = t['6/Anal4 - 4: koelbedrijf']
    heating = t[mode == HEATING]
    cooling = t[mode == COOLING]

    return DataFrame({
        'E_kb': [heating.ΔT_pri * heating],
        'E_kb': [0],
        'Productivity': [0]
    })


def main():

    args = parse_args()

    # read the file
    table: DataFrame = read_csv(
        args.source_csv_path,
        parse_dates={'Datum en tijd': ['Datum', 'Tijd']},
        ** CSV_OPTIONS
    )

    # process data
    prepared = prepare_table(table)
    temp_report = generate_temp_report(prepared)
    flow_report, energy_report = generate_flow_report(prepared)

    # resolve the output path
    out_path = Path(
        args.out_path or
        # FIXME: hacky str path manipulation
        f'./{args.source_csv_path[:-4] + "_report.xlsx"}'
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # write the output to a file
    with ExcelWriter(out_path) as writer:
        temp_report.to_excel(writer, sheet_name='Temperature report')
        flow_report.to_excel(writer, sheet_name='Water flow report')
        energy_report.to_excel(writer, sheet_name='Power report')


if __name__ == '__main__':
    main()
