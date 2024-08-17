DROP TABLE IF EXISTS clean_daily_subs;
create temporary table clean_daily_subs as (select daily_subs.sub_end_ts::date as sub_start_date, date_trunc('week',daily_subs.sub_end_ts::date) as sub_start_week, 
date_trunc('month',daily_subs.sub_end_ts::date) as sub_start_month, 
date_trunc('year', daily_subs.sub_end_ts::date) as sub_start_year, 
date_trunc('quarter',daily_subs.sub_end_ts::date) as sub_start_quarter,
daily_subs.user_id,
daily_subs.plan,
daily_subs.period,
concat(daily_subs.plan,' ',daily_subs.period) as full_plan_type,
daily_subs.price as local_price,
lower(daily_subs.currency) as currency_2,
daily_subs.country_code as country_code,
geo_lookup.c2 as country,
geo_lookup.c3 as continent,
geo_lookup.c5 as region
from zoom.first.daily_subs left outer join zoom.first.geo_lookup
on daily_subs.country_code = geo_lookup.c4);


select clean_daily_subs.*, exchange_rates.CURRENCY, case when clean_daily_subs.currency_2 = 'usd' then clean_daily_subs.local_price else clean_daily_subs.local_price * exchange_rates.rate end as usd_sub_price  from clean_daily_subs left outer join zoom.first.exchange_rates
on clean_daily_subs.currency_2 = exchange_rates.CURRENCY
and clean_daily_subs.sub_start_month = exchange_rates.date;