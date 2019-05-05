--
-- PostgreSQL database dump
--

-- Dumped from database version 10.6 (Ubuntu 10.6-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 11.2 (Ubuntu 11.2-1.pgdg18.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: collections; Type: TABLE; Schema: public; Owner: quotable
--

CREATE TABLE public.collections (
    colid integer NOT NULL,
    uid integer,
    qid integer
);


ALTER TABLE public.collections OWNER TO quotable;

--
-- Name: collections_colid_seq; Type: SEQUENCE; Schema: public; Owner: quotable
--

CREATE SEQUENCE public.collections_colid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.collections_colid_seq OWNER TO quotable;

--
-- Name: collections_colid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: quotable
--

ALTER SEQUENCE public.collections_colid_seq OWNED BY public.collections.colid;


--
-- Name: contacts; Type: TABLE; Schema: public; Owner: quotable
--

CREATE TABLE public.contacts (
    clid integer NOT NULL,
    uid integer,
    cid integer
);


ALTER TABLE public.contacts OWNER TO quotable;

--
-- Name: contacts_clid_seq; Type: SEQUENCE; Schema: public; Owner: quotable
--

CREATE SEQUENCE public.contacts_clid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.contacts_clid_seq OWNER TO quotable;

--
-- Name: contacts_clid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: quotable
--

ALTER SEQUENCE public.contacts_clid_seq OWNED BY public.contacts.clid;


--
-- Name: quotes; Type: TABLE; Schema: public; Owner: quotable
--

CREATE TABLE public.quotes (
    qid integer NOT NULL,
    firstname character varying(30),
    lastname character varying(30),
    text text,
    uploader integer
);


ALTER TABLE public.quotes OWNER TO quotable;

--
-- Name: quotes_qid_seq; Type: SEQUENCE; Schema: public; Owner: quotable
--

CREATE SEQUENCE public.quotes_qid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.quotes_qid_seq OWNER TO quotable;

--
-- Name: quotes_qid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: quotable
--

ALTER SEQUENCE public.quotes_qid_seq OWNED BY public.quotes.qid;


--
-- Name: shared; Type: TABLE; Schema: public; Owner: quotable
--

CREATE TABLE public.shared (
    sid integer NOT NULL,
    uid integer,
    cid integer,
    qid integer
);


ALTER TABLE public.shared OWNER TO quotable;

--
-- Name: shared_sid_seq; Type: SEQUENCE; Schema: public; Owner: quotable
--

CREATE SEQUENCE public.shared_sid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.shared_sid_seq OWNER TO quotable;

--
-- Name: shared_sid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: quotable
--

ALTER SEQUENCE public.shared_sid_seq OWNED BY public.shared.sid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: quotable
--

CREATE TABLE public.users (
    uid integer NOT NULL,
    name character varying(50),
    email character varying(100),
    username character varying(20),
    password character varying(100)
);


ALTER TABLE public.users OWNER TO quotable;

--
-- Name: users_uid_seq; Type: SEQUENCE; Schema: public; Owner: quotable
--

CREATE SEQUENCE public.users_uid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_uid_seq OWNER TO quotable;

--
-- Name: users_uid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: quotable
--

ALTER SEQUENCE public.users_uid_seq OWNED BY public.users.uid;


--
-- Name: collections colid; Type: DEFAULT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.collections ALTER COLUMN colid SET DEFAULT nextval('public.collections_colid_seq'::regclass);


--
-- Name: contacts clid; Type: DEFAULT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.contacts ALTER COLUMN clid SET DEFAULT nextval('public.contacts_clid_seq'::regclass);


--
-- Name: quotes qid; Type: DEFAULT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.quotes ALTER COLUMN qid SET DEFAULT nextval('public.quotes_qid_seq'::regclass);


--
-- Name: shared sid; Type: DEFAULT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.shared ALTER COLUMN sid SET DEFAULT nextval('public.shared_sid_seq'::regclass);


--
-- Name: users uid; Type: DEFAULT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.users ALTER COLUMN uid SET DEFAULT nextval('public.users_uid_seq'::regclass);


--
-- Data for Name: collections; Type: TABLE DATA; Schema: public; Owner: quotable
--

COPY public.collections (colid, uid, qid) FROM stdin;
4	1	4
15	3	14
17	3	4
18	4	15
19	4	16
20	1	16
\.


--
-- Data for Name: contacts; Type: TABLE DATA; Schema: public; Owner: quotable
--

COPY public.contacts (clid, uid, cid) FROM stdin;
5	1	3
6	3	1
7	4	1
8	4	3
\.


--
-- Data for Name: quotes; Type: TABLE DATA; Schema: public; Owner: quotable
--

COPY public.quotes (qid, firstname, lastname, text, uploader) FROM stdin;
4	Theon	Greyjoy	<p>What is dead may never die.</p>	1
14	Tyrion	Lannister	<p>Never forget what you are. The rest of the world won't. Wear it like armor, and it can never be used to hurt you.</p>	3
15	Louis	Székely	<p>When a person tells you that you hurt them, you don't get to decide that you didn't.</p>	4
16	Jimmy	Dean	<p>I can't change the direction of the wind, but I can adjust my sails to always reach my destination.</p>	4
\.


--
-- Data for Name: shared; Type: TABLE DATA; Schema: public; Owner: quotable
--

COPY public.shared (sid, uid, cid, qid) FROM stdin;
3	3	1	14
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: quotable
--

COPY public.users (uid, name, email, username, password) FROM stdin;
1	Julian Cuevas	julian.cuevas1@upr.edu	jdcuevas	$5$rounds=535000$g6FDpMHjROjR2avN$n/cVum0B8bj37lg2dTOEof2QlRhBaQsJpUbhb1Wqyf/
3	John Doe	john.doe@upr.edu	jdoe	$5$rounds=535000$x3EqEckCYQS.0AoK$Z3VqUAv4rNiVPd84Yo4JqKUG5Ip8ztLPVYQO6S.c1vC
4	Jane Doe	jane.doe@upr.edu	janed	$5$rounds=535000$fPmr5CZo6hYi0bXu$Is/Ihvf/8GJAHN8qudermu.iq8FG6jHESOCDM4kWWE3
\.


--
-- Name: collections_colid_seq; Type: SEQUENCE SET; Schema: public; Owner: quotable
--

SELECT pg_catalog.setval('public.collections_colid_seq', 20, true);


--
-- Name: contacts_clid_seq; Type: SEQUENCE SET; Schema: public; Owner: quotable
--

SELECT pg_catalog.setval('public.contacts_clid_seq', 8, true);


--
-- Name: quotes_qid_seq; Type: SEQUENCE SET; Schema: public; Owner: quotable
--

SELECT pg_catalog.setval('public.quotes_qid_seq', 16, true);


--
-- Name: shared_sid_seq; Type: SEQUENCE SET; Schema: public; Owner: quotable
--

SELECT pg_catalog.setval('public.shared_sid_seq', 5, true);


--
-- Name: users_uid_seq; Type: SEQUENCE SET; Schema: public; Owner: quotable
--

SELECT pg_catalog.setval('public.users_uid_seq', 4, true);


--
-- Name: collections collections_pkey; Type: CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_pkey PRIMARY KEY (colid);


--
-- Name: contacts contacts_pkey; Type: CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_pkey PRIMARY KEY (clid);


--
-- Name: quotes quotes_pkey; Type: CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_pkey PRIMARY KEY (qid);


--
-- Name: shared shared_pkey; Type: CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.shared
    ADD CONSTRAINT shared_pkey PRIMARY KEY (sid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (uid);


--
-- Name: collections collections_qid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_qid_fkey FOREIGN KEY (qid) REFERENCES public.quotes(qid);


--
-- Name: collections collections_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.collections
    ADD CONSTRAINT collections_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: contacts contacts_cid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_cid_fkey FOREIGN KEY (cid) REFERENCES public.users(uid);


--
-- Name: contacts contacts_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.contacts
    ADD CONSTRAINT contacts_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- Name: quotes quotes_uploader_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.quotes
    ADD CONSTRAINT quotes_uploader_fkey FOREIGN KEY (uploader) REFERENCES public.users(uid);


--
-- Name: shared shared_cid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.shared
    ADD CONSTRAINT shared_cid_fkey FOREIGN KEY (cid) REFERENCES public.users(uid);


--
-- Name: shared shared_qid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.shared
    ADD CONSTRAINT shared_qid_fkey FOREIGN KEY (qid) REFERENCES public.quotes(qid);


--
-- Name: shared shared_uid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: quotable
--

ALTER TABLE ONLY public.shared
    ADD CONSTRAINT shared_uid_fkey FOREIGN KEY (uid) REFERENCES public.users(uid);


--
-- PostgreSQL database dump complete
--

