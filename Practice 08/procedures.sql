CREATE OR REPLACE PROCEDURE upsert_contact(p_first_name VARCHAR, p_last_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_first_name AND last_name = p_last_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_first_name AND last_name = p_last_name;
    ELSE
        INSERT INTO phonebook(first_name, last_name, phone) VALUES(p_first_name, p_last_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_proc(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook 
    WHERE first_name = p_identifier OR phone = p_identifier;
END;
$$;
CREATE OR REPLACE PROCEDURE bulk_insert_simple(
    p_fnames VARCHAR[],
    p_lnames VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_fnames, 1) LOOP
        INSERT INTO phonebook(first_name, last_name, phone)
        VALUES (p_fnames[i], p_lnames[i], p_phones[i])
        ON CONFLICT (phone) DO NOTHING;
    END LOOP;
END;
$$;