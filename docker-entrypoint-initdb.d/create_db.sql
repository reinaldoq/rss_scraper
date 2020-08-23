create table subscription(
    id serial primary key,
    url varchar,
    create_date timestamp with time zone default current_timestamp
)