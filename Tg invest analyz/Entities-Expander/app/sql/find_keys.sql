select i.key_id from ideas i 
left join processed_keys p
on i.key_id = p.key_id 
where p.key_id isnull