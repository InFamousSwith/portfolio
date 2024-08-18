select i.message_date, i.full_text, i.key_id
from ideas i
join processed_keys p
on i.key_id = p.key_id
where p.processed is false
limit 100
