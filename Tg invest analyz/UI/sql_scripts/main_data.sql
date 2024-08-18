select distinct %s from prices p
join ideas i
on p.key_id = i.key_id
join tickers t
on p.ticker = t.ticker
where i.channel_name in %s
and p.real_percent_profit is not null
