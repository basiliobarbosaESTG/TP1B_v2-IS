--
-- PostgreSQL database dump
--

-- Dumped from database version 14.1
-- Dumped by pg_dump version 14.1

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

--
-- Name: delete_xmlfile(integer); Type: PROCEDURE; Schema: public; Owner: marco
--

CREATE PROCEDURE public.delete_xmlfile(IN _id integer)
    LANGUAGE sql
    AS $$
DELETE FROM public.xmldata WHERE id = _id
$$;


ALTER PROCEDURE public.delete_xmlfile(IN _id integer) OWNER TO marco;

--
-- Name: getathelet(); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.getathelet()
    LANGUAGE plpgsql
    AS $$ 
DECLARE
	_local TEXT := 'tokyo-2020';
	_path_nome TEXT := '/olympics/atheletes/athlete[@id=/olympics/olympic_results/local_event[@id="'+_local+']/discipline[@id="Shooting"]/
			 event_title[@id="50m Rifle 3 Positions women"]/event_gender[@id="Women"]/medal_type[@id="GOLD"]/athelete/@id]/athlete_full_name/text()';
	_path_ano TEXT := '/olympics/atheletes/athlete[@id=/olympics/olympic_results/local_event[@id="tokyo-2020"]/discipline[@id="Shooting"]/
			 event_title[@id="50m Rifle 3 Positions women"]/event_gender[@id="Women"]/medal_type[@id="GOLD"]/athelete/@id]/athlete_year_birth/text()';
BEGIN
SELECT XPATH(_path_nome, xml), XPATH(_path_ano, xml)
from xmldata where id =6;
END
$$;


ALTER PROCEDURE public.getathelet() OWNER TO postgres;

--
-- Name: getathelet(text, text); Type: PROCEDURE; Schema: public; Owner: postgres
--

CREATE PROCEDURE public.getathelet(IN _path1 text, IN _path2 text)
    LANGUAGE sql
    AS $$ 
SELECT XPATH(_path1, xml), XPATH(_path2, xml) from xmldata where id =6;
$$;


ALTER PROCEDURE public.getathelet(IN _path1 text, IN _path2 text) OWNER TO postgres;

--
-- Name: insert_xmlfile(character varying, xml, date); Type: PROCEDURE; Schema: public; Owner: marco
--

CREATE PROCEDURE public.insert_xmlfile(IN filename character varying, IN xmlfile xml, IN datetime date)
    LANGUAGE sql
    AS $$
INSERT INTO public.xmldata(filename, xml, date) VALUES (filename ,xmlfile, datetime);
$$;


ALTER PROCEDURE public.insert_xmlfile(IN filename character varying, IN xmlfile xml, IN datetime date) OWNER TO marco;

--
-- Name: movedeleted(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION public.movedeleted() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
    INSERT INTO Deleted_xmldata VALUES((OLD).*);
    RETURN OLD;
  END;
$$;


ALTER FUNCTION public.movedeleted() OWNER TO postgres;

--
-- Name: update_xmlfile(integer, character varying, xml, date); Type: PROCEDURE; Schema: public; Owner: marco
--

CREATE PROCEDURE public.update_xmlfile(IN _id integer, IN _filename character varying, IN _xmlfile xml, IN _datetime date)
    LANGUAGE sql
    AS $$
UPDATE public.xmldata SET filename = _filename, xml = _xmlfile, date = _datetime WHERE id = _id;
$$;


ALTER PROCEDURE public.update_xmlfile(IN _id integer, IN _filename character varying, IN _xmlfile xml, IN _datetime date) OWNER TO marco;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: deleted_xmldata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.deleted_xmldata (
    id integer,
    filename character varying(255),
    xml xml,
    date date
);


ALTER TABLE public.deleted_xmldata OWNER TO postgres;

--
-- Name: xmldata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.xmldata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.xmldata_id_seq OWNER TO postgres;

--
-- Name: xmldata; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.xmldata (
    id integer DEFAULT nextval('public.xmldata_id_seq'::regclass) NOT NULL,
    filename character varying(255) NOT NULL,
    xml xml NOT NULL,
    date date NOT NULL
);


ALTER TABLE public.xmldata OWNER TO postgres;

--
-- Data for Name: deleted_xmldata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.deleted_xmldata (id, filename, xml, date) FROM stdin;
\.


--
-- Data for Name: xmldata; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.xmldata (id, filename, xml, date) FROM stdin;
\.


--
-- Name: xmldata_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.xmldata_id_seq', 1, true);


--
-- Name: xmldata xmldata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.xmldata
    ADD CONSTRAINT xmldata_pkey PRIMARY KEY (id);


--
-- Name: xmldata movedeleted; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER movedeleted BEFORE DELETE ON public.xmldata FOR EACH ROW EXECUTE FUNCTION public.movedeleted();


--
-- PostgreSQL database dump complete
--

