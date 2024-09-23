--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg120+1)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dim_date; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.dim_date (
    date_id integer NOT NULL,
    date_name character varying(255)
);


ALTER TABLE public.dim_date OWNER TO your_username;

--
-- Name: dim_date_date_id_seq; Type: SEQUENCE; Schema: public; Owner: your_username
--

CREATE SEQUENCE public.dim_date_date_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dim_date_date_id_seq OWNER TO your_username;

--
-- Name: dim_date_date_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: your_username
--

ALTER SEQUENCE public.dim_date_date_id_seq OWNED BY public.dim_date.date_id;


--
-- Name: dim_energy_category; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.dim_energy_category (
    energycategory_id integer NOT NULL,
    energycategory_name character varying(255) NOT NULL
);


ALTER TABLE public.dim_energy_category OWNER TO your_username;

--
-- Name: dim_energy_category_energycategory_id_seq; Type: SEQUENCE; Schema: public; Owner: your_username
--

CREATE SEQUENCE public.dim_energy_category_energycategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dim_energy_category_energycategory_id_seq OWNER TO your_username;

--
-- Name: dim_energy_category_energycategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: your_username
--

ALTER SEQUENCE public.dim_energy_category_energycategory_id_seq OWNED BY public.dim_energy_category.energycategory_id;


--
-- Name: dim_energy_subcategory; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.dim_energy_subcategory (
    energysubcategory_id integer NOT NULL,
    energysubcategory_name character varying(255)
);


ALTER TABLE public.dim_energy_subcategory OWNER TO your_username;

--
-- Name: dim_energy_subcategory_energysubcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: your_username
--

CREATE SEQUENCE public.dim_energy_subcategory_energysubcategory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dim_energy_subcategory_energysubcategory_id_seq OWNER TO your_username;

--
-- Name: dim_energy_subcategory_energysubcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: your_username
--

ALTER SEQUENCE public.dim_energy_subcategory_energysubcategory_id_seq OWNED BY public.dim_energy_subcategory.energysubcategory_id;


--
-- Name: dim_flow_direction; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.dim_flow_direction (
    flowdirection_id integer NOT NULL,
    flowdirection_name character varying(255) NOT NULL
);


ALTER TABLE public.dim_flow_direction OWNER TO your_username;

--
-- Name: dim_flow_direction_flowdirection_id_seq; Type: SEQUENCE; Schema: public; Owner: your_username
--

CREATE SEQUENCE public.dim_flow_direction_flowdirection_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dim_flow_direction_flowdirection_id_seq OWNER TO your_username;

--
-- Name: dim_flow_direction_flowdirection_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: your_username
--

ALTER SEQUENCE public.dim_flow_direction_flowdirection_id_seq OWNED BY public.dim_flow_direction.flowdirection_id;


--
-- Name: dim_metric; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.dim_metric (
    metric_id integer NOT NULL,
    metric_name character varying(255) NOT NULL,
    metric_unit character varying(50)
);


ALTER TABLE public.dim_metric OWNER TO your_username;

--
-- Name: dim_metric_metric_id_seq; Type: SEQUENCE; Schema: public; Owner: your_username
--

CREATE SEQUENCE public.dim_metric_metric_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.dim_metric_metric_id_seq OWNER TO your_username;

--
-- Name: dim_metric_metric_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: your_username
--

ALTER SEQUENCE public.dim_metric_metric_id_seq OWNED BY public.dim_metric.metric_id;


--
-- Name: fact_energy_metrics; Type: TABLE; Schema: public; Owner: your_username
--

CREATE TABLE public.fact_energy_metrics (
    energycategory_id integer,
    energysubcategory_id integer,
    date_id integer,
    flowdirection_id integer,
    metric_id integer,
    metric_value double precision
);


ALTER TABLE public.fact_energy_metrics OWNER TO your_username;

--
-- Name: dim_date date_id; Type: DEFAULT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_date ALTER COLUMN date_id SET DEFAULT nextval('public.dim_date_date_id_seq'::regclass);


--
-- Name: dim_energy_category energycategory_id; Type: DEFAULT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_energy_category ALTER COLUMN energycategory_id SET DEFAULT nextval('public.dim_energy_category_energycategory_id_seq'::regclass);


--
-- Name: dim_energy_subcategory energysubcategory_id; Type: DEFAULT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_energy_subcategory ALTER COLUMN energysubcategory_id SET DEFAULT nextval('public.dim_energy_subcategory_energysubcategory_id_seq'::regclass);


--
-- Name: dim_flow_direction flowdirection_id; Type: DEFAULT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_flow_direction ALTER COLUMN flowdirection_id SET DEFAULT nextval('public.dim_flow_direction_flowdirection_id_seq'::regclass);


--
-- Name: dim_metric metric_id; Type: DEFAULT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_metric ALTER COLUMN metric_id SET DEFAULT nextval('public.dim_metric_metric_id_seq'::regclass);


--
-- Data for Name: dim_date; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.dim_date (date_id, date_name) FROM stdin;
1	2017
2	2023
3	2024
\.


--
-- Data for Name: dim_energy_category; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.dim_energy_category (energycategory_id, energycategory_name) FROM stdin;
1	Nuclear
2	Renewable
3	Fossil
\.


