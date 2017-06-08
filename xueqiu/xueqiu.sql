sqlite3 xq_0608.db;
create table IF NOT EXISTS User(id int primary key, screen_name text, gender text, province text, city text, verified
  int,
  verified_type int, cube_count int, stocks_count int, friends_count int, followers_count int, status_count int,
  last_status_id int, is_visited int default 0);