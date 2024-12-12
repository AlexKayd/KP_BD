-- Drop table

-- DROP TABLE public.admins;

CREATE TABLE public.admins (
	admin_id serial4 NOT NULL,
	login varchar(50) NOT NULL,
	"password" int4 NOT NULL,
	"name" varchar(100) NULL,
	surname varchar(100) NULL,
	sex varchar(10) NULL,
	phone_number varchar(15) NULL
);

-- Drop table

-- DROP TABLE public.deliveries;

CREATE TABLE public.deliveries (
	delivery_id serial4 NOT NULL,
	order_id int4 NULL,
	address varchar(255) NULL,
	delivery_time timestamp NULL,
	delivery_cost numeric(10, 2) NULL,
	telephone varchar(15) NULL,
	CONSTRAINT deliveries_pkey PRIMARY KEY (delivery_id),
	CONSTRAINT fk_order_delivery FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE
);

-- Drop table

-- DROP TABLE public.diameters;

CREATE TABLE public.diameters (
	diameter_id serial4 NOT NULL,
	diameter numeric(10, 2) NULL,
	CONSTRAINT diameters_pkey PRIMARY KEY (diameter_id)
);

-- Drop table

-- DROP TABLE public.materials;

CREATE TABLE public.materials (
	material_id serial4 NOT NULL,
	material varchar(100) NULL,
	price numeric(10, 2) NULL,
	CONSTRAINT materials_pkey PRIMARY KEY (material_id)
);

-- Drop table

-- DROP TABLE public.orders;

CREATE TABLE public.orders (
	order_id serial4 NOT NULL,
	size_id int4 NULL,
	material_id int4 NULL,
	quantity int4 NULL,
	diameter_id int4 NULL,
	total_cost numeric(10, 2) NULL,
	CONSTRAINT orders_pkey PRIMARY KEY (order_id),
	CONSTRAINT fk_diameter FOREIGN KEY (diameter_id) REFERENCES public.diameters(diameter_id) ON DELETE CASCADE,
	CONSTRAINT fk_material FOREIGN KEY (material_id) REFERENCES public.materials(material_id) ON DELETE CASCADE,
	CONSTRAINT fk_size FOREIGN KEY (size_id) REFERENCES public.sizes(size_id) ON DELETE CASCADE
);

-- Drop table

-- DROP TABLE public.sizes;

CREATE TABLE public.sizes (
	size_id serial4 NOT NULL,
	"size" varchar(50) NULL,
	price numeric(10, 2) NULL,
	CONSTRAINT sizes_pkey PRIMARY KEY (size_id)
);

-- Drop table

-- DROP TABLE public.user_actions;

CREATE TABLE public.user_actions (
	action_id serial4 NOT NULL,
	order_id int4 NULL,
	user_id int4 NULL,
	"action" varchar(255) NULL,
	"time" timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT user_actions_pkey PRIMARY KEY (action_id),
	CONSTRAINT fk_order FOREIGN KEY (order_id) REFERENCES public.orders(order_id) ON DELETE CASCADE,
	CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES public.users(user_id) ON DELETE CASCADE
);

-- Table Triggers

create trigger trigger_set_default_action_active before
insert
    on
    public.user_actions for each row execute function set_default_action_active();

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	user_id serial4 NOT NULL,
	login varchar(50) NOT NULL,
	password_hash bytea NOT NULL,
	"name" varchar(100) NULL,
	surname varchar(100) NULL,
	sex varchar(10) NULL,
	phone_number varchar(15) NULL,
	CONSTRAINT users_login_key UNIQUE (login),
	CONSTRAINT users_phone_number_key UNIQUE (phone_number),
	CONSTRAINT users_pkey PRIMARY KEY (user_id)
);

-- DROP FUNCTION public.set_default_action_active();

CREATE OR REPLACE FUNCTION public.set_default_action_active()
 RETURNS trigger
 LANGUAGE plpgsql
AS $function$
BEGIN
  -- Устанавливаем значение "активный" по умолчанию
  IF NEW.action IS NULL THEN
    NEW.action := 'активный';
  END IF;
  RETURN NEW;
END;
$function$
;

-- Триггер, срабатывающий при вставке новых записей в таблицу user_actions
CREATE TRIGGER trigger_set_default_action_active
BEFORE INSERT ON public.user_actions
FOR EACH ROW
EXECUTE FUNCTION public.set_default_action_active();