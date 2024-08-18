select column_name
from information_schema.columns
where table_name = 'prices'
order by ordinal_position
