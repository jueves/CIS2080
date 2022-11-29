# Codebook
## Original card structure
The interview is structured in 5 "cards", and each card has around 80 values.  
On the original file, there are 5 rows per person interviewed, one per card.  
As each column only comprises a single character, some answers use multiple columns.

## Variable names
`cis2080_to_csv.py` transforms the original file into csv format, with column names
indicating card number and original column number, as labelled on the original questionnaire.  
For answers comprising multiple characters, these have been merged. For example, `T5_26` means
column 26 on card 5. While `T1_1-4` means columns 1 to 4, both inclusive, on card 1.

| Coded column name | Long name      | Description |
|-------------------|----------------|-------------|
| T5_26             | sex            |             |
| T5_27-28          | age            |             |
| T5_29             | marital_status |             |
| T5_30-31          | num_children   |             |


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
We asume this as an NA value.

## Other codes for "no"
In some questions, such as telling if they have taken a specific medicament, many answers have been
coded as `0`, although the questionnaire specifically codes them as `1`, `2` and `9`. We assume
that this means "No".