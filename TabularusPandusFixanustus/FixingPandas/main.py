import pandas as pd

# Some globals.
by_columns = 1


# Is needed for preiod_compress function.
def period_division(table_with_period, period_limit, period_step, period_prefix):
    # Table stack will keep data divided by period_step
    table_stack = []

    # The values are poped, so we need to reverse the list to keep period_prefix in order.
    period_prefix.reverse()

    bottom_period = 0
    while bottom_period + period_step <= period_limit:
        # This way it keeps chronological order.
        period_bit = table_with_period[(table_with_period.period > bottom_period) &
                                       (table_with_period.period <= bottom_period + period_step)]

        # Keeps names distinct to avoid collisions.
        period_bit = period_bit.add_prefix(period_prefix.pop())

        table_stack.append(period_bit)

        bottom_period += period_step

    return table_stack


# Just resolves a trouble realted to ids and does period_division
def period_division_and_drop_broken_ids(table_with_period, period_limit, period_step, period_prefix, broken_ids):
    # Main obective of this function is correct column concatenation.

    periods = period_division(table_with_period, period_limit, period_step, period_prefix)

    # We need some preparations before concatenation.
    for table in periods:
        table.reset_index(drop=True, inplace=True)
    # pd.concat requires indexes to be equal, otherwise it will generate NaN-s.

    # Concatenated, but with several ids.
    period_table = pd.concat(periods, axis=by_columns)

    # So, let's get rid of them.
    return period_table.drop(broken_ids, axis=by_columns)


# Returns data shuffled by periods.
def preiod_compress(period_table, quartile=False, half_years=False):

    # The way data gets separated.
    period_limit = 12
    by_quartile = 4
    by_half_years = 2
    # What kind of trickery it is? I'm not to explain.

    # Prefixes are later used to concatenate tables.
    quartile_period_prefix = ["Fiqua_", "Sequa_", "Thqua_"]
    half_year_period_prefix = ["Fiyear_", "Seyear_", "Thyear_", "Frryear_", "Fvyear_", "Siyear_"]

    # Rename ids to make them correct.
    quartile_period_correct_id = quartile_period_prefix[0] + "id"
    half_year_period_correct_id = half_year_period_prefix[0] + "id"

    # Broken ids.
    quartile_period_broken_ids = [pre + "id" for pre in quartile_period_prefix[1:]]
    half_year_period_broken_ids = [pre + "id" for pre in half_year_period_prefix[1:]]

    correct_naming = str()

    if quartile:
        period_table = period_division_and_drop_broken_ids(
            period_table, period_limit, by_quartile, quartile_period_prefix, quartile_period_broken_ids)
        correct_naming = quartile_period_correct_id

    if half_years:
        period_table = period_division_and_drop_broken_ids(
            period_table, period_limit, by_half_years, half_year_period_prefix, half_year_period_broken_ids)
        correct_naming = half_year_period_correct_id

    period_table = period_table.rename(columns={correct_naming: "id"})

    return period_table
# The longer the period, the denser the data.


def help_extract_periods(period_names):
    return list(period_names.iloc[:, 0].values)


# This fucntion is basically is a shortcut.
def apply_preiod_compression(period_table, drop_periods=True):

    quartiles_table = preiod_compress(period_table, quartile=True)
    half_years_table = preiod_compress(period_table, half_years=True)

    # Actually, we don't need periods.
    if drop_periods:

        exctaction_name = r'(.*period)$'

        # Unfortunately, I have to use this.
        quartiles_period_names = quartiles_table.columns.str.extract(exctaction_name).dropna()
        half_years_period_names = half_years_table.columns.str.extract(exctaction_name).dropna()

        # Getting lists.
        quartiles_period_names = help_extract_periods(quartiles_period_names)
        half_years_period_names = help_extract_periods(half_years_period_names)

        # Getting shit done at last.
        quartiles_table.drop(quartiles_period_names, axis=by_columns, inplace=True)
        half_years_table.drop(half_years_period_names, axis=by_columns, inplace=True)

    # There were some insane troubles with the name period.
    # Check:
    #   print(period_table["period"])
    #   del period_table["period"]
    # That's why I delete period afterwards. Not from the very beginning.
    # It's possible "period" name is preserved.

    return quartiles_table, half_years_table


periods_table = pd.read_csv("tabular_data.csv")

# The only difference between quartile_table and half_years_table is how dense data is spread (density per example).
quartile_table, half_year_table = apply_preiod_compression(periods_table)

print(quartile_table)
print(half_year_table)
# Wow, let's finish it for now.
