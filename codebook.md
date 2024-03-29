# Codebook
Data seems to be an SPSS dataset, but there are not file extensions and I could not find documentation in the source.  
It also seems that several CIS datasets fail to import with either [Haven](https://haven.tidyverse.org/) or [Pandas](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_spss.html)
due to [this issue](https://github.com/tidyverse/haven/issues/683) in the [ReadStat](https://github.com/WizardMac/ReadStat) library.
It has been already fixed, but not included yet (2/2/2023) in either Pandas or Haven.  
I couldn't convert the data to other formats using the last version of ReadStat, so I wrote `cis2080_to_csv.py`.

## Original card structure
The interview is structured in 5 "cards", and each card has around 80 values.  
On the original file, there are 5 rows per person interviewed, one per card.  
As each column only comprises a single character, some answers use multiple columns.

## Variable names
`cis2080_to_csv.py` transforms the original file into csv format, with column names
indicating card number and original column number, as labelled on the original questionnaire.  
For answers comprising multiple characters, these have been merged. For example, `T5_26` means
column 26 on card 5. While `T1_1-4` means columns 1 to 4, both inclusive, on card 1.

## Inconsistencies
### City code
There aren't codes for every city or town in the provided documentation. Only for the largest
city in the _provincia_ and for every city with a population over 100.000. Although not specified
in the documentation, it seems that smaller areas are coded as `0`.

### Card 5 blank page
The number of columns in card 5 is far larger than the documented variables.  
On the last page that covers the last variables of this card, there are documented variables
for a general poll weight and also weights for some regions in Andalucía, which is the first region ordered by name. The next page is blank.  
It is a reasonable guess that the undocumented variables relate to other regions that should have been on the blank page.  
We import the variable for general weight and discard consecutive columns, including those relating to Andalucía.

**Therefore, for card 5, columns after 84 are discarded.**


## Zero
It's not specified in the documentation, but it seems that very often spaces
mean zero.

## NA values
Not specified in the documentation.

For people who never smoked, the answer for the number of cigarettes a day is `-8`.
We assume this as an NA value.

In several variables, like amount of beverages or drinkin location, 9 is considered a NA.

99 is sometimes used as number, sometimes used to code a "No answer" label and sometimes as an NA value.

## Other codes for "no"
In some questions, such as telling if they have taken a specific medicament, many answers have been
coded as `0`, although the questionnaire specifically codes them as `1`, `2` and `9`. We assume
that this means "No".


## UBEs
This is a variable that represents the number of [standard drinks](https://www.niaaa.nih.gov/alcohols-effects-health/overview-alcohol-consumption/what-standard-drink) the person had during the last thursday, friday and saturday. It's labelled as its Spanish acronym "Unidades de Bebida Estándar (UBE)".

### Reference for Standard Drinks in Spain
As alcohol is drank in different containers and concentrations depending on the culture, a [spaniard reference](https://doi.org/10.20882/adicciones.621) is used.

1 beer = 1 Standard Drink  
1 glass of wine = 1 Standard Drink  
1 glass of spirits = 2 Standard Drinks

Vermouth is considered as a spirit.

## Population
The population is given in ranges. For quantitative computation the central value of each range is assigned to each one.  
For the last range "Over 1 million people", the chosen value is a rounded average of the two Spaniard cities with populations over 1 million.

## Income
As with population, income comes in ranges, that are replaced with numeric values.  
For all but the higher category, the middle value of each interval is assigned.
On last range, "Over 1 million ptas" is replaced with 1.250.000, which preserves the 250.000 step between the previous intervals.

## Impute missing data

| name                | prop  | type | aproach   | comment                |
| ------------------- | ----- | ---- | --------- | ---------------------- |
| political_espectrum | 0.336 | num  | drop      | 34%                    |
| income              | 0.319 | num  | drop      | 32%                    |
| population          | 0.001 | num  | compute   | median in their region |
| age                 | 0.003 | num  | compute   | median                 |
| cigarettes          | 0.656 | num  | assign    | 0                      |
| cigars              | 0.979 | num  | assign    | 0                      |
| occupation          | 0.045 | cat  | assign    | N.C.                   |
| drink_loc1          | 0.464 | cat  | assign    | N.C.                   |
| drink_loc2          | 0.799 | cat  | assign    | N.C.                   |
| sex                 | 0.001 | cat  | assign    | New label: "No answer" |
| sector              | 0.035 | cat  | assign    | N.S.                   |

# Impute political_spectrum and income
Could I just impute a value? Are these people similar to the rest or a well diferenciated group?
How many people results from exluding these two?

For first version, drop these two variables.
