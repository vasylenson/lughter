#!/usr/bin/python3

from argparse import ArgumentParser, Namespace
from pathlib import Path
from pandas import DataFrame, read_csv

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
    # '6/Anal14 - 19: Alarm.well.pump',
    # '6/Anal15 - 20: Status.heat.pump',
    # '6/Anal16 - 21: Alarm.heat.pump',
    # '6/Anal17 - 3: p.prim.top.WHEx',
    '6/Anal18 - 13: Flow.heat.pump',
    # '6/Anal19 - 7: Impulsteller Tellerstand va',
    # '6/Anal20 - 7: RV.buiten',
    # '6/Anal21 - 8: T.buiten',
    # '6/Anal22 - 9: Dauwpunt.buiten',
    # '6/Anal23 - 10: SV.buiten',
    # '6/Anal24 - 7: Impulsteller Totale tellers',
    # '6/Anal25 - 9: Sample & Hold Uitkomst',
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
    # '6/Anal37 - 10: F.sec.hr Uitkomst',
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


def parse_args() -> Namespace:
    parser = ArgumentParser('Process CSV logs')

    parser.add_argument('source_csv_path',
                        help='Path to the CSV file with the logs', type=str)
    parser.add_argument('-o', '--output_path',
                        help='Path to compiled result', type=str)

    return parser.parse_args()


def generate_report(table: DataFrame) -> DataFrame:
    pass


def main():

    args = parse_args()
    print(args.output_path)

    # read the file
    table: DataFrame = read_csv(
        args.source_csv_path,
        parse_dates={'Datum en tijd': ['Datum', 'Tijd']},
        ** CSV_OPTIONS
    )

    # filter out invalid rows
    filtered_table = table[
        (table['6/Anal13 - 18: Status.well.pump'] == 0) &
        (table['6/Anal8 - 11: T.sec.sup'] < 20)
    ]

    # write the output to a file

    out_path = Path(args.output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    table.to_csv(
        out_path or f'./{args.source_csv_path[:-4] + "_Processed.csv"}',
        ** CSV_OPTIONS
    )


if __name__ == '__main__':
    main()
