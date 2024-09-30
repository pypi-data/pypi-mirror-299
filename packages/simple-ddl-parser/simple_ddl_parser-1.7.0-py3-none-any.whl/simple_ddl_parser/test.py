from simple_ddl_parser import DDLParser

ddl = """
CREATE TABLE pole.t_zuschauer (
	email varchar(50) NULL, -- email-Adresse
	CONSTRAINT t_zuschauer_email CHECK (((email IS NULL) OR ((email)::text = ''::text) OR ((email)::text ~* '([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+)\.[a-zA-Z]{2,}'::text)))
"""
result = DDLParser(ddl, debug=True).run(group_by_type=True, 
                            output_mode="mysql",
                            )

import pprint

pprint.pprint(result)