--
-- Data for Name: dim_energy_subcategory; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.dim_energy_subcategory (energysubcategory_id, energysubcategory_name) FROM stdin;
1	NaN
2	Fuel (incl. biomass)
3	Purchased or acquired electricity, heat, steam, and cooling
4	Self-generated non-fuel energy
5	Natural Gas
6	Coal and coal products
7	Crude oil and petroleum products
8	Other fossil
9	Wind
10	Solar
\.


--
-- Data for Name: dim_flow_direction; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.dim_flow_direction (flowdirection_id, flowdirection_name) FROM stdin;
1	consumption
2	production
\.


--
-- Data for Name: dim_metric; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.dim_metric (metric_id, metric_name, metric_unit) FROM stdin;
1	energy	MWh
\.


--
-- Data for Name: fact_energy_metrics; Type: TABLE DATA; Schema: public; Owner: your_username
--

COPY public.fact_energy_metrics (energycategory_id, energysubcategory_id, date_id, flowdirection_id, metric_id, metric_value) FROM stdin;
1	1	1	1	1	311067.32
2	2	1	1	1	432530.9
2	3	1	1	1	553994.48
2	4	1	1	1	675458.06
3	1	1	1	1	296250.58
3	5	1	1	1	100000
1	1	2	1	1	127407.12
2	2	2	1	1	142223.86
2	3	2	1	1	157040.6
2	4	2	1	1	171857.34
3	1	2	1	1	53323.42
1	1	3	1	1	796921.64
2	2	3	1	1	918385.22
2	3	3	1	1	1039848.8
2	4	3	1	1	1161312.38
3	6	3	1	1	37920.75
3	7	3	1	1	50000
3	5	3	1	1	34000
3	8	3	1	1	25000
3	3	3	1	1	30000
2	9	3	2	1	231000
2	10	3	2	1	143300
3	1	3	2	1	150000
\.


--
-- Name: dim_date_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: your_username
--

SELECT pg_catalog.setval('public.dim_date_date_id_seq', 1, false);


--
-- Name: dim_energy_category_energycategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: your_username
--

SELECT pg_catalog.setval('public.dim_energy_category_energycategory_id_seq', 1, false);


--
-- Name: dim_energy_subcategory_energysubcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: your_username
--

SELECT pg_catalog.setval('public.dim_energy_subcategory_energysubcategory_id_seq', 1, false);


--
-- Name: dim_flow_direction_flowdirection_id_seq; Type: SEQUENCE SET; Schema: public; Owner: your_username
--

SELECT pg_catalog.setval('public.dim_flow_direction_flowdirection_id_seq', 1, false);


--
-- Name: dim_metric_metric_id_seq; Type: SEQUENCE SET; Schema: public; Owner: your_username
--

SELECT pg_catalog.setval('public.dim_metric_metric_id_seq', 1, false);


--
-- Name: dim_date dim_date_pkey; Type: CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_date
    ADD CONSTRAINT dim_date_pkey PRIMARY KEY (date_id);


--
-- Name: dim_energy_category dim_energy_category_pkey; Type: CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_energy_category
    ADD CONSTRAINT dim_energy_category_pkey PRIMARY KEY (energycategory_id);


--
-- Name: dim_energy_subcategory dim_energy_subcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_energy_subcategory
    ADD CONSTRAINT dim_energy_subcategory_pkey PRIMARY KEY (energysubcategory_id);


--
-- Name: dim_flow_direction dim_flow_direction_pkey; Type: CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_flow_direction
    ADD CONSTRAINT dim_flow_direction_pkey PRIMARY KEY (flowdirection_id);


--
-- Name: dim_metric dim_metric_pkey; Type: CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.dim_metric
    ADD CONSTRAINT dim_metric_pkey PRIMARY KEY (metric_id);


--
-- Name: fact_energy_metrics fact_energy_metrics_date_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.fact_energy_metrics
    ADD CONSTRAINT fact_energy_metrics_date_id_fkey FOREIGN KEY (date_id) REFERENCES public.dim_date(date_id);


--
-- Name: fact_energy_metrics fact_energy_metrics_energycategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.fact_energy_metrics
    ADD CONSTRAINT fact_energy_metrics_energycategory_id_fkey FOREIGN KEY (energycategory_id) REFERENCES public.dim_energy_category(energycategory_id);


--
-- Name: fact_energy_metrics fact_energy_metrics_energysubcategory_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.fact_energy_metrics
    ADD CONSTRAINT fact_energy_metrics_energysubcategory_id_fkey FOREIGN KEY (energysubcategory_id) REFERENCES public.dim_energy_subcategory(energysubcategory_id);


--
-- Name: fact_energy_metrics fact_energy_metrics_flowdirection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.fact_energy_metrics
    ADD CONSTRAINT fact_energy_metrics_flowdirection_id_fkey FOREIGN KEY (flowdirection_id) REFERENCES public.dim_flow_direction(flowdirection_id);


--
-- Name: fact_energy_metrics fact_energy_metrics_metric_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: your_username
--

ALTER TABLE ONLY public.fact_energy_metrics
    ADD CONSTRAINT fact_energy_metrics_metric_id_fkey FOREIGN KEY (metric_id) REFERENCES public.dim_metric(metric_id);


--
-- PostgreSQL database dump complete
--

