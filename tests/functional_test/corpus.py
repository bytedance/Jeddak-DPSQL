clickhouse_single_test = [
    "select count(menu_id) from menu_page group by menu_id limit 20",
    "select sum(page_number) as sum_val from menu_page group by menu_id limit 20",
    "select avg(page_number) as sum_val from menu_page group by menu_id limit 20",
    "SELECT count(c1) FROM (select count(menu_id) as c1 from menu_page group by menu_id)",
    "SELECT sum (c1) FROM (select count(menu_id) as c1 from menu_page group by menu_id)"
]

clickhouse_join_test = [
    "select count(menu.id) from menu_page inner join menu ON menu_page.menu_id=menu.id limit 10",
    "select count(menu.id) from menu_page left join menu ON menu_page.menu_id=menu.id limit 10",
    "select count(menu.id) from menu_page right join menu ON menu_page.menu_id=menu.id limit 10",
    "select count(menu.id) from menu_page full join menu ON menu_page.menu_id=menu.id limit 10",
    "select count(menu.id) from menu join menu_page ON menu_page.menu_id=menu.id join menu_item ON menu_item.menu_page_id=menu_page.id limit 10",
    "select sum(menu.id) from menu join menu_page ON menu_page.menu_id=menu.id join menu_item ON menu_item.menu_page_id=menu_page.id limit 10",
    "select count(c) from (select count(menu.id) as c from menu join menu_page ON menu_page.menu_id=menu.id join menu_item ON menu_item.menu_page_id=menu_page.id limit 10)",
    "select count(menu.id) from menu_page inner join (select * from menu) v2 on v2.menu_id=menu.id ",
    "select sum(c) from (select sum(menu.id) as c from menu join menu_page ON menu_page.menu_id=menu.id join menu_item ON menu_item.menu_page_id=menu_page.id limit 10)"
    "select count(menu_page.menu_id) from menu_page inner join (select id from menu) as v2 on v2.id=menu_page.menu_id"
]

hive_single_test = [
    "select gender, sum(age) as total_age from user_info group by gender",
    "select gender, count(age) as total_age from user_info group by gender",
    "select gender, avg(age) as total_age from user_info group by gender"
]
