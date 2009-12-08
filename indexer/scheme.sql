DROP TABLE IF EXISTS data_payments;

CREATE TABLE data_payments
(
  paymentid integer,  
  globalpaymentid varchar(20),
  constraint globalpaymentid primary key (globalpaymentid),
  globalrecipientid varchar(20),
  globalrecipientidx varchar(20),
  globalschemeid varchar(20),
  amounteuro numeric,
  amountnationalcurrency numeric,
  year int,
  countrypayment varchar(2)
)
WITH (OIDS=FALSE);




DROP TABLE IF EXISTS data_recipients;
CREATE TABLE data_recipients
(
  
  
  recipientid varchar(20),
  recipientidx varchar(20),
  globalrecipientid varchar(20),
  globalrecipientidx varchar(20),
  name text,
  address1 text,
  address2 text,
  zipcode varchar(20),
  town text,
  countryrecipient varchar(2),
  countrypayment varchar(2),
  geo1 text,
  geo2 text,
  geo3 text,
  geo4 text,
  geo1nationallanguage text,
  geo2nationallanguage text,
  geo3nationallanguage text,
  geo4nationallanguage text,
  lat double precision,
  lng double precision  
) WITH (OIDS=FALSE);



DROP TABLE IF EXISTS data_schemes;
CREATE TABLE data_schemes
(
  globalschemeid varchar,
  CONSTRAINT globalschemeid PRIMARY KEY (globalschemeid),
  namenationallanguage text,
  nameenglish text,
  budgetlines8digit varchar(10),
  countrypayment varchar(2)  
) WITH (OIDS=FALSE);





DROP TABLE IF EXISTS data_totals;
CREATE TABLE data_totals
(
  global_id character varying(20) NOT NULL,
  amount_euro numeric,
  "year" integer,
  countrypayment varchar(2),
  nameenglish text   
)
WITH (OIDS=FALSE);




DROP TABLE IF EXISTS data_locations;
CREATE TABLE data_locations
(
  location_type varchar(10),
  country varchar(2),
  geo1 text,
  geo2 text,
  geo3 text,
  geo4 text,
  recipients numeric,
  total numeric
)
WITH (OIDS=FALSE);

-- DROP TABLE IF EXISTS data_recipient_locations;
-- CREATE TABLE data_recipient_locations
-- (
--   global_id character varying(20) NOT NULL,
--   location text,
--   country varchar(2)
-- )
-- WITH (OIDS=FALSE);



DROP TABLE IF EXISTS data_years;
CREATE TABLE data_years
(
  country varchar(2),
  year integer,
  recipients integer,
  amount numeric
)
WITH (OIDS=FALSE);


DROP TABLE IF EXISTS data_scheme_totals;
CREATE TABLE data_scheme_totals
(
  country varchar(2),
  year integer,
  name text,
  amount numeric,
  globalschemeid varchar
)
WITH (OIDS=FALSE);


DROP TABLE IF EXISTS data_counts;
CREATE TABLE data_counts
(
  country varchar(2),
  year integer,
  type text,
  value text,
  count integer
)
WITH (OIDS=FALSE);
