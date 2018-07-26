create table user_profile (
    email varchar(60) not null,
    name varchar(40) not null,
    inserted_at timestamp not null default now(),
    id serial primary key,
    picture varchar(100),
    UNIQUE(email)
);