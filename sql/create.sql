create table provider_user (
    email varchar(60) not null,
    name varchar(40) not null,
    provider varchar(40) not null,
    inserted_at timestamp not null default now(),
    id serial primary key,
    picture varchar(100),
    UNIQUE(email, provider)
);