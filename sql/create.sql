create table users (
    email varchar(60) not null,
    provider varchar(40) not null,
    inserted_at timestamp not null default now(),
    id serial primary key,
    UNIQUE(email)
);