create table user_profile (
    email varchar(60) not null,
    name varchar(40) not null,
    created_at timestamp not null default now(),
    id serial primary key,
    picture varchar(100),
    UNIQUE(email)
);

create table pet_family (
    id serial primary key,
    name varchar(60) not null,
    detail text,
    created_at timestamp not null default now()
    picture varchar(100)
    UNIQUE(name)
)

create table pet_type (
    id serial primary key,
    name varchar(60) not null,
    detail text,
    created_at timestamp not null default now(),
    edited_at timestamp,
    family_id integer references pet_family(id),
    user_id integer references user_profile(id)
    UNIQUE(name, family_id)
)