create table subscription(
    id serial primary key,
    url varchar,
    create_date timestamp with time zone default current_timestamp
);

create table items(
    id serial primary key,
    subscription_id integer REFERENCES subscription (id),
    title varchar,
    link varchar ,
    published date,
    description varchar ,
    read boolean default false,
    create_date timestamp with time zone default current_timestamp
);