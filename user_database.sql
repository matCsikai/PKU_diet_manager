--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

ALTER TABLE IF EXISTS ONLY public.diet_users DROP CONSTRAINT IF EXISTS pk_diet_users_id CASCADE;


DROP TABLE IF EXISTS public.diet_users;
DROP SEQUENCE IF EXISTS public.diet_users_id_seq;
CREATE TABLE diet_users (
    id serial NOT NULL,
    username varchar(30) UNIQUE,
    password varchar(120),
    submission_time timestamp without time zone,
	tolerance int,
	CHECK (tolerance > 19 AND tolerance < 1001)
);


ALTER TABLE ONLY diet_users
    ADD CONSTRAINT pk_diet_users_id PRIMARY KEY (id);


INSERT INTO diet_users VALUES (1, 'Kata', 'pbkdf2:sha256:50000$k8ozXFeh$c3cdf6863b5a2243afd85d13a6bdd22d82a0905fc043073f9bfeadb3a246118c', '2017-04-28 08:29:00', 100);
INSERT INTO diet_users VALUES (2, 'Daniel', 'pbkdf2:sha256:50000$D16YPd4i$033443d86e789ac31aba8581b9e568a6de1f82f8879d3d8c2a1ea2e1ae4ef6e9', '2017-04-28 08:29:00', 200);
INSERT INTO diet_users VALUES (3, 'Béci', 'pbkdf2:sha256:50000$vQUz23E0$6c8d838d29f7876292bd51d78aa71030502a4950afd3970c4ab9d66f96f88562', '2017-04-28 08:29:00', 300);
SELECT pg_catalog.setval('diet_users_id_seq', 3, true);